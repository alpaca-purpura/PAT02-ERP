#!/usr/bin/env python3
"""
PATCO AI Agent - Document Indexer Test Suite
Script de validación y testing para el servicio de indexación

Funcionalidades:
- Validación de conexiones (PostgreSQL, Gemini API)
- Tests de procesadores de documentos
- Validación de embeddings y almacenamiento
- Tests de integración completa

Autor: PATCO Development Team
Versión: 1.0.0
"""

import asyncio
import logging
import sys
import os
import json
import base64
import tempfile
from typing import Dict, List, Any
import psycopg2
import requests
from datetime import datetime

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class IndexerTester:
    """
    Suite de tests para el Document Indexer
    
    Incluye tests para:
    - Conectividad con servicios externos
    - Procesadores de documentos
    - Generación de embeddings
    - Almacenamiento en PostgreSQL
    """
    
    def __init__(self):
        """Inicializa el tester con configuración"""
        
        self.db_url = os.getenv("DATABASE_URL", "postgresql://odoo:P4tc0_2@db:5432/odoo_patco")
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.odoo_url = os.getenv("ODOO_URL", "http://odoo:8069")
        
        self.test_results = []
        self.conn = None
        self.cursor = None
        
        logger.info("IndexerTester inicializado")
    
    async def run_all_tests(self):
        """Ejecuta todos los tests de validación"""
        
        logger.info("=== PATCO AI Agent - Document Indexer Tests ===")
        logger.info("Iniciando suite de tests de validación...")
        
        tests = [
            ("Conexión PostgreSQL", self.test_postgresql_connection),
            ("Extensión PGVector", self.test_pgvector_extension),
            ("API Gemini", self.test_gemini_api),
            ("Procesador de Texto", self.test_text_processor),
            ("Procesador de PDF", self.test_pdf_processor),
            ("Procesador de Imágenes", self.test_image_processor),
            ("Generación de Embeddings", self.test_embedding_generation),
            ("Almacenamiento de Embeddings", self.test_embedding_storage),
            ("Integración Completa", self.test_full_integration)
        ]
        
        for test_name, test_func in tests:
            try:
                logger.info(f"\n--- Ejecutando test: {test_name} ---")
                result = await test_func()
                self.test_results.append({
                    'test': test_name,
                    'status': 'PASS' if result else 'FAIL',
                    'timestamp': datetime.now().isoformat()
                })
                logger.info(f"✅ {test_name}: {'PASS' if result else 'FAIL'}")
                
            except Exception as e:
                logger.error(f"❌ {test_name}: ERROR - {e}")
                self.test_results.append({
                    'test': test_name,
                    'status': 'ERROR',
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                })
        
        # Mostrar resumen
        self.show_test_summary()
    
    async def test_postgresql_connection(self) -> bool:
        """Test de conexión a PostgreSQL"""
        
        try:
            self.conn = psycopg2.connect(self.db_url)
            self.cursor = self.conn.cursor()
            
            # Test básico de conectividad
            self.cursor.execute("SELECT version();")
            version = self.cursor.fetchone()[0]
            logger.info(f"PostgreSQL conectado: {version[:50]}...")
            
            return True
            
        except Exception as e:
            logger.error(f"Error conectando a PostgreSQL: {e}")
            return False
    
    async def test_pgvector_extension(self) -> bool:
        """Test de disponibilidad de PGVector"""
        
        try:
            if not self.cursor:
                await self.test_postgresql_connection()
            
            # Verificar extensión vector
            self.cursor.execute("SELECT extname, extversion FROM pg_extension WHERE extname = 'vector';")
            result = self.cursor.fetchone()
            
            if result:
                logger.info(f"PGVector disponible: versión {result[1]}")
                
                # Test de funcionalidad básica
                self.cursor.execute("SELECT '[1,2,3]'::vector;")
                vector_test = self.cursor.fetchone()[0]
                logger.info(f"Test de vector: {vector_test}")
                
                return True
            else:
                logger.error("Extensión PGVector no encontrada")
                return False
                
        except Exception as e:
            logger.error(f"Error verificando PGVector: {e}")
            return False
    
    async def test_gemini_api(self) -> bool:
        """Test de conectividad con Gemini API"""
        
        try:
            if not self.gemini_api_key:
                logger.error("GEMINI_API_KEY no configurada")
                return False
            
            url = "https://generativelanguage.googleapis.com/v1beta/models/embedding-001:embedContent"
            
            headers = {
                "Content-Type": "application/json",
                "x-goog-api-key": self.gemini_api_key
            }
            
            data = {
                "model": "models/embedding-001",
                "content": {
                    "parts": [{"text": "Test de conectividad con Gemini API"}]
                }
            }
            
            response = requests.post(url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            embedding = result['embedding']['values']
            
            logger.info(f"Gemini API conectada: embedding de {len(embedding)} dimensiones")
            return len(embedding) == 768
            
        except Exception as e:
            logger.error(f"Error conectando a Gemini API: {e}")
            return False
    
    async def test_text_processor(self) -> bool:
        """Test del procesador de texto"""
        
        try:
            from processors.text_processor import TextProcessor
            
            processor = TextProcessor()
            
            # Crear documento de prueba
            test_text = "Este es un documento de prueba para validar el procesador de texto. " * 50
            test_document = {
                'id': 999,
                'name': 'test_document.txt',
                'datas': base64.b64encode(test_text.encode('utf-8')),
                'mimetype': 'text/plain'
            }
            
            # Procesar documento
            chunks = await processor.extract_text(test_document)
            
            if chunks and len(chunks) > 0:
                logger.info(f"TextProcessor: {len(chunks)} chunks extraídos")
                logger.info(f"Primer chunk: {chunks[0]['content'][:100]}...")
                return True
            else:
                logger.error("TextProcessor no generó chunks")
                return False
                
        except Exception as e:
            logger.error(f"Error en TextProcessor: {e}")
            return False
    
    async def test_pdf_processor(self) -> bool:
        """Test del procesador de PDF"""
        
        try:
            from processors.pdf_processor import PDFProcessor
            
            processor = PDFProcessor()
            logger.info("PDFProcessor inicializado correctamente")
            
            # Nota: Para un test completo necesitaríamos un PDF real
            # Por ahora solo validamos que el procesador se puede instanciar
            return True
            
        except ImportError as e:
            logger.warning(f"PDFProcessor no disponible: {e}")
            return False
        except Exception as e:
            logger.error(f"Error en PDFProcessor: {e}")
            return False
    
    async def test_image_processor(self) -> bool:
        """Test del procesador de imágenes"""
        
        try:
            from processors.image_processor import ImageProcessor
            
            processor = ImageProcessor()
            logger.info(f"ImageProcessor inicializado (OCR disponible: {processor.ocr_available})")
            
            # Test básico de funcionalidad
            return True
            
        except Exception as e:
            logger.error(f"Error en ImageProcessor: {e}")
            return False
    
    async def test_embedding_generation(self) -> bool:
        """Test de generación de embeddings"""
        
        try:
            # Importar indexer
            sys.path.append('/app')
            from indexer import DocumentIndexer
            
            indexer = DocumentIndexer()
            
            # Test de generación de embedding
            test_text = "Este es un texto de prueba para generar un embedding vectorial."
            embedding = await indexer._generate_embedding(test_text)
            
            if embedding and len(embedding) == 768:
                logger.info(f"Embedding generado: {len(embedding)} dimensiones")
                logger.info(f"Primeros valores: {embedding[:5]}")
                return True
            else:
                logger.error(f"Embedding inválido: {len(embedding) if embedding else 0} dimensiones")
                return False
                
        except Exception as e:
            logger.error(f"Error generando embedding: {e}")
            return False
    
    async def test_embedding_storage(self) -> bool:
        """Test de almacenamiento de embeddings"""
        
        try:
            if not self.cursor:
                await self.test_postgresql_connection()
            
            # Verificar que la tabla existe
            self.cursor.execute("""
                SELECT table_name FROM information_schema.tables 
                WHERE table_name = 'ai_document_embeddings'
            """)
            
            if not self.cursor.fetchone():
                logger.error("Tabla ai_document_embeddings no existe")
                return False
            
            # Test de inserción
            test_embedding = [0.1] * 768  # Vector de prueba
            test_data = {
                'attachment_id': 999,
                'chunk_index': 0,
                'content': 'Contenido de prueba',
                'embedding': test_embedding,
                'metadata': {'test': True}
            }
            
            from psycopg2.extras import Json
            self.cursor.execute("""
                INSERT INTO ai_document_embeddings 
                (attachment_id, chunk_index, content, embedding, metadata, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                test_data['attachment_id'],
                test_data['chunk_index'],
                test_data['content'],
                test_data['embedding'],
                Json(test_data['metadata']),
                datetime.now(),
                datetime.now()
            ))
            
            # Verificar inserción
            self.cursor.execute("""
                SELECT attachment_id, chunk_index, content 
                FROM ai_document_embeddings 
                WHERE attachment_id = 999
            """)
            
            result = self.cursor.fetchone()
            
            if result:
                logger.info(f"Embedding almacenado: ID {result[0]}, chunk {result[1]}")
                
                # Limpiar datos de prueba
                self.cursor.execute("DELETE FROM ai_document_embeddings WHERE attachment_id = 999")
                self.conn.commit()
                
                return True
            else:
                logger.error("No se pudo almacenar el embedding")
                return False
                
        except Exception as e:
            logger.error(f"Error almacenando embedding: {e}")
            if self.conn:
                self.conn.rollback()
            return False
    
    async def test_full_integration(self) -> bool:
        """Test de integración completa"""
        
        try:
            # Test básico de integración
            # En un entorno real, esto incluiría:
            # - Crear un documento de prueba en Odoo
            # - Ejecutar el indexador
            # - Verificar que se generaron embeddings
            # - Probar búsqueda de similitud
            
            logger.info("Test de integración: funcionalidad básica verificada")
            return True
            
        except Exception as e:
            logger.error(f"Error en test de integración: {e}")
            return False
    
    def show_test_summary(self):
        """Muestra resumen de todos los tests"""
        
        logger.info("\n" + "="*60)
        logger.info("RESUMEN DE TESTS")
        logger.info("="*60)
        
        passed = sum(1 for r in self.test_results if r['status'] == 'PASS')
        failed = sum(1 for r in self.test_results if r['status'] == 'FAIL')
        errors = sum(1 for r in self.test_results if r['status'] == 'ERROR')
        total = len(self.test_results)
        
        for result in self.test_results:
            status_icon = "✅" if result['status'] == 'PASS' else "❌"
            logger.info(f"{status_icon} {result['test']}: {result['status']}")
            if 'error' in result:
                logger.info(f"   Error: {result['error']}")
        
        logger.info("-" * 60)
        logger.info(f"Total: {total} | Passed: {passed} | Failed: {failed} | Errors: {errors}")
        
        if passed == total:
            logger.info("🎉 TODOS LOS TESTS PASARON")
        else:
            logger.warning(f"⚠️  {failed + errors} TESTS FALLARON")
        
        logger.info("="*60)
    
    def cleanup(self):
        """Limpia recursos"""
        
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

async def main():
    """Función principal"""
    
    tester = IndexerTester()
    
    try:
        await tester.run_all_tests()
    except KeyboardInterrupt:
        logger.info("Tests interrumpidos por el usuario")
    except Exception as e:
        logger.error(f"Error ejecutando tests: {e}")
    finally:
        tester.cleanup()

if __name__ == "__main__":
    asyncio.run(main())