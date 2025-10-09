#!/usr/bin/env python3
"""
Script de validación del servidor MCP
Valida el funcionamiento completo del servidor MCP y sus herramientas

Autor: PATCO - Automatización Industrial
Fecha: Enero 2025
Versión: 1.0
"""

import asyncio
import json
import logging
import os
import sys
import time
from typing import Dict, Any, List

import aiohttp
import psycopg2
from psycopg2.extras import RealDictCursor

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuración del servidor MCP
MCP_BASE_URL = os.getenv('MCP_BASE_URL', 'http://localhost:8080')
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', '5432')),
    'database': os.getenv('DB_NAME', 'odoo_patco'),
    'user': os.getenv('DB_USER', 'odoo'),
    'password': os.getenv('DB_PASSWORD', 'P4tc0_2')
}
ODOO_CONFIG = {
    'url': os.getenv('ODOO_URL', 'http://localhost:8069'),
    'db': os.getenv('ODOO_DB', 'odoo_patco'),
    'username': os.getenv('ODOO_USERNAME', 'admin'),
    'password': os.getenv('ODOO_PASSWORD', 'admin')
}

class MCPValidator:
    """Validador del servidor MCP"""
    
    def __init__(self):
        self.session = None
        self.db_conn = None
        self.validation_results = []
    
    async def __aenter__(self):
        """Inicializar recursos async"""
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Limpiar recursos async"""
        if self.session:
            await self.session.close()
        if self.db_conn:
            self.db_conn.close()
    
    def add_result(self, test_name: str, success: bool, message: str, details: Dict = None):
        """Agregar resultado de validación"""
        result = {
            'test': test_name,
            'success': success,
            'message': message,
            'timestamp': time.time(),
            'details': details or {}
        }
        self.validation_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        logger.info(f"{status} - {test_name}: {message}")
    
    async def validate_health_check(self) -> bool:
        """Validar health check del servidor"""
        try:
            async with self.session.get(f"{MCP_BASE_URL}/health") as response:
                if response.status == 200:
                    data = await response.json()
                    self.add_result(
                        "Health Check",
                        True,
                        "Servidor MCP respondiendo correctamente",
                        data
                    )
                    return True
                else:
                    self.add_result(
                        "Health Check",
                        False,
                        f"Servidor respondió con status {response.status}"
                    )
                    return False
        except Exception as e:
            self.add_result(
                "Health Check",
                False,
                f"Error conectando al servidor: {str(e)}"
            )
            return False
    
    async def validate_tools_list(self) -> bool:
        """Validar listado de herramientas MCP"""
        try:
            payload = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/list",
                "params": {}
            }
            
            async with self.session.post(
                f"{MCP_BASE_URL}/mcp",
                json=payload,
                headers={'Content-Type': 'application/json'}
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    if 'result' in data and 'tools' in data['result']:
                        tools = data['result']['tools']
                        expected_tools = [
                            'get_fsm_order',
                            'update_fsm_order',
                            'get_equipment_info',
                            'search_knowledge_base',
                            'create_ai_conversation',
                            'send_ai_message',
                            'get_ai_conversation'
                        ]
                        
                        found_tools = [tool['name'] for tool in tools]
                        missing_tools = set(expected_tools) - set(found_tools)
                        
                        if not missing_tools:
                            self.add_result(
                                "Tools List",
                                True,
                                f"Todas las herramientas disponibles ({len(tools)} herramientas)",
                                {'tools': found_tools}
                            )
                            return True
                        else:
                            self.add_result(
                                "Tools List",
                                False,
                                f"Herramientas faltantes: {list(missing_tools)}",
                                {'found': found_tools, 'missing': list(missing_tools)}
                            )
                            return False
                    else:
                        self.add_result(
                            "Tools List",
                            False,
                            "Respuesta no contiene lista de herramientas",
                            data
                        )
                        return False
                else:
                    self.add_result(
                        "Tools List",
                        False,
                        f"Error HTTP {response.status}"
                    )
                    return False
        except Exception as e:
            self.add_result(
                "Tools List",
                False,
                f"Error validando herramientas: {str(e)}"
            )
            return False
    
    def validate_database_connection(self) -> bool:
        """Validar conexión a la base de datos"""
        try:
            self.db_conn = psycopg2.connect(**DB_CONFIG)
            with self.db_conn.cursor(cursor_factory=RealDictCursor) as cursor:
                # Verificar PGVector
                cursor.execute("SELECT * FROM pg_available_extensions WHERE name = 'vector';")
                vector_ext = cursor.fetchone()
                
                if vector_ext:
                    self.add_result(
                        "Database Connection",
                        True,
                        "Conexión a PostgreSQL exitosa, PGVector disponible",
                        {'pgvector': dict(vector_ext)}
                    )
                    return True
                else:
                    self.add_result(
                        "Database Connection",
                        False,
                        "PGVector no está disponible"
                    )
                    return False
        except Exception as e:
            self.add_result(
                "Database Connection",
                False,
                f"Error conectando a la base de datos: {str(e)}"
            )
            return False
    
    async def validate_odoo_connection(self) -> bool:
        """Validar conexión a Odoo"""
        try:
            async with self.session.get(f"{ODOO_CONFIG['url']}/web/database/selector") as response:
                if response.status == 200:
                    self.add_result(
                        "Odoo Connection",
                        True,
                        "Conexión a Odoo exitosa"
                    )
                    return True
                else:
                    self.add_result(
                        "Odoo Connection",
                        False,
                        f"Odoo respondió con status {response.status}"
                    )
                    return False
        except Exception as e:
            self.add_result(
                "Odoo Connection",
                False,
                f"Error conectando a Odoo: {str(e)}"
            )
            return False
    
    async def validate_fsm_tools(self) -> bool:
        """Validar herramientas FSM"""
        try:
            # Test get_fsm_order
            payload = {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/call",
                "params": {
                    "name": "get_fsm_order",
                    "arguments": {
                        "order_id": 1
                    }
                }
            }
            
            async with self.session.post(
                f"{MCP_BASE_URL}/mcp",
                json=payload,
                headers={'Content-Type': 'application/json'}
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    if 'result' in data:
                        self.add_result(
                            "FSM Tools",
                            True,
                            "Herramientas FSM funcionando correctamente",
                            {'response': data['result']}
                        )
                        return True
                    else:
                        self.add_result(
                            "FSM Tools",
                            False,
                            "Respuesta no contiene resultado",
                            data
                        )
                        return False
                else:
                    self.add_result(
                        "FSM Tools",
                        False,
                        f"Error HTTP {response.status}"
                    )
                    return False
        except Exception as e:
            self.add_result(
                "FSM Tools",
                False,
                f"Error validando herramientas FSM: {str(e)}"
            )
            return False
    
    async def validate_knowledge_tools(self) -> bool:
        """Validar herramientas de conocimiento"""
        try:
            payload = {
                "jsonrpc": "2.0",
                "id": 3,
                "method": "tools/call",
                "params": {
                    "name": "search_knowledge_base",
                    "arguments": {
                        "query": "test query",
                        "limit": 5
                    }
                }
            }
            
            async with self.session.post(
                f"{MCP_BASE_URL}/mcp",
                json=payload,
                headers={'Content-Type': 'application/json'}
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    if 'result' in data:
                        self.add_result(
                            "Knowledge Tools",
                            True,
                            "Herramientas de conocimiento funcionando",
                            {'response': data['result']}
                        )
                        return True
                    else:
                        self.add_result(
                            "Knowledge Tools",
                            False,
                            "Respuesta no contiene resultado",
                            data
                        )
                        return False
                else:
                    self.add_result(
                        "Knowledge Tools",
                        False,
                        f"Error HTTP {response.status}"
                    )
                    return False
        except Exception as e:
            self.add_result(
                "Knowledge Tools",
                False,
                f"Error validando herramientas de conocimiento: {str(e)}"
            )
            return False
    
    def print_summary(self):
        """Imprimir resumen de validación"""
        print("\n" + "="*60)
        print("📋 RESUMEN DE VALIDACIÓN DEL SERVIDOR MCP")
        print("="*60)
        
        total_tests = len(self.validation_results)
        passed_tests = sum(1 for r in self.validation_results if r['success'])
        failed_tests = total_tests - passed_tests
        
        print(f"\n📊 Estadísticas:")
        print(f"   Total de pruebas: {total_tests}")
        print(f"   ✅ Exitosas: {passed_tests}")
        print(f"   ❌ Fallidas: {failed_tests}")
        print(f"   📈 Tasa de éxito: {(passed_tests/total_tests)*100:.1f}%")
        
        print(f"\n📝 Detalles de pruebas:")
        for result in self.validation_results:
            status = "✅" if result['success'] else "❌"
            print(f"   {status} {result['test']}: {result['message']}")
        
        if failed_tests == 0:
            print(f"\n🎉 ¡VALIDACIÓN EXITOSA!")
            print(f"   El servidor MCP está funcionando correctamente.")
            print(f"   Todas las herramientas están disponibles y operativas.")
        else:
            print(f"\n⚠️  VALIDACIÓN PARCIAL")
            print(f"   Algunas pruebas fallaron. Revisar la configuración.")
        
        print("\n" + "="*60)
    
    def save_report(self, filename: str = "mcp_validation_report.json"):
        """Guardar reporte de validación"""
        report = {
            'timestamp': time.time(),
            'mcp_url': MCP_BASE_URL,
            'total_tests': len(self.validation_results),
            'passed_tests': sum(1 for r in self.validation_results if r['success']),
            'failed_tests': sum(1 for r in self.validation_results if not r['success']),
            'results': self.validation_results
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Reporte guardado en: {filename}")

async def main():
    """Función principal de validación"""
    print("🚀 Iniciando validación del servidor MCP...")
    print(f"📍 URL del servidor: {MCP_BASE_URL}")
    
    async with MCPValidator() as validator:
        # Ejecutar validaciones
        await validator.validate_health_check()
        await validator.validate_tools_list()
        validator.validate_database_connection()
        await validator.validate_odoo_connection()
        await validator.validate_fsm_tools()
        await validator.validate_knowledge_tools()
        
        # Mostrar resumen
        validator.print_summary()
        validator.save_report()
        
        # Determinar código de salida
        failed_tests = sum(1 for r in validator.validation_results if not r['success'])
        return 0 if failed_tests == 0 else 1

if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n⏹️  Validación interrumpida por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Error fatal durante la validación: {str(e)}")
        sys.exit(1)