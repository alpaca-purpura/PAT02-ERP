# -*- coding: utf-8 -*-

from odoo import models, fields, api
import hashlib
import json
import logging

_logger = logging.getLogger(__name__)


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'
    
    # Campos para RAG (Retrieval-Augmented Generation)
    x_embedding = fields.Binary('Vector Embedding', 
                               help='Embedding vectorial del contenido para búsqueda semántica')
    x_embedding_model = fields.Char('Modelo de Embedding', default='gemini-embedding-001',
                                   help='Modelo utilizado para generar el embedding')
    x_chunk_index = fields.Integer('Índice de Chunk', default=0,
                                  help='Índice del fragmento si el documento fue dividido')
    x_parent_document_id = fields.Many2one('ir.attachment', 'Documento Padre',
                                          help='Documento original si este es un fragmento')
    x_content_hash = fields.Char('Hash de Contenido', compute='_compute_content_hash', store=True,
                                help='Hash SHA256 del contenido para detectar cambios')
    x_indexed_date = fields.Datetime('Fecha de Indexación',
                                    help='Fecha en que se generó el embedding')
    
    # Relaciones con entidades PATCO para filtrado contextual
    x_equipment_category_ids = fields.Many2many(
        'maintenance.equipment.category', 
        'attachment_equipment_category_rel',
        'attachment_id', 'category_id',
        string='Categorías de Equipo Relacionadas',
        help='Categorías de equipos a las que aplica este documento'
    )
    x_service_nature_ids = fields.Many2many(
        'patco.service.nature',
        'attachment_service_nature_rel',
        'attachment_id', 'nature_id',
        string='Naturalezas de Servicio Relacionadas',
        help='Tipos de servicio a los que aplica este documento'
    )
    
    # Clasificación de documentos
    x_document_type = fields.Selection([
        ('manual', 'Manual Técnico'),
        ('procedure', 'Procedimiento'),
        ('checklist', 'Lista de Verificación'),
        ('report', 'Reporte de Servicio'),
        ('image', 'Imagen Técnica'),
        ('video', 'Video Instructivo'),
        ('specification', 'Especificación Técnica'),
        ('diagram', 'Diagrama'),
        ('other', 'Otro')
    ], string='Tipo de Documento', default='other',
       help='Clasificación del tipo de documento para filtrado')
    
    # Estado de indexación
    x_is_indexed = fields.Boolean('Indexado para RAG', default=False,
                                 help='Indica si el documento ha sido procesado para búsqueda semántica')
    x_indexing_error = fields.Text('Error de Indexación',
                                  help='Descripción del error si falló la indexación')
    x_indexing_priority = fields.Selection([
        ('low', 'Baja'),
        ('normal', 'Normal'),
        ('high', 'Alta'),
        ('urgent', 'Urgente')
    ], string='Prioridad de Indexación', default='normal',
       help='Prioridad para el procesamiento de indexación')
    
    # Metadatos adicionales para RAG
    x_language = fields.Selection([
        ('es', 'Español'),
        ('en', 'Inglés'),
        ('pt', 'Portugués')
    ], string='Idioma', default='es',
       help='Idioma del documento para procesamiento de texto')
    
    x_technical_level = fields.Selection([
        ('basic', 'Básico'),
        ('intermediate', 'Intermedio'),
        ('advanced', 'Avanzado'),
        ('expert', 'Experto')
    ], string='Nivel Técnico', default='intermediate',
       help='Nivel técnico del contenido')
    
    x_keywords = fields.Char('Palabras Clave',
                            help='Palabras clave separadas por comas para mejorar búsquedas')
    
    @api.depends('raw')
    def _compute_content_hash(self):
        """Computa hash SHA256 del contenido"""
        import base64
        import binascii
        
        for record in self:
            if not record.raw:
                record.x_content_hash = False
                continue
            
            try:
                # Validar que el contenido sea base64 válido
                decoded_content = base64.b64decode(record.raw, validate=True)
                record.x_content_hash = hashlib.sha256(decoded_content).hexdigest()
            except (binascii.Error, ValueError) as e:
                # Si no es base64 válido, intentar como string directo
                try:
                    content_bytes = record.raw.encode('utf-8') if isinstance(record.raw, str) else record.raw
                    record.x_content_hash = hashlib.sha256(content_bytes).hexdigest()
                except Exception:
                    # Como último recurso, asignar False
                    record.x_content_hash = False
                    _logger.warning(f"Could not compute content hash for attachment {record.id}: {e}")
    
    def action_index_for_rag(self):
        """Indexa el documento inmediatamente para RAG con verificación de duplicados"""
        self.ensure_one()
        
        # Validar que el documento sea indexable
        if not self.raw:
            self.x_indexing_error = "No hay contenido para indexar"
            return False
        
        # Validar tipo MIME soportado
        supported_mimetypes = [
            'application/pdf',
            'text/plain',
            'text/html',
            'image/jpeg',
            'image/png',
            'application/msword',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        ]
        
        if self.mimetype not in supported_mimetypes:
            self.x_indexing_error = f"Tipo MIME no soportado: {self.mimetype}"
            return False
        
        # Verificar si ya está indexado y el contenido no ha cambiado
        if self.x_is_indexed and self.x_content_hash:
            current_hash = hashlib.sha256(base64.b64decode(self.raw)).hexdigest()
            if current_hash == self.x_content_hash:
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': '✅ Documento ya indexado',
                        'message': f'El documento "{self.name}" ya está indexado y no ha cambiado.',
                        'type': 'info',
                        'sticky': False,
                    }
                }
        
        # Marcar para indexación con prioridad urgente
        self.write({
            'x_is_indexed': False,
            'x_indexing_error': False,
            'x_indexed_date': False,
            'x_indexing_priority': 'urgent'  # Prioridad urgente para procesamiento inmediato
        })
        
        # Intentar procesamiento inmediato
        try:
            success = self._process_document_immediately()
            if success:
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': '🚀 Indexación Completada',
                        'message': f'El documento "{self.name}" ha sido indexado exitosamente para RAG.',
                        'type': 'success',
                        'sticky': False,
                    }
                }
            else:
                # Si falla el procesamiento inmediato, queda marcado para el servicio indexer
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': '⏳ Documento en Cola',
                        'message': f'El documento "{self.name}" ha sido marcado para indexación. El servicio indexer lo procesará automáticamente.',
                        'type': 'warning',
                        'sticky': False,
                    }
                }
        except Exception as e:
            _logger.error(f"Error en indexación inmediata: {e}")
            self.x_indexing_error = f"Error en indexación inmediata: {str(e)}"
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': '❌ Error de Indexación',
                    'message': f'Error al indexar "{self.name}": {str(e)}',
                    'type': 'danger',
                    'sticky': True,
                }
            }
    
    def _process_document_immediately(self):
        """
        Procesa el documento inmediatamente usando la lógica del indexer
        
        Returns:
            bool: True si el procesamiento fue exitoso, False en caso contrario
        """
        try:
            # Importar y usar la lógica del indexer
            import sys
            import os
            
            # Agregar el path del indexer al sys.path temporalmente
            indexer_path = '/app' if os.path.exists('/app/indexer.py') else os.path.join(os.getcwd(), 'ai-services', 'indexer')
            if indexer_path not in sys.path:
                sys.path.insert(0, indexer_path)
            
            # Intentar importar el indexer
            try:
                from indexer import DocumentIndexer
                
                # Crear instancia del indexer
                indexer = DocumentIndexer()
                
                # Preparar datos del documento
                document_data = {
                    'id': self.id,
                    'name': self.name,
                    'raw': self.raw,
                    'mimetype': self.mimetype,
                    'res_model': self.res_model,
                    'res_id': self.res_id,
                    'x_document_type': self.x_document_type,
                    'x_content_hash': self.x_content_hash,
                    'x_equipment_category_ids': self.x_equipment_category_ids.ids if self.x_equipment_category_ids else [],
                    'x_service_nature_ids': self.x_service_nature_ids.ids if self.x_service_nature_ids else [],
                    'create_date': self.create_date
                }
                
                # Procesar el documento
                import asyncio
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                try:
                    # Conectar a la base de datos
                    loop.run_until_complete(indexer.connect_db())
                    
                    # Procesar el documento
                    embeddings_data = loop.run_until_complete(indexer.process_document(document_data))
                    
                    if embeddings_data:
                        # Guardar embeddings
                        loop.run_until_complete(indexer.save_embeddings(embeddings_data))
                        _logger.info(f"Documento {self.name} (ID: {self.id}) indexado inmediatamente")
                        return True
                    else:
                        _logger.warning(f"No se generaron embeddings para el documento {self.name} (ID: {self.id})")
                        return False
                        
                finally:
                    loop.close()
                    
            except ImportError as e:
                _logger.warning(f"No se pudo importar el indexer: {e}. El documento será procesado por el servicio indexer.")
                return False
                
        except Exception as e:
            _logger.error(f"Error en procesamiento inmediato del documento {self.id}: {e}")
            return False
    
    def action_reindex_for_rag(self):
        """Fuerza la re-indexación del documento"""
        self.ensure_one()
        
        # Limpiar datos de indexación anterior
        self.write({
            'x_embedding': False,
            'x_is_indexed': False,
            'x_indexing_error': False,
            'x_indexed_date': False,
            'x_indexing_priority': 'urgent'
        })
        
        return self.action_index_for_rag()
    
    def search_similar(self, query: str, context: dict = None, limit: int = 10) -> 'IrAttachment':
        """
        Búsqueda por similitud semántica usando el servicio RAG avanzado.
        
        Args:
            query: Consulta de búsqueda
            context: Contexto de la conversación (opcional)
            limit: Número máximo de resultados
            
        Returns:
            Recordset de attachments similares
        """
        
        try:
            # Usar el servicio RAG avanzado
            from ..services.vector_service import VectorSearchService
            
            vector_service = VectorSearchService(self.env)
            results = vector_service.search_knowledge_base(
                query=query,
                context=context or {},
                limit=limit,
                search_type='semantic'
            )
            
            # Extraer IDs de attachments de los resultados
            attachment_ids = [result['attachment_id'] for result in results if result.get('attachment_id')]
            
            # Retornar recordset ordenado por relevancia
            if attachment_ids:
                # Crear mapeo de ID a posición para mantener orden
                id_to_position = {aid: idx for idx, aid in enumerate(attachment_ids)}
                
                attachments = self.browse(attachment_ids)
                
                # Ordenar según el orden de relevancia de los resultados
                sorted_attachments = sorted(
                    attachments, 
                    key=lambda a: id_to_position.get(a.id, 999)
                )
                
                return self.browse([a.id for a in sorted_attachments])
            else:
                return self.browse([])
                
        except Exception as e:
            _logger.error(f"Error en búsqueda semántica: {e}")
            return self.browse([])
    
    def search_similar_hybrid(self, query: str, context: dict = None, limit: int = 10) -> dict:
        """
        Búsqueda híbrida (semántica + palabras clave) con información detallada.
        
        Args:
            query: Consulta de búsqueda
            context: Contexto de la conversación (opcional)
            limit: Número máximo de resultados
            
        Returns:
            Diccionario con resultados detallados y metadatos
        """
        
        try:
            # Usar el servicio RAG avanzado con búsqueda híbrida
            from ..services.vector_service import VectorSearchService
            
            vector_service = VectorSearchService(self.env)
            results = vector_service.search_knowledge_base(
                query=query,
                context=context or {},
                limit=limit,
                search_type='hybrid'
            )
            
            # Procesar resultados para incluir recordsets de Odoo
            processed_results = []
            attachment_ids = []
            
            for result in results:
                attachment_id = result.get('attachment_id')
                if attachment_id:
                    attachment_ids.append(attachment_id)
                    processed_results.append({
                        'attachment_id': attachment_id,
                        'content': result.get('content', ''),
                        'snippet': result.get('snippet', ''),
                        'similarity': result.get('similarity', 0.0),
                        'relevance_score': result.get('relevance_score', 0),
                        'document_type': result.get('document_type'),
                        'document_type_display': result.get('document_type_display'),
                        'document_name': result.get('document_name'),
                        'context_match': result.get('context_match', {}),
                        'scoring_factors': result.get('scoring_factors', {}),
                        'search_type': result.get('search_type', 'hybrid')
                    })
            
            # Obtener recordsets de attachments
            attachments = self.browse(attachment_ids) if attachment_ids else self.browse([])
            
            return {
                'attachments': attachments,
                'results': processed_results,
                'total_results': len(processed_results),
                'query': query,
                'context': context or {},
                'search_type': 'hybrid'
            }
            
        except Exception as e:
            _logger.error(f"Error en búsqueda híbrida: {e}")
            return {
                'attachments': self.browse([]),
                'results': [],
                'total_results': 0,
                'query': query,
                'context': context or {},
                'search_type': 'hybrid',
                'error': str(e)
            }
    
    @api.model
    def get_indexing_candidates(self, limit=50):
        """Obtiene documentos candidatos para indexación"""
        
        domain = [
            ('x_is_indexed', '=', False),
            ('raw', '!=', False),
            ('mimetype', 'in', [
                'application/pdf',
                'text/plain',
                'text/html',
                'image/jpeg',
                'image/png'
            ])
        ]
        
        # Ordenar por prioridad y fecha
        order = 'x_indexing_priority desc, create_date desc'
        
        candidates = self.search(domain, limit=limit, order=order)
        
        _logger.info(f"Encontrados {len(candidates)} documentos candidatos para indexación")
        
        return candidates
    
    def mark_indexing_complete(self, embedding_data=None):
        """Marca la indexación como completada"""
        self.ensure_one()
        
        values = {
            'x_is_indexed': True,
            'x_indexed_date': fields.Datetime.now(),
            'x_indexing_error': False
        }
        
        if embedding_data:
            values['x_embedding'] = embedding_data
        
        self.write(values)
        
        _logger.info(f"Indexación completada para documento: {self.name} (ID: {self.id})")
    
    def mark_indexing_error(self, error_message):
        """Marca error en la indexación"""
        self.ensure_one()
        
        self.write({
            'x_is_indexed': False,
            'x_indexing_error': error_message,
            'x_indexed_date': False
        })
        
        _logger.error(f"Error en indexación de documento {self.name} (ID: {self.id}): {error_message}")
    
    @api.model
    def get_rag_statistics(self):
        """Obtiene estadísticas de la base de conocimiento RAG"""
        
        total_docs = self.search_count([('raw', '!=', False)])
        indexed_docs = self.search_count([('x_is_indexed', '=', True)])
        pending_docs = self.search_count([
            ('x_is_indexed', '=', False),
            ('raw', '!=', False),
            ('mimetype', 'in', ['application/pdf', 'text/plain', 'text/html'])
        ])
        error_docs = self.search_count([('x_indexing_error', '!=', False)])
        
        # Estadísticas por tipo de documento
        doc_types = self.read_group(
            [('x_is_indexed', '=', True)],
            ['x_document_type'],
            ['x_document_type']
        )
        
        stats = {
            'total_documents': total_docs,
            'indexed_documents': indexed_docs,
            'pending_documents': pending_docs,
            'error_documents': error_docs,
            'indexing_percentage': (indexed_docs / total_docs * 100) if total_docs > 0 else 0,
            'document_types': {item['x_document_type']: item['x_document_type_count'] for item in doc_types}
        }
        
        return stats
    
    def action_view_rag_stats(self):
        """Acción para ver estadísticas RAG"""
        stats = self.get_rag_statistics()
        
        message = f"""
        📊 **Estadísticas de Base de Conocimiento RAG**
        
        - Total de documentos: {stats['total_documents']}
        - Documentos indexados: {stats['indexed_documents']}
        - Documentos pendientes: {stats['pending_documents']}
        - Documentos con error: {stats['error_documents']}
        - Porcentaje indexado: {stats['indexing_percentage']:.1f}%
        
        **Por tipo de documento:**
        {chr(10).join([f"- {k}: {v}" for k, v in stats['document_types'].items()])}
        """
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Estadísticas RAG',
                'message': message,
                'type': 'info',
                'sticky': True
            }
        }