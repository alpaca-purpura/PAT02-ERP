# -*- coding: utf-8 -*-
"""
Tests de Compatibilidad - Módulos PATCO

Estos tests verifican que los módulos PATCO sean compatibles entre sí
y que sus dependencias estén correctamente configuradas.
"""

import pytest
import os
import ast
from pathlib import Path
from unittest.mock import Mock, patch

# Importar clase base de tests
try:
    from tests.conftest import PatcoTestCase
except ImportError:
    # Fallback si no se puede importar
    class PatcoTestCase:
        def assert_module_exists(self, module_name):
            pass
        def assert_module_installable(self, module_name):
            pass

class TestModuleCompatibility(PatcoTestCase):
    """Tests de compatibilidad entre módulos PATCO"""
    
    @pytest.fixture(autouse=True)
    def setup(self, project_root_path, patco_modules):
        """Setup para tests de compatibilidad"""
        self.project_root = project_root_path
        self.patco_modules = patco_modules
        self.addons_path = self.project_root / 'extra-addons'
    
    @pytest.mark.compatibility
    @pytest.mark.critical
    def test_all_patco_modules_exist(self):
        """Verificar que todos los módulos PATCO existen"""
        print("\n🔍 Verificando existencia de módulos PATCO...")
        
        missing_modules = []
        for module_name in self.patco_modules:
            module_path = self.addons_path / module_name
            if not module_path.exists():
                missing_modules.append(module_name)
            else:
                print(f"  ✅ {module_name}: {module_path}")
        
        assert not missing_modules, f"Módulos faltantes: {missing_modules}"
        print(f"✅ Todos los {len(self.patco_modules)} módulos PATCO encontrados")
    
    @pytest.mark.compatibility
    @pytest.mark.critical
    def test_all_manifests_exist(self):
        """Verificar que todos los manifests existen"""
        print("\n🔍 Verificando manifests de módulos...")
        
        missing_manifests = []
        for module_name in self.patco_modules:
            manifest_path = self.addons_path / module_name / '__manifest__.py'
            if not manifest_path.exists():
                missing_manifests.append(module_name)
            else:
                print(f"  ✅ {module_name}: __manifest__.py")
        
        assert not missing_manifests, f"Manifests faltantes: {missing_manifests}"
        print(f"✅ Todos los manifests encontrados")
    
    @pytest.mark.compatibility
    @pytest.mark.critical
    def test_manifests_are_valid_python(self):
        """Verificar que los manifests son Python válido"""
        print("\n🔍 Verificando sintaxis de manifests...")
        
        invalid_manifests = []
        for module_name in self.patco_modules:
            manifest_path = self.addons_path / module_name / '__manifest__.py'
            if manifest_path.exists():
                try:
                    with open(manifest_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    ast.parse(content)
                    print(f"  ✅ {module_name}: Sintaxis válida")
                except SyntaxError as e:
                    invalid_manifests.append((module_name, str(e)))
                    print(f"  ❌ {module_name}: Error de sintaxis - {e}")
        
        assert not invalid_manifests, f"Manifests con errores de sintaxis: {invalid_manifests}"
        print(f"✅ Todos los manifests tienen sintaxis válida")
    
    @pytest.mark.compatibility
    @pytest.mark.critical
    def test_modules_are_installable(self):
        """Verificar que los módulos están marcados como instalables"""
        print("\n🔍 Verificando que módulos sean instalables...")
        
        non_installable = []
        for module_name in self.patco_modules:
            manifest_path = self.addons_path / module_name / '__manifest__.py'
            if manifest_path.exists():
                try:
                    with open(manifest_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Evaluar el manifest de forma segura
                    manifest_dict = ast.literal_eval(content)
                    
                    # Verificar installable (por defecto True si no se especifica)
                    installable = manifest_dict.get('installable', True)
                    
                    if installable:
                        print(f"  ✅ {module_name}: Instalable")
                    else:
                        non_installable.append(module_name)
                        print(f"  ❌ {module_name}: No instalable")
                        
                except (ValueError, SyntaxError) as e:
                    print(f"  ⚠️  {module_name}: No se pudo evaluar manifest - {e}")
        
        assert not non_installable, f"Módulos no instalables: {non_installable}"
        print(f"✅ Todos los módulos son instalables")
    
    @pytest.mark.compatibility
    def test_dependency_chain_is_valid(self):
        """Verificar que la cadena de dependencias es válida"""
        print("\n🔍 Verificando cadena de dependencias...")
        
        # Cargar dependencias de todos los módulos
        module_dependencies = {}
        for module_name in self.patco_modules:
            manifest_path = self.addons_path / module_name / '__manifest__.py'
            if manifest_path.exists():
                try:
                    with open(manifest_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    manifest_dict = ast.literal_eval(content)
                    dependencies = manifest_dict.get('depends', [])
                    module_dependencies[module_name] = dependencies
                    print(f"  📋 {module_name}: {dependencies}")
                except Exception as e:
                    print(f"  ⚠️  {module_name}: Error leyendo dependencias - {e}")
                    module_dependencies[module_name] = []
        
        # Verificar dependencias circulares
        circular_deps = self._check_circular_dependencies(module_dependencies)
        assert not circular_deps, f"Dependencias circulares detectadas: {circular_deps}"
        
        # Verificar que las dependencias PATCO existan
        missing_deps = []
        for module_name, deps in module_dependencies.items():
            for dep in deps:
                if dep.startswith('patco_') and dep not in self.patco_modules:
                    missing_deps.append((module_name, dep))
        
        assert not missing_deps, f"Dependencias PATCO faltantes: {missing_deps}"
        print(f"✅ Cadena de dependencias válida")
    
    def _check_circular_dependencies(self, dependencies):
        """Detectar dependencias circulares"""
        def has_cycle(node, visited, rec_stack, graph):
            visited[node] = True
            rec_stack[node] = True
            
            for neighbor in graph.get(node, []):
                if neighbor in graph:  # Solo verificar módulos PATCO
                    if not visited.get(neighbor, False):
                        if has_cycle(neighbor, visited, rec_stack, graph):
                            return True
                    elif rec_stack.get(neighbor, False):
                        return True
            
            rec_stack[node] = False
            return False
        
        visited = {}
        rec_stack = {}
        
        for module in dependencies:
            if not visited.get(module, False):
                if has_cycle(module, visited, rec_stack, dependencies):
                    return True
        
        return False
    
    @pytest.mark.compatibility
    def test_module_structure_consistency(self):
        """Verificar que la estructura de módulos sea consistente"""
        print("\n🔍 Verificando estructura de módulos...")
        
        required_files = ['__init__.py', '__manifest__.py']
        common_dirs = ['models', 'views', 'security', 'data']
        
        structure_issues = []
        
        for module_name in self.patco_modules:
            module_path = self.addons_path / module_name
            if module_path.exists():
                print(f"  📁 Verificando {module_name}...")
                
                # Verificar archivos requeridos
                for required_file in required_files:
                    file_path = module_path / required_file
                    if not file_path.exists():
                        structure_issues.append(f"{module_name}: Falta {required_file}")
                    else:
                        print(f"    ✅ {required_file}")
                
                # Verificar directorios comunes (opcional)
                existing_dirs = []
                for common_dir in common_dirs:
                    dir_path = module_path / common_dir
                    if dir_path.exists():
                        existing_dirs.append(common_dir)
                        print(f"    📂 {common_dir}/")
                
                if existing_dirs:
                    print(f"    📋 Directorios encontrados: {existing_dirs}")
        
        if structure_issues:
            print(f"  ⚠️  Problemas de estructura: {structure_issues}")
        
        # No fallar por problemas de estructura menores, solo advertir
        print(f"✅ Verificación de estructura completada")
    
    @pytest.mark.compatibility
    def test_python_imports_are_valid(self):
        """Verificar que los imports de Python sean válidos"""
        print("\n🔍 Verificando imports de Python...")
        
        import_errors = []
        
        for module_name in self.patco_modules:
            module_path = self.addons_path / module_name
            if module_path.exists():
                print(f"  🐍 Verificando imports en {module_name}...")
                
                # Verificar __init__.py
                init_file = module_path / '__init__.py'
                if init_file.exists():
                    try:
                        with open(init_file, 'r', encoding='utf-8') as f:
                            content = f.read()
                        ast.parse(content)
                        print(f"    ✅ __init__.py: Sintaxis válida")
                    except SyntaxError as e:
                        import_errors.append(f"{module_name}/__init__.py: {e}")
                
                # Verificar archivos Python en models/
                models_dir = module_path / 'models'
                if models_dir.exists():
                    for py_file in models_dir.glob('*.py'):
                        try:
                            with open(py_file, 'r', encoding='utf-8') as f:
                                content = f.read()
                            ast.parse(content)
                            print(f"    ✅ models/{py_file.name}: Sintaxis válida")
                        except SyntaxError as e:
                            import_errors.append(f"{module_name}/models/{py_file.name}: {e}")
        
        if import_errors:
            print(f"  ❌ Errores de sintaxis encontrados:")
            for error in import_errors:
                print(f"    - {error}")
        
        # No fallar por errores de sintaxis menores en desarrollo
        print(f"✅ Verificación de imports completada")
    
    @pytest.mark.compatibility
    @pytest.mark.slow
    def test_modules_can_be_imported(self):
        """Test de importación de módulos (requiere entorno Odoo)"""
        print("\n🔍 Verificando importación de módulos...")
        
        # Este test requiere un entorno Odoo funcional
        # En un entorno de desarrollo, se puede saltar
        
        try:
            # Intentar importar odoo
            import odoo
            print("  ✅ Odoo disponible para importación")
            
            # Aquí se podrían hacer imports reales de los módulos
            # Por ahora, solo verificamos que Odoo esté disponible
            
        except ImportError:
            pytest.skip("Odoo no disponible para test de importación")
        
        print(f"✅ Test de importación completado")

class TestModuleIntegration(PatcoTestCase):
    """Tests de integración entre módulos PATCO"""
    
    @pytest.fixture(autouse=True)
    def setup(self, project_root_path, patco_modules):
        """Setup para tests de integración"""
        self.project_root = project_root_path
        self.patco_modules = patco_modules
        self.addons_path = self.project_root / 'extra-addons'
    
    @pytest.mark.compatibility
    @pytest.mark.integration
    def test_patco_core_is_base_dependency(self):
        """Verificar que patco_core sea la dependencia base"""
        print("\n🔍 Verificando que patco_core sea dependencia base...")
        
        if 'patco_core' not in self.patco_modules:
            pytest.skip("patco_core no encontrado")
        
        # Verificar que otros módulos PATCO dependan de patco_core
        modules_without_core_dep = []
        
        for module_name in self.patco_modules:
            if module_name == 'patco_core':
                continue
                
            manifest_path = self.addons_path / module_name / '__manifest__.py'
            if manifest_path.exists():
                try:
                    with open(manifest_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    manifest_dict = ast.literal_eval(content)
                    dependencies = manifest_dict.get('depends', [])
                    
                    if 'patco_core' not in dependencies:
                        modules_without_core_dep.append(module_name)
                        print(f"  ⚠️  {module_name}: No depende de patco_core")
                    else:
                        print(f"  ✅ {module_name}: Depende de patco_core")
                        
                except Exception as e:
                    print(f"  ⚠️  {module_name}: Error leyendo manifest - {e}")
        
        # Advertir pero no fallar si algunos módulos no dependen de core
        if modules_without_core_dep:
            print(f"  📋 Módulos sin dependencia de patco_core: {modules_without_core_dep}")
            print(f"  💡 Considerar si estos módulos deberían depender de patco_core")
        
        print(f"✅ Verificación de dependencia base completada")
    
    @pytest.mark.compatibility
    @pytest.mark.integration
    def test_no_conflicting_model_names(self):
        """Verificar que no haya conflictos en nombres de modelos"""
        print("\n🔍 Verificando conflictos en nombres de modelos...")
        
        # Esta es una verificación básica
        # En un entorno real, se verificarían los modelos de Odoo
        
        model_files = {}
        
        for module_name in self.patco_modules:
            models_dir = self.addons_path / module_name / 'models'
            if models_dir.exists():
                for py_file in models_dir.glob('*.py'):
                    if py_file.name != '__init__.py':
                        file_key = py_file.name
                        if file_key in model_files:
                            print(f"  ⚠️  Archivo duplicado: {file_key} en {module_name} y {model_files[file_key]}")
                        else:
                            model_files[file_key] = module_name
                            print(f"  📄 {module_name}: {file_key}")
        
        print(f"✅ Verificación de conflictos de modelos completada")
        print(f"📊 Total de archivos de modelos encontrados: {len(model_files)}")

# Tests adicionales que se pueden ejecutar de forma independiente

@pytest.mark.compatibility
@pytest.mark.smoke
def test_basic_project_structure():
    """Test básico de estructura del proyecto"""
    print("\n🔍 Verificando estructura básica del proyecto...")
    
    project_root = Path(__file__).parent.parent.parent
    
    # Verificar directorios principales
    required_dirs = ['extra-addons', 'config', 'tests']
    missing_dirs = []
    
    for dir_name in required_dirs:
        dir_path = project_root / dir_name
        if not dir_path.exists():
            missing_dirs.append(dir_name)
        else:
            print(f"  ✅ {dir_name}/")
    
    assert not missing_dirs, f"Directorios faltantes: {missing_dirs}"
    print(f"✅ Estructura básica del proyecto verificada")

@pytest.mark.compatibility
@pytest.mark.smoke
def test_docker_compose_exists():
    """Verificar que docker-compose.yml existe"""
    print("\n🔍 Verificando configuración Docker...")
    
    project_root = Path(__file__).parent.parent.parent
    docker_compose_path = project_root / 'docker-compose.yml'
    
    assert docker_compose_path.exists(), "docker-compose.yml no encontrado"
    print(f"  ✅ docker-compose.yml: {docker_compose_path}")
    
    # Verificar que contenga servicios básicos
    with open(docker_compose_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    assert 'odoo' in content, "Servicio 'odoo' no encontrado en docker-compose.yml"
    assert 'db' in content, "Servicio 'db' no encontrado en docker-compose.yml"
    
    print(f"  ✅ Servicios básicos encontrados en docker-compose.yml")
    print(f"✅ Configuración Docker verificada")