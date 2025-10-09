# -*- coding: utf-8 -*-
"""
PATCO AI Agent - Vector Search Service
Servicio RAG avanzado con filtros contextuales para búsqueda semántica

Implementa la Fase 7: RAG y Búsqueda Semántica del plan de implementación
con optimizaciones de relevancia y filtros por contexto.

Autor: PATCO Development Team
Versión: 1.0.0
Fecha: Enero 2025
"""

import logging
import psycopg2
import numpy as np
import requests
import json
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import os

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class VectorSearchService:
    """Servicio avanzado de búsqueda vectorial con filtros contextuales"""
    
    def __init__(self, env):
        """
        Inicializa el servicio de búsqueda vectorial.
        
        Args:
            env: Entorno de Odoo
        """
        self.env = env
        self._logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        
        # Configuración desde parámetros del sistema
        self.gemini_api_key = self.env['ir.config_parameter'].sudo().get_param(
            'patco_ai_agent.gemini_api_key'
        )
        self.similarity_threshold = float(self.env['ir.config_parameter'].sudo().get_param(
            'patco_ai_agent.similarity_threshold', '0.7'
        ))
        self.max_search_results = int(self.env['ir.config_parameter'].sudo().get_param(
            'patco_ai_agent.max_search_results', '10'
        ))
        self.embedding_model = self.env['ir.config_parameter'].sudo().get_param(
            'patco_ai_agent.embedding_model', 'text-embedding-004'
        )
        
        # Configuración de base de datos
        self.db_config = {
            'host': os.environ.get('DB_HOST', 'localhost'),
            'port': int(os.environ.get('DB_PORT', '5432')),
            'database': os.environ.get('DB_NAME', 'odoo_patco'),
            'user': os.environ.get('DB_USER', 'odoo'),
            'password': os.environ.get('DB_PASSWORD', 'P4tc0_2')
        }
    
    def search_knowledge_base(
        self, 
        query: str, 
        context: Dict[str, Any] = None,
        limit: int = None,
        similarity_threshold: float = None,
        search_type: str = 'semantic'
    ) -> List[Dict[str, Any]]:
        """
        Búsqueda semántica avanzada en base de conocimiento con filtros contextuales.
        
        Args:
            query: Consulta de búsqueda
            context: Contexto de la conversación (FSM order, equipment, etc.)
            limit: Número máximo de resultados
            similarity_threshold: Umbral de similitud mínimo
            search_type: Tipo de búsqueda ('semantic', 'keyword', 'hybrid')
            
        Returns:
            Lista de resultados con scoring avanzado
        """
        
        try:
            self._logger.info(f"🔍 Búsqueda RAG: '{query}' (tipo: {search_type})")
            
            # Usar valores por defecto si no se especifican
            limit = limit or self.max_search_results
            similarity_threshold = similarity_threshold or self.similarity_threshold
            context = context or {}
            
            # Validar configuración
            if not self.gemini_api_key:
                raise UserError(_("Clave API de Gemini no configurada"))
            
            # Realizar búsqueda según el tipo
            if search_type == 'semantic':
                results = self._semantic_search(query, context, limit, similarity_threshold)
            elif search_type == 'keyword':
                results = self._keyword_search(query, context, limit)
            elif search_type == 'hybrid':
                results = self._hybrid_search(query, context, limit, similarity_threshold)
            else:
                raise ValidationError(_("Tipo de búsqueda no válido: %s") % search_type)
            
            # Aplicar scoring avanzado
            scored_results = self._apply_advanced_scoring(results, query, context)
            
            # Enriquecer con metadatos
            enriched_results = self._enrich_results(scored_results, context)
            
            self._logger.info(f"✅ Búsqueda completada: {len(enriched_results)} resultados")
            
            return enriched_results
            
        except Exception as e:
            self._logger.error(f"❌ Error en búsqueda RAG: {e}")
            return []
    
    def _semantic_search(
        self, 
        query: str, 
        context: Dict[str, Any], 
        limit: int, 
        similarity_threshold: float
    ) -> List[Dict[str, Any]]:
        """Búsqueda semántica usando embeddings vectoriales"""
        
        try:
            # Generar embedding de la consulta
            query_embedding = self._generate_embedding(query)
            if not query_embedding:
                return []
            
            # Construir filtros contextuales
            filters = self._build_context_filters(context)
            
            # Ejecutar búsqueda vectorial
            results = self._execute_vector_search(
                query_embedding, 
                filters, 
                limit, 
                similarity_threshold
            )
            
            return results
            
        except Exception as e:
            self._logger.error(f"Error en búsqueda semántica: {e}")
            return []
    
    def _keyword_search(
        self, 
        query: str, 
        context: Dict[str, Any], 
        limit: int
    ) -> List[Dict[str, Any]]:
        """Búsqueda por palabras clave con filtros contextuales"""
        
        try:
            # Extraer palabras clave
            keywords = self._extract_keywords(query)
            if not keywords:
                return []
            
            # Construir filtros contextuales
            filters = self._build_context_filters(context)
            
            # Ejecutar búsqueda por texto
            results = self._execute_text_search(keywords, filters, limit)
            
            return results
            
        except Exception as e:
            self._logger.error(f"Error en búsqueda por palabras clave: {e}")
            return []
    
    def _hybrid_search(
        self, 
        query: str, 
        context: Dict[str, Any], 
        limit: int, 
        similarity_threshold: float
    ) -> List[Dict[str, Any]]:
        """Búsqueda híbrida combinando semántica y palabras clave"""
        
        try:
            # Búsqueda semántica (70% de los resultados)
            semantic_limit = int(limit * 0.7)
            semantic_results = self._semantic_search(
                query, context, semantic_limit, similarity_threshold
            )
            
            # Búsqueda por palabras clave (30% de los resultados)
            keyword_limit = limit - len(semantic_results)
            keyword_results = self._keyword_search(query, context, keyword_limit)
            
            # Combinar y deduplicar resultados
            combined_results = self._merge_search_results(
                semantic_results, keyword_results, limit
            )
            
            return combined_results
            
        except Exception as e:
            self._logger.error(f"Error en búsqueda híbrida: {e}")
            return []
    
    def _generate_embedding(self, text: str) -> List[float]:
        """Genera embedding usando Gemini API"""
        
        try:
            url = "https://generativelanguage.googleapis.com/v1beta/models/embedding-001:embedContent"
            
            headers = {
                "Content-Type": "application/json",
                "x-goog-api-key": self.gemini_api_key
            }
            
            data = {
                "model": "models/embedding-001",
                "content": {"parts": [{"text": text}]},
                "task_type": "retrieval_query"
            }
            
            response = requests.post(url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            embedding = result['embedding']['values']
            
            # Validar dimensión del embedding
            if len(embedding) != 768:
                raise ValueError(f"Dimensión de embedding incorrecta: {len(embedding)} != 768")
            
            return embedding
            
        except Exception as e:
            self._logger.error(f"Error generando embedding: {e}")
            return []
    
    def _build_context_filters(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Construye filtros basados en contexto de la conversación"""
        
        filters = {}
        
        # Filtro por categoría de equipo
        if context.get('equipment_category_id'):
            filters['equipment_category_id'] = context['equipment_category_id']
        elif context.get('equipment_ids'):
            # Obtener categorías de los equipos
            equipment_ids = context['equipment_ids']
            equipments = self.env['maintenance.equipment'].browse(equipment_ids)
            category_ids = equipments.mapped('category_id.id')
            if category_ids:
                filters['equipment_category_ids'] = category_ids
        
        # Filtro por naturaleza de servicio
        if context.get('service_nature_id'):
            filters['service_nature_id'] = context['service_nature_id']
        
        # Filtro por área de servicio
        if context.get('service_area_id'):
            filters['service_area_id'] = context['service_area_id']
        
        # Filtro por complejidad de servicio
        if context.get('service_complexity_id'):
            filters['service_complexity_id'] = context['service_complexity_id']
        
        # Filtro por tipo de documento según contexto
        document_types = self._determine_document_types_by_context(context)
        if document_types:
            filters['document_types'] = document_types
        
        # Filtro temporal (documentos recientes tienen mayor relevancia)
        filters['boost_recent'] = True
        
        return filters
    
    def _determine_document_types_by_context(self, context: Dict[str, Any]) -> List[str]:
        """Determina tipos de documentos relevantes según el contexto"""
        
        document_types = []
        
        # Si hay información de orden FSM, priorizar según el estado
        fsm_state = context.get('fsm_state')
        if fsm_state:
            if fsm_state in ['new', 'assigned']:
                # Al inicio: manuales y procedimientos
                document_types.extend(['manual', 'procedure'])
            elif fsm_state in ['in_progress']:
                # Durante trabajo: procedimientos y checklists
                document_types.extend(['procedure', 'checklist'])
            elif fsm_state in ['done', 'completed']:
                # Al final: reportes y checklists de salida
                document_types.extend(['checklist', 'report'])
        
        # Si hay información de equipo, incluir manuales técnicos
        if context.get('equipment_ids') or context.get('equipment_category_id'):
            if 'manual' not in document_types:
                document_types.append('manual')
        
        # Por defecto, incluir los tipos más comunes
        if not document_types:
            document_types = ['manual', 'procedure', 'checklist']
        
        return document_types
    
    def _execute_vector_search(
        self, 
        query_embedding: List[float], 
        filters: Dict[str, Any],
        limit: int,
        similarity_threshold: float
    ) -> List[Dict[str, Any]]:
        """Ejecuta búsqueda vectorial en PostgreSQL con PGVector"""
        
        conn = None
        try:
            # Conectar a PostgreSQL
            conn = psycopg2.connect(**self.db_config)
            cursor = conn.cursor()
            
            # Query base con similitud coseno
            query = """
            SELECT 
                e.attachment_id,
                e.chunk_index,
                e.content,
                e.metadata,
                1 - (e.embedding <=> %s::vector) as similarity,
                a.name as document_name,
                a.x_document_type,
                a.create_date,
                a.x_equipment_category_ids,
                a.x_service_nature_ids
            FROM ai_document_embeddings e
            JOIN ir_attachment a ON e.attachment_id = a.id
            WHERE 1 - (e.embedding <=> %s::vector) > %s
            """
            
            params = [query_embedding, query_embedding, similarity_threshold]
            
            # Aplicar filtros contextuales
            if filters.get('equipment_category_id'):
                query += " AND a.x_equipment_category_ids @> %s"
                params.append(json.dumps([filters['equipment_category_id']]))
            
            if filters.get('equipment_category_ids'):
                query += " AND a.x_equipment_category_ids && %s"
                params.append(json.dumps(filters['equipment_category_ids']))
            
            if filters.get('service_nature_id'):
                query += " AND a.x_service_nature_ids @> %s"
                params.append(json.dumps([filters['service_nature_id']]))
            
            if filters.get('document_types'):
                placeholders = ','.join(['%s'] * len(filters['document_types']))
                query += f" AND a.x_document_type IN ({placeholders})"
                params.extend(filters['document_types'])
            
            # Ordenar por similitud y limitar
            query += " ORDER BY e.embedding <=> %s::vector LIMIT %s"
            params.extend([query_embedding, limit])
            
            cursor.execute(query, params)
            results = cursor.fetchall()
            
            # Convertir a diccionarios
            documents = []
            for row in results:
                documents.append({
                    'attachment_id': row[0],
                    'chunk_index': row[1],
                    'content': row[2],
                    'metadata': row[3] or {},
                    'similarity': float(row[4]),
                    'document_name': row[5],
                    'document_type': row[6],
                    'create_date': row[7],
                    'equipment_category_ids': row[8] or [],
                    'service_nature_ids': row[9] or []
                })
            
            return documents
            
        except Exception as e:
            self._logger.error(f"Error en búsqueda vectorial: {e}")
            return []
        finally:
            if conn:
                conn.close()
    
    def _execute_text_search(
        self, 
        keywords: List[str], 
        filters: Dict[str, Any], 
        limit: int
    ) -> List[Dict[str, Any]]:
        """Ejecuta búsqueda por texto usando PostgreSQL full-text search"""
        
        conn = None
        try:
            # Conectar a PostgreSQL
            conn = psycopg2.connect(**self.db_config)
            cursor = conn.cursor()
            
            # Construir query de texto completo
            search_query = ' & '.join(keywords)
            
            query = """
            SELECT 
                e.attachment_id,
                e.chunk_index,
                e.content,
                e.metadata,
                ts_rank(to_tsvector('spanish', e.content), to_tsquery('spanish', %s)) as rank,
                a.name as document_name,
                a.x_document_type,
                a.create_date,
                a.x_equipment_category_ids,
                a.x_service_nature_ids
            FROM ai_document_embeddings e
            JOIN ir_attachment a ON e.attachment_id = a.id
            WHERE to_tsvector('spanish', e.content) @@ to_tsquery('spanish', %s)
            """
            
            params = [search_query, search_query]
            
            # Aplicar filtros contextuales (similar a búsqueda vectorial)
            if filters.get('equipment_category_id'):
                query += " AND a.x_equipment_category_ids @> %s"
                params.append(json.dumps([filters['equipment_category_id']]))
            
            if filters.get('document_types'):
                placeholders = ','.join(['%s'] * len(filters['document_types']))
                query += f" AND a.x_document_type IN ({placeholders})"
                params.extend(filters['document_types'])
            
            # Ordenar por ranking y limitar
            query += " ORDER BY rank DESC LIMIT %s"
            params.append(limit)
            
            cursor.execute(query, params)
            results = cursor.fetchall()
            
            # Convertir a diccionarios
            documents = []
            for row in results:
                documents.append({
                    'attachment_id': row[0],
                    'chunk_index': row[1],
                    'content': row[2],
                    'metadata': row[3] or {},
                    'similarity': float(row[4]),  # Usar rank como similarity
                    'document_name': row[5],
                    'document_type': row[6],
                    'create_date': row[7],
                    'equipment_category_ids': row[8] or [],
                    'service_nature_ids': row[9] or []
                })
            
            return documents
            
        except Exception as e:
            self._logger.error(f"Error en búsqueda por texto: {e}")
            return []
        finally:
            if conn:
                conn.close()
    
    def _extract_keywords(self, query: str) -> List[str]:
        """Extrae palabras clave relevantes de la consulta"""
        
        import re
        
        # Limpiar y normalizar texto
        query = query.lower().strip()
        
        # Remover palabras vacías en español
        stop_words = {
            'el', 'la', 'de', 'que', 'y', 'a', 'en', 'un', 'es', 'se', 'no', 'te', 'lo', 'le',
            'da', 'su', 'por', 'son', 'con', 'para', 'al', 'del', 'los', 'las', 'una', 'como',
            'qué', 'cómo', 'cuál', 'dónde', 'cuándo', 'por qué', 'porque'
        }
        
        # Extraer palabras (solo letras, mínimo 3 caracteres)
        words = re.findall(r'\b[a-záéíóúñ]{3,}\b', query)
        
        # Filtrar palabras vacías
        keywords = [word for word in words if word not in stop_words]
        
        return keywords[:10]  # Máximo 10 palabras clave
    
    def _merge_search_results(
        self, 
        semantic_results: List[Dict[str, Any]], 
        keyword_results: List[Dict[str, Any]], 
        limit: int
    ) -> List[Dict[str, Any]]:
        """Combina y deduplicar resultados de búsqueda semántica y por palabras clave"""
        
        # Crear diccionario para deduplicar por attachment_id + chunk_index
        merged_results = {}
        
        # Agregar resultados semánticos con peso mayor
        for result in semantic_results:
            key = f"{result['attachment_id']}_{result['chunk_index']}"
            # Dar mayor peso a resultados semánticos
            result['similarity'] *= 1.2
            result['search_type'] = 'semantic'
            merged_results[key] = result
        
        # Agregar resultados de palabras clave
        for result in keyword_results:
            key = f"{result['attachment_id']}_{result['chunk_index']}"
            if key not in merged_results:
                result['search_type'] = 'keyword'
                merged_results[key] = result
            else:
                # Si ya existe, combinar scores
                existing = merged_results[key]
                existing['similarity'] = (existing['similarity'] + result['similarity']) / 2
                existing['search_type'] = 'hybrid'
        
        # Convertir a lista y ordenar por similitud
        final_results = list(merged_results.values())
        final_results.sort(key=lambda x: x['similarity'], reverse=True)
        
        return final_results[:limit]
    
    def _apply_advanced_scoring(
        self, 
        results: List[Dict[str, Any]], 
        query: str, 
        context: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Aplica scoring avanzado considerando múltiples factores"""
        
        for result in results:
            base_score = result['similarity']
            
            # Factor 1: Relevancia por tipo de documento
            doc_type_boost = self._get_document_type_boost(
                result['document_type'], context
            )
            
            # Factor 2: Recencia del documento
            recency_boost = self._get_recency_boost(result['create_date'])
            
            # Factor 3: Coincidencia de categorías
            category_boost = self._get_category_boost(result, context)
            
            # Factor 4: Longitud del contenido (contenido más largo puede ser más completo)
            content_boost = self._get_content_length_boost(result['content'])
            
            # Calcular score final
            final_score = base_score * (1 + doc_type_boost + recency_boost + category_boost + content_boost)
            
            result['final_score'] = final_score
            result['scoring_factors'] = {
                'base_score': base_score,
                'doc_type_boost': doc_type_boost,
                'recency_boost': recency_boost,
                'category_boost': category_boost,
                'content_boost': content_boost
            }
        
        # Reordenar por score final
        results.sort(key=lambda x: x['final_score'], reverse=True)
        
        return results
    
    def _get_document_type_boost(self, doc_type: str, context: Dict[str, Any]) -> float:
        """Calcula boost basado en tipo de documento y contexto"""
        
        # Mapeo de tipos de documento a boost base
        type_boosts = {
            'manual': 0.2,
            'procedure': 0.3,
            'checklist': 0.25,
            'report': 0.1,
            'image': 0.15,
            'video': 0.1
        }
        
        base_boost = type_boosts.get(doc_type, 0.0)
        
        # Boost adicional según contexto FSM
        fsm_state = context.get('fsm_state')
        if fsm_state and doc_type:
            if fsm_state in ['new', 'assigned'] and doc_type == 'manual':
                base_boost += 0.1
            elif fsm_state == 'in_progress' and doc_type == 'procedure':
                base_boost += 0.15
            elif fsm_state in ['done', 'completed'] and doc_type == 'checklist':
                base_boost += 0.1
        
        return base_boost
    
    def _get_recency_boost(self, create_date) -> float:
        """Calcula boost basado en la recencia del documento"""
        
        if not create_date:
            return 0.0
        
        try:
            if isinstance(create_date, str):
                create_date = datetime.fromisoformat(create_date.replace('Z', '+00:00'))
            
            days_old = (datetime.now() - create_date.replace(tzinfo=None)).days
            
            # Documentos más recientes tienen mayor boost
            if days_old <= 30:
                return 0.1
            elif days_old <= 90:
                return 0.05
            elif days_old <= 365:
                return 0.02
            else:
                return 0.0
                
        except Exception:
            return 0.0
    
    def _get_category_boost(self, result: Dict[str, Any], context: Dict[str, Any]) -> float:
        """Calcula boost basado en coincidencia de categorías"""
        
        boost = 0.0
        
        # Boost por categoría de equipo
        result_categories = result.get('equipment_category_ids', [])
        context_category = context.get('equipment_category_id')
        context_categories = context.get('equipment_category_ids', [])
        
        if context_category and context_category in result_categories:
            boost += 0.15
        elif context_categories:
            # Calcular intersección
            intersection = set(result_categories) & set(context_categories)
            if intersection:
                boost += 0.1 * (len(intersection) / len(context_categories))
        
        # Boost por naturaleza de servicio
        result_natures = result.get('service_nature_ids', [])
        context_nature = context.get('service_nature_id')
        
        if context_nature and context_nature in result_natures:
            boost += 0.1
        
        return boost
    
    def _get_content_length_boost(self, content: str) -> float:
        """Calcula boost basado en la longitud del contenido"""
        
        if not content:
            return 0.0
        
        length = len(content)
        
        # Contenido de longitud media tiene mejor boost
        if 200 <= length <= 1000:
            return 0.05
        elif 100 <= length <= 2000:
            return 0.02
        else:
            return 0.0
    
    def _enrich_results(
        self, 
        results: List[Dict[str, Any]], 
        context: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Enriquece resultados con información adicional y metadatos"""
        
        for result in results:
            # Agregar snippet destacado
            content = result['content']
            if len(content) > 300:
                result['snippet'] = content[:300] + "..."
            else:
                result['snippet'] = content
            
            # Agregar score de relevancia (0-100)
            result['relevance_score'] = min(int(result.get('final_score', result['similarity']) * 100), 100)
            
            # Agregar tipo de documento legible
            doc_type_map = {
                'manual': 'Manual Técnico',
                'procedure': 'Procedimiento',
                'checklist': 'Lista de Verificación',
                'report': 'Reporte',
                'image': 'Imagen Técnica',
                'video': 'Video Instructivo'
            }
            result['document_type_display'] = doc_type_map.get(
                result['document_type'], 
                result['document_type']
            )
            
            # Agregar información de contexto
            result['context_match'] = self._calculate_context_match(result, context)
            
            # Agregar timestamp de búsqueda
            result['search_timestamp'] = datetime.now().isoformat()
        
        return results
    
    def _calculate_context_match(self, result: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Calcula qué tan bien coincide el resultado con el contexto"""
        
        match_info = {
            'equipment_category_match': False,
            'service_nature_match': False,
            'document_type_relevant': False,
            'overall_match_score': 0.0
        }
        
        # Verificar coincidencia de categoría de equipo
        result_categories = result.get('equipment_category_ids', [])
        context_category = context.get('equipment_category_id')
        if context_category and context_category in result_categories:
            match_info['equipment_category_match'] = True
            match_info['overall_match_score'] += 0.4
        
        # Verificar coincidencia de naturaleza de servicio
        result_natures = result.get('service_nature_ids', [])
        context_nature = context.get('service_nature_id')
        if context_nature and context_nature in result_natures:
            match_info['service_nature_match'] = True
            match_info['overall_match_score'] += 0.3
        
        # Verificar relevancia del tipo de documento
        doc_type = result['document_type']
        relevant_types = self._determine_document_types_by_context(context)
        if doc_type in relevant_types:
            match_info['document_type_relevant'] = True
            match_info['overall_match_score'] += 0.3
        
        return match_info


class VectorSearchMixin(models.AbstractModel):
    """Mixin para agregar capacidades de búsqueda vectorial a modelos"""
    
    _name = 'vector.search.mixin'
    _description = 'Vector Search Mixin'
    
    def get_vector_service(self):
        """Obtiene instancia del servicio de búsqueda vectorial"""
        return VectorSearchService(self.env)
    
    def search_knowledge_base(self, query, context=None, **kwargs):
        """Método de conveniencia para búsqueda en base de conocimiento"""
        service = self.get_vector_service()
        return service.search_knowledge_base(query, context, **kwargs)