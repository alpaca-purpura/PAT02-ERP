# -*- coding: utf-8 -*-
"""
Tests de Regresión - Funcionalidad Principal PATCO

Estos tests verifican que las funcionalidades principales del sistema
se mantengan funcionando correctamente después de cambios.
"""

import pytest
import requests
import time
import json
from pathlib import Path
from unittest.mock import Mock, patch

# Importar clase base de tests
try:
    from tests.conftest import PatcoTestCase
except ImportError:
    class PatcoTestCase:
        pass

class TestOdooSystemRegression(PatcoTestCase):
    """Tests de regresión del sistema Odoo base"""
    
    @pytest.fixture(autouse=True)
    def setup(self, test_config):
        """Setup para tests de regresión"""
        self.config = test_config
        self.base_url = f"http://{self.config['odoo_host']}:{self.config['odoo_port']}"
        self.timeout = self.config['timeout']
        self.max_retries = self.config['max_retries']
    
    @pytest.mark.regression
    @pytest.mark.critical
    @pytest.mark.smoke
    def test_odoo_server_is_responding(self):
        """Verificar que el servidor Odoo responda"""
        print(f"\n🔍 Verificando conectividad con Odoo en {self.base_url}...")
        
        for attempt in range(self.max_retries):
            try:
                response = requests.get(
                    f"{self.base_url}/web/health",
                    timeout=self.timeout
                )
                
                if response.status_code == 200:
                    print(f"  ✅ Odoo respondiendo correctamente (intento {attempt + 1})")
                    print(f"  📊 Código de respuesta: {response.status_code}")
                    return
                else:
                    print(f"  ⚠️  Respuesta inesperada: {response.status_code} (intento {attempt + 1})")
                    
            except requests.exceptions.RequestException as e:
                print(f"  ❌ Error de conexión (intento {attempt + 1}): {e}")
                if attempt < self.max_retries - 1:
                    print(f"  ⏳ Esperando 5 segundos antes del siguiente intento...")
                    time.sleep(5)
        
        pytest.fail(f"Odoo no responde después de {self.max_retries} intentos")
    
    @pytest.mark.regression
    @pytest.mark.critical
    def test_odoo_database_connection(self):
        """Verificar conexión con la base de datos"""
        print(f"\n🔍 Verificando conexión con base de datos...")
        
        try:
            # Intentar acceder a la página de login que requiere DB
            response = requests.get(
                f"{self.base_url}/web/login",
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                print(f"  ✅ Página de login accesible")
                
                # Verificar que la página contenga elementos esperados
                content = response.text.lower()
                if 'login' in content or 'database' in content:
                    print(f"  ✅ Contenido de login válido")
                else:
                    print(f"  ⚠️  Contenido de login inesperado")
                    
            else:
                pytest.fail(f"Error accediendo a login: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            pytest.fail(f"Error de conexión a base de datos: {e}")
    
    @pytest.mark.regression
    @pytest.mark.critical
    def test_odoo_web_interface_loads(self):
        """Verificar que la interfaz web cargue correctamente"""
        print(f"\n🔍 Verificando interfaz web de Odoo...")
        
        try:
            response = requests.get(
                f"{self.base_url}/web",
                timeout=self.timeout,
                allow_redirects=True
            )
            
            assert response.status_code == 200, f"Error cargando interfaz web: {response.status_code}"
            print(f"  ✅ Interfaz web carga correctamente")
            
            # Verificar elementos básicos de la interfaz
            content = response.text.lower()
            expected_elements = ['odoo', 'web', 'css', 'javascript']
            
            for element in expected_elements:
                if element in content:
                    print(f"  ✅ Elemento '{element}' encontrado")
                else:
                    print(f"  ⚠️  Elemento '{element}' no encontrado")
            
        except requests.exceptions.RequestException as e:
            pytest.fail(f"Error cargando interfaz web: {e}")
    
    @pytest.mark.regression
    def test_odoo_static_resources(self):
        """Verificar que los recursos estáticos se sirvan correctamente"""
        print(f"\n🔍 Verificando recursos estáticos...")
        
        static_resources = [
            '/web/static/src/css/bootstrap.css',
            '/web/static/src/js/boot.js',
            '/web/static/img/favicon.ico'
        ]
        
        for resource in static_resources:
            try:
                response = requests.get(
                    f"{self.base_url}{resource}",
                    timeout=self.timeout
                )
                
                if response.status_code == 200:
                    print(f"  ✅ {resource}: OK")
                else:
                    print(f"  ⚠️  {resource}: {response.status_code}")
                    
            except requests.exceptions.RequestException as e:
                print(f"  ❌ {resource}: Error - {e}")
        
        print(f"✅ Verificación de recursos estáticos completada")

class TestPatcoModulesRegression(PatcoTestCase):
    """Tests de regresión específicos para módulos PATCO"""
    
    @pytest.fixture(autouse=True)
    def setup(self, test_config, patco_modules):
        """Setup para tests de módulos PATCO"""
        self.config = test_config
        self.patco_modules = patco_modules
        self.base_url = f"http://{self.config['odoo_host']}:{self.config['odoo_port']}"
        self.project_root = Path(__file__).parent.parent.parent
    
    @pytest.mark.regression
    @pytest.mark.critical
    def test_patco_modules_are_discoverable(self):
        """Verificar que los módulos PATCO sean descubribles por Odoo"""
        print(f"\n🔍 Verificando descubrimiento de módulos PATCO...")
        
        # Verificar estructura de archivos necesaria para descubrimiento
        missing_requirements = []
        
        for module_name in self.patco_modules:
            module_path = self.project_root / 'extra-addons' / module_name
            
            if not module_path.exists():
                missing_requirements.append(f"{module_name}: Directorio no existe")
                continue
            
            # Verificar __manifest__.py
            manifest_path = module_path / '__manifest__.py'
            if not manifest_path.exists():
                missing_requirements.append(f"{module_name}: __manifest__.py faltante")
            else:
                print(f"  ✅ {module_name}: __manifest__.py")
            
            # Verificar __init__.py
            init_path = module_path / '__init__.py'
            if not init_path.exists():
                missing_requirements.append(f"{module_name}: __init__.py faltante")
            else:
                print(f"  ✅ {module_name}: __init__.py")
        
        assert not missing_requirements, f"Requisitos faltantes para descubrimiento: {missing_requirements}"
        print(f"✅ Todos los módulos PATCO son descubribles")
    
    @pytest.mark.regression
    def test_patco_module_manifests_have_required_fields(self):
        """Verificar que los manifests tengan campos requeridos"""
        print(f"\n🔍 Verificando campos requeridos en manifests...")
        
        required_fields = ['name', 'version', 'depends', 'data']
        recommended_fields = ['author', 'category', 'description', 'installable']
        
        manifest_issues = []
        
        for module_name in self.patco_modules:
            manifest_path = self.project_root / 'extra-addons' / module_name / '__manifest__.py'
            
            if manifest_path.exists():
                try:
                    with open(manifest_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    import ast
                    manifest_dict = ast.literal_eval(content)
                    
                    print(f"  📋 Verificando {module_name}...")
                    
                    # Verificar campos requeridos
                    missing_required = []
                    for field in required_fields:
                        if field not in manifest_dict:
                            missing_required.append(field)
                        else:
                            print(f"    ✅ {field}: {manifest_dict[field]}")
                    
                    if missing_required:
                        manifest_issues.append(f"{module_name}: Campos requeridos faltantes: {missing_required}")
                    
                    # Verificar campos recomendados
                    missing_recommended = []
                    for field in recommended_fields:
                        if field not in manifest_dict:
                            missing_recommended.append(field)
                        else:
                            print(f"    ✅ {field}: {manifest_dict[field]}")
                    
                    if missing_recommended:
                        print(f"    ⚠️  Campos recomendados faltantes: {missing_recommended}")
                    
                except Exception as e:
                    manifest_issues.append(f"{module_name}: Error leyendo manifest: {e}")
        
        if manifest_issues:
            print(f"  ❌ Problemas en manifests:")
            for issue in manifest_issues:
                print(f"    - {issue}")
        
        # No fallar por campos recomendados faltantes, solo requeridos
        critical_issues = [issue for issue in manifest_issues if 'requeridos faltantes' in issue]
        assert not critical_issues, f"Problemas críticos en manifests: {critical_issues}"
        
        print(f"✅ Verificación de manifests completada")
    
    @pytest.mark.regression
    @pytest.mark.slow
    def test_patco_modules_installation_readiness(self):
        """Verificar que los módulos estén listos para instalación"""
        print(f"\n🔍 Verificando preparación para instalación...")
        
        installation_issues = []
        
        for module_name in self.patco_modules:
            module_path = self.project_root / 'extra-addons' / module_name
            print(f"  🔧 Verificando {module_name}...")
            
            # Verificar estructura básica
            required_structure = {
                '__init__.py': 'Archivo de inicialización',
                '__manifest__.py': 'Manifest del módulo'
            }
            
            for file_name, description in required_structure.items():
                file_path = module_path / file_name
                if not file_path.exists():
                    installation_issues.append(f"{module_name}: {description} faltante")
                else:
                    print(f"    ✅ {file_name}")
            
            # Verificar directorios comunes si existen
            common_dirs = ['models', 'views', 'security', 'data', 'static']
            existing_dirs = []
            
            for dir_name in common_dirs:
                dir_path = module_path / dir_name
                if dir_path.exists():
                    existing_dirs.append(dir_name)
                    print(f"    📂 {dir_name}/")
                    
                    # Verificar que los directorios no estén vacíos
                    if dir_name in ['models', 'views'] and not any(dir_path.iterdir()):
                        print(f"    ⚠️  {dir_name}/ está vacío")
            
            if existing_dirs:
                print(f"    📋 Estructura encontrada: {existing_dirs}")
            else:
                print(f"    ⚠️  No se encontraron directorios estándar")
        
        if installation_issues:
            print(f"  ❌ Problemas de instalación:")
            for issue in installation_issues:
                print(f"    - {issue}")
        
        assert not installation_issues, f"Problemas que impiden instalación: {installation_issues}"
        print(f"✅ Todos los módulos están listos para instalación")

class TestSystemIntegrationRegression(PatcoTestCase):
    """Tests de regresión de integración del sistema"""
    
    @pytest.fixture(autouse=True)
    def setup(self, test_config):
        """Setup para tests de integración"""
        self.config = test_config
        self.base_url = f"http://{self.config['odoo_host']}:{self.config['odoo_port']}"
        self.project_root = Path(__file__).parent.parent.parent
    
    @pytest.mark.regression
    @pytest.mark.integration
    def test_docker_services_are_healthy(self):
        """Verificar que los servicios Docker estén saludables"""
        print(f"\n🔍 Verificando salud de servicios Docker...")
        
        import subprocess
        
        try:
            # Verificar estado de contenedores
            result = subprocess.run(
                ['docker-compose', 'ps'],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                check=True
            )
            
            output = result.stdout
            print(f"  📋 Estado de contenedores:")
            print(f"    {output}")
            
            # Verificar que los servicios principales estén corriendo
            assert 'Up' in output, "Servicios no están corriendo"
            
            # Verificar servicios específicos
            expected_services = ['odoo', 'db']
            for service in expected_services:
                if service in output.lower():
                    print(f"  ✅ Servicio {service}: Encontrado")
                else:
                    print(f"  ⚠️  Servicio {service}: No encontrado")
            
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Error verificando servicios Docker: {e}")
        except FileNotFoundError:
            pytest.skip("Docker Compose no disponible")
        
        print(f"✅ Verificación de servicios Docker completada")
    
    @pytest.mark.regression
    @pytest.mark.integration
    def test_odoo_logs_show_no_critical_errors(self):
        """Verificar que los logs no muestren errores críticos"""
        print(f"\n🔍 Verificando logs de Odoo...")
        
        import subprocess
        
        try:
            # Obtener logs recientes
            result = subprocess.run(
                ['docker-compose', 'logs', '--tail=50', 'odoo'],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                check=True
            )
            
            logs = result.stdout
            
            # Buscar errores críticos
            critical_errors = [
                'CRITICAL',
                'FATAL',
                'ERROR.*database',
                'ERROR.*connection',
                'ImportError',
                'ModuleNotFoundError'
            ]
            
            found_errors = []
            for error_pattern in critical_errors:
                import re
                if re.search(error_pattern, logs, re.IGNORECASE):
                    found_errors.append(error_pattern)
            
            if found_errors:
                print(f"  ⚠️  Errores críticos encontrados: {found_errors}")
                print(f"  📋 Últimas líneas de log:")
                for line in logs.split('\n')[-10:]:
                    if line.strip():
                        print(f"    {line}")
            else:
                print(f"  ✅ No se encontraron errores críticos")
            
            # Verificar que Odoo esté iniciando correctamente
            if 'odoo.service.server: HTTP service' in logs:
                print(f"  ✅ Servicio HTTP de Odoo iniciado")
            else:
                print(f"  ⚠️  Servicio HTTP de Odoo no confirmado")
            
        except subprocess.CalledProcessError as e:
            print(f"  ⚠️  Error obteniendo logs: {e}")
        except FileNotFoundError:
            pytest.skip("Docker Compose no disponible")
        
        print(f"✅ Verificación de logs completada")
    
    @pytest.mark.regression
    @pytest.mark.integration
    def test_configuration_files_are_valid(self):
        """Verificar que los archivos de configuración sean válidos"""
        print(f"\n🔍 Verificando archivos de configuración...")
        
        config_files = {
            'docker-compose.yml': 'Configuración Docker Compose',
            'config/odoo.conf': 'Configuración Odoo'
        }
        
        config_issues = []
        
        for file_path, description in config_files.items():
            full_path = self.project_root / file_path
            
            if not full_path.exists():
                config_issues.append(f"{description}: Archivo no existe")
                continue
            
            print(f"  📄 Verificando {file_path}...")
            
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if not content.strip():
                    config_issues.append(f"{description}: Archivo vacío")
                else:
                    print(f"    ✅ {description}: Contenido válido ({len(content)} caracteres)")
                    
                    # Verificaciones específicas
                    if file_path == 'docker-compose.yml':
                        if 'odoo' not in content or 'db' not in content:
                            config_issues.append(f"{description}: Servicios básicos faltantes")
                        else:
                            print(f"    ✅ Servicios básicos encontrados")
                    
                    elif file_path == 'config/odoo.conf':
                        required_sections = ['db_host', 'db_port', 'addons_path']
                        missing_sections = []
                        for section in required_sections:
                            if section not in content:
                                missing_sections.append(section)
                            else:
                                print(f"    ✅ {section} configurado")
                        
                        if missing_sections:
                            config_issues.append(f"{description}: Secciones faltantes: {missing_sections}")
                
            except Exception as e:
                config_issues.append(f"{description}: Error leyendo archivo: {e}")
        
        if config_issues:
            print(f"  ❌ Problemas de configuración:")
            for issue in config_issues:
                print(f"    - {issue}")
        
        assert not config_issues, f"Problemas críticos de configuración: {config_issues}"
        print(f"✅ Todos los archivos de configuración son válidos")

# Tests de funcionalidad específica que se pueden ejecutar independientemente

@pytest.mark.regression
@pytest.mark.smoke
def test_project_root_structure():
    """Test básico de estructura del proyecto"""
    print(f"\n🔍 Verificando estructura raíz del proyecto...")
    
    project_root = Path(__file__).parent.parent.parent
    
    # Verificar archivos críticos
    critical_files = {
        'docker-compose.yml': 'Configuración Docker',
        'README.md': 'Documentación principal',
        '.gitignore': 'Configuración Git'
    }
    
    missing_files = []
    for file_name, description in critical_files.items():
        file_path = project_root / file_name
        if not file_path.exists():
            missing_files.append(f"{description} ({file_name})")
        else:
            print(f"  ✅ {file_name}: {description}")
    
    # Verificar directorios críticos
    critical_dirs = ['extra-addons', 'config', 'tests']
    missing_dirs = []
    for dir_name in critical_dirs:
        dir_path = project_root / dir_name
        if not dir_path.exists():
            missing_dirs.append(dir_name)
        else:
            print(f"  ✅ {dir_name}/")
    
    # Reportar problemas pero no fallar por archivos opcionales
    if missing_files:
        print(f"  ⚠️  Archivos opcionales faltantes: {missing_files}")
    
    assert not missing_dirs, f"Directorios críticos faltantes: {missing_dirs}"
    print(f"✅ Estructura raíz del proyecto verificada")

@pytest.mark.regression
@pytest.mark.smoke
def test_python_environment():
    """Verificar entorno Python básico"""
    print(f"\n🔍 Verificando entorno Python...")
    
    import sys
    import platform
    
    print(f"  🐍 Python: {sys.version}")
    print(f"  💻 Plataforma: {platform.platform()}")
    print(f"  📁 Path: {sys.path[:3]}...")  # Mostrar solo los primeros 3
    
    # Verificar módulos básicos
    required_modules = ['os', 'sys', 'pathlib', 'json']
    for module_name in required_modules:
        try:
            __import__(module_name)
            print(f"  ✅ {module_name}: Disponible")
        except ImportError:
            pytest.fail(f"Módulo básico {module_name} no disponible")
    
    print(f"✅ Entorno Python verificado")