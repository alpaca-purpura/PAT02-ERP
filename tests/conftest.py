# -*- coding: utf-8 -*-
"""
Configuración compartida para tests de PATCO ERP

Este archivo contiene fixtures y configuraciones que se comparten
entre todos los tests del proyecto.
"""

import os
import sys
import pytest
import logging
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch

# Configurar logging para tests
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)

# Añadir directorios al path de Python
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / 'extra-addons'))

# Configuración de entorno para tests
os.environ.setdefault('ODOO_RC', str(project_root / 'config' / 'odoo.conf'))
os.environ.setdefault('RUNNING_TESTS', '1')
os.environ.setdefault('TEST_ENABLE', '1')

# ============================================================================
# FIXTURES DE CONFIGURACIÓN
# ============================================================================

@pytest.fixture(scope='session')
def project_root_path():
    """Path raíz del proyecto"""
    return project_root

@pytest.fixture(scope='session')
def test_config():
    """Configuración para tests"""
    return {
        'odoo_host': 'localhost',
        'odoo_port': 8069,
        'odoo_db': 'patco_test',
        'odoo_user': 'admin',
        'odoo_password': 'admin',
        'timeout': 30,
        'max_retries': 3
    }

@pytest.fixture(scope='session')
def temp_directory():
    """Directorio temporal para tests"""
    temp_dir = tempfile.mkdtemp(prefix='patco_test_')
    yield Path(temp_dir)
    shutil.rmtree(temp_dir, ignore_errors=True)

# ============================================================================
# FIXTURES DE ODOO
# ============================================================================

@pytest.fixture(scope='session')
def odoo_env():
    """Mock del entorno de Odoo para tests unitarios"""
    try:
        # Intentar importar Odoo real si está disponible
        import odoo
        from odoo import api, SUPERUSER_ID
        from odoo.tests.common import TransactionCase
        
        # Si Odoo está disponible, usar entorno real
        registry = odoo.registry('patco_test')
        with registry.cursor() as cr:
            env = api.Environment(cr, SUPERUSER_ID, {})
            yield env
    except ImportError:
        # Si Odoo no está disponible, usar mock
        mock_env = Mock()
        mock_env.user = Mock()
        mock_env.user.id = 1
        mock_env.user.name = 'Administrator'
        mock_env.company = Mock()
        mock_env.company.id = 1
        mock_env.company.name = 'Test Company'
        yield mock_env

@pytest.fixture
def odoo_registry():
    """Mock del registry de Odoo"""
    mock_registry = Mock()
    mock_registry.db_name = 'patco_test'
    return mock_registry

@pytest.fixture
def odoo_cursor():
    """Mock del cursor de base de datos"""
    mock_cursor = Mock()
    mock_cursor.execute = Mock()
    mock_cursor.fetchall = Mock(return_value=[])
    mock_cursor.fetchone = Mock(return_value=None)
    mock_cursor.commit = Mock()
    mock_cursor.rollback = Mock()
    return mock_cursor

# ============================================================================
# FIXTURES DE MÓDULOS PATCO
# ============================================================================

@pytest.fixture
def patco_modules():
    """Lista de módulos PATCO para tests"""
    return [
        'patco_core',
        'patco_suite', 
        'patco_customer_equipment',
        'patco_hr_skills',
        'patco_hr_fsm_integration'
    ]

@pytest.fixture
def patco_core_mock():
    """Mock del módulo patco_core"""
    mock_core = Mock()
    mock_core.name = 'patco_core'
    mock_core.version = '1.0.0'
    mock_core.depends = ['base', 'mail']
    return mock_core

@pytest.fixture
def patco_suite_mock():
    """Mock del módulo patco_suite"""
    mock_suite = Mock()
    mock_suite.name = 'patco_suite'
    mock_suite.version = '1.0.0'
    mock_suite.depends = ['patco_core']
    return mock_suite

# ============================================================================
# FIXTURES DE DATOS DE PRUEBA
# ============================================================================

@pytest.fixture
def sample_customer_data():
    """Datos de ejemplo para clientes"""
    return {
        'name': 'Test Customer',
        'email': 'test@customer.com',
        'phone': '+1234567890',
        'is_company': True,
        'customer_rank': 1
    }

@pytest.fixture
def sample_equipment_data():
    """Datos de ejemplo para equipos"""
    return {
        'name': 'Test Equipment',
        'model': 'TEST-001',
        'serial_number': 'SN123456',
        'category': 'Test Category',
        'status': 'active'
    }

@pytest.fixture
def sample_employee_data():
    """Datos de ejemplo para empleados"""
    return {
        'name': 'Test Employee',
        'email': 'test@employee.com',
        'department': 'Test Department',
        'job_title': 'Test Position'
    }

# ============================================================================
# FIXTURES DE UTILIDADES
# ============================================================================

@pytest.fixture
def mock_logger():
    """Logger mock para tests"""
    return Mock(spec=logging.Logger)

@pytest.fixture
def mock_requests():
    """Mock de requests para tests de API"""
    with patch('requests.get') as mock_get, \
         patch('requests.post') as mock_post, \
         patch('requests.put') as mock_put, \
         patch('requests.delete') as mock_delete:
        
        # Configurar respuestas por defecto
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'success': True}
        mock_response.text = 'OK'
        
        mock_get.return_value = mock_response
        mock_post.return_value = mock_response
        mock_put.return_value = mock_response
        mock_delete.return_value = mock_response
        
        yield {
            'get': mock_get,
            'post': mock_post,
            'put': mock_put,
            'delete': mock_delete,
            'response': mock_response
        }

@pytest.fixture
def database_transaction():
    """Fixture para transacciones de base de datos"""
    # En un entorno real, esto manejaría transacciones reales
    # Para tests, usamos un mock
    transaction = Mock()
    transaction.begin = Mock()
    transaction.commit = Mock()
    transaction.rollback = Mock()
    return transaction

# ============================================================================
# HOOKS DE PYTEST
# ============================================================================

def pytest_configure(config):
    """Configuración inicial de pytest"""
    # Registrar marcadores personalizados
    config.addinivalue_line(
        "markers", "compatibility: Tests de compatibilidad entre módulos"
    )
    config.addinivalue_line(
        "markers", "regression: Tests de regresión funcional"
    )
    config.addinivalue_line(
        "markers", "performance: Tests de rendimiento"
    )
    config.addinivalue_line(
        "markers", "critical: Tests críticos que deben pasar"
    )
    config.addinivalue_line(
        "markers", "slow: Tests que tardan más de 30 segundos"
    )

def pytest_collection_modifyitems(config, items):
    """Modificar items de la colección de tests"""
    # Marcar tests lentos automáticamente
    for item in items:
        if 'performance' in item.keywords:
            item.add_marker(pytest.mark.slow)
        
        # Marcar tests críticos
        if any(keyword in item.keywords for keyword in ['compatibility', 'regression']):
            item.add_marker(pytest.mark.critical)

def pytest_runtest_setup(item):
    """Setup antes de cada test"""
    # Configurar logging específico para cada test
    test_logger = logging.getLogger(item.name)
    test_logger.info(f"Iniciando test: {item.name}")

def pytest_runtest_teardown(item, nextitem):
    """Teardown después de cada test"""
    # Limpiar después de cada test
    test_logger = logging.getLogger(item.name)
    test_logger.info(f"Finalizando test: {item.name}")

def pytest_sessionstart(session):
    """Inicio de sesión de tests"""
    print("\n🚀 Iniciando sesión de tests PATCO ERP")
    print(f"📁 Directorio de trabajo: {project_root}")
    print(f"🐍 Python: {sys.version}")
    
def pytest_sessionfinish(session, exitstatus):
    """Final de sesión de tests"""
    if exitstatus == 0:
        print("\n✅ Sesión de tests completada exitosamente")
    else:
        print(f"\n❌ Sesión de tests falló con código: {exitstatus}")

# ============================================================================
# UTILIDADES PARA TESTS
# ============================================================================

class PatcoTestCase:
    """Clase base para tests de PATCO"""
    
    def setup_method(self, method):
        """Setup para cada método de test"""
        self.test_name = method.__name__
        self.logger = logging.getLogger(self.test_name)
        self.logger.info(f"Setup para {self.test_name}")
    
    def teardown_method(self, method):
        """Teardown para cada método de test"""
        self.logger.info(f"Teardown para {self.test_name}")
    
    def assert_module_exists(self, module_name):
        """Verificar que un módulo existe"""
        module_path = project_root / 'extra-addons' / module_name
        assert module_path.exists(), f"Módulo {module_name} no encontrado en {module_path}"
        
        manifest_path = module_path / '__manifest__.py'
        assert manifest_path.exists(), f"Manifest no encontrado para {module_name}"
    
    def assert_module_installable(self, module_name):
        """Verificar que un módulo es instalable"""
        self.assert_module_exists(module_name)
        
        manifest_path = project_root / 'extra-addons' / module_name / '__manifest__.py'
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest_content = f.read()
            
        # Verificar que no esté marcado como no instalable
        assert "'installable': False" not in manifest_content, f"Módulo {module_name} marcado como no instalable"

# Hacer disponible la clase base
__all__ = ['PatcoTestCase']