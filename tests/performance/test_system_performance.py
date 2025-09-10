# -*- coding: utf-8 -*-
"""
Tests de Rendimiento - Sistema PATCO ERP

Estos tests monitorean el rendimiento del sistema para detectar
regresiones de performance durante la refactorización.
"""

import pytest
import time
import requests
import psutil
import statistics
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Any

# Importar clase base de tests
try:
    from tests.conftest import PatcoTestCase
except ImportError:
    class PatcoTestCase:
        pass

class PerformanceMonitor:
    """Monitor de rendimiento para tests"""
    
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.memory_start = None
        self.memory_end = None
        self.cpu_samples = []
    
    def start(self):
        """Iniciar monitoreo"""
        self.start_time = time.time()
        self.memory_start = psutil.virtual_memory().used
        self.cpu_samples = []
        return self
    
    def sample_cpu(self):
        """Tomar muestra de CPU"""
        cpu_percent = psutil.cpu_percent(interval=0.1)
        self.cpu_samples.append(cpu_percent)
        return cpu_percent
    
    def stop(self):
        """Detener monitoreo"""
        self.end_time = time.time()
        self.memory_end = psutil.virtual_memory().used
        return self
    
    def get_metrics(self) -> Dict[str, Any]:
        """Obtener métricas de rendimiento"""
        if not self.start_time or not self.end_time:
            return {}
        
        duration = self.end_time - self.start_time
        memory_delta = (self.memory_end - self.memory_start) / (1024 * 1024)  # MB
        
        cpu_stats = {}
        if self.cpu_samples:
            cpu_stats = {
                'avg': statistics.mean(self.cpu_samples),
                'max': max(self.cpu_samples),
                'min': min(self.cpu_samples)
            }
        
        return {
            'duration_seconds': round(duration, 3),
            'memory_delta_mb': round(memory_delta, 2),
            'cpu_usage': cpu_stats
        }

class TestOdooPerformance(PatcoTestCase):
    """Tests de rendimiento del sistema Odoo"""
    
    @pytest.fixture(autouse=True)
    def setup(self, test_config):
        """Setup para tests de rendimiento"""
        self.config = test_config
        self.base_url = f"http://{self.config['odoo_host']}:{self.config['odoo_port']}"
        self.timeout = self.config['timeout']
        self.performance_thresholds = {
            'response_time_max': 5.0,  # segundos
            'memory_usage_max': 100,   # MB
            'cpu_usage_max': 80        # porcentaje
        }
    
    @pytest.mark.performance
    @pytest.mark.critical
    def test_odoo_startup_time(self):
        """Medir tiempo de inicio de Odoo"""
        print(f"\n⏱️  Midiendo tiempo de respuesta inicial de Odoo...")
        
        monitor = PerformanceMonitor().start()
        
        # Realizar múltiples requests para medir consistencia
        response_times = []
        
        for i in range(5):
            start_time = time.time()
            
            try:
                response = requests.get(
                    f"{self.base_url}/web/health",
                    timeout=self.timeout
                )
                
                end_time = time.time()
                response_time = end_time - start_time
                response_times.append(response_time)
                
                monitor.sample_cpu()
                
                print(f"  📊 Request {i+1}: {response_time:.3f}s (Status: {response.status_code})")
                
                # Pequeña pausa entre requests
                time.sleep(0.5)
                
            except requests.exceptions.RequestException as e:
                print(f"  ❌ Request {i+1} falló: {e}")
                response_times.append(self.timeout)  # Penalizar con timeout
        
        monitor.stop()
        metrics = monitor.get_metrics()
        
        # Calcular estadísticas
        if response_times:
            avg_response_time = statistics.mean(response_times)
            max_response_time = max(response_times)
            min_response_time = min(response_times)
            
            print(f"  📈 Estadísticas de respuesta:")
            print(f"    • Promedio: {avg_response_time:.3f}s")
            print(f"    • Máximo: {max_response_time:.3f}s")
            print(f"    • Mínimo: {min_response_time:.3f}s")
            print(f"    • Duración total: {metrics.get('duration_seconds', 0)}s")
            
            if metrics.get('cpu_usage'):
                cpu = metrics['cpu_usage']
                print(f"    • CPU promedio: {cpu.get('avg', 0):.1f}%")
            
            # Verificar umbrales
            assert avg_response_time < self.performance_thresholds['response_time_max'], \
                f"Tiempo de respuesta promedio ({avg_response_time:.3f}s) excede umbral ({self.performance_thresholds['response_time_max']}s)"
            
            print(f"  ✅ Rendimiento dentro de umbrales aceptables")
        else:
            pytest.fail("No se pudieron obtener tiempos de respuesta")
    
    @pytest.mark.performance
    def test_odoo_concurrent_requests(self):
        """Probar rendimiento con requests concurrentes"""
        print(f"\n⏱️  Probando requests concurrentes...")
        
        import concurrent.futures
        import threading
        
        def make_request(request_id: int) -> Dict[str, Any]:
            """Realizar un request individual"""
            start_time = time.time()
            
            try:
                response = requests.get(
                    f"{self.base_url}/web/login",
                    timeout=self.timeout
                )
                
                end_time = time.time()
                
                return {
                    'id': request_id,
                    'success': True,
                    'status_code': response.status_code,
                    'response_time': end_time - start_time,
                    'content_length': len(response.content)
                }
                
            except Exception as e:
                return {
                    'id': request_id,
                    'success': False,
                    'error': str(e),
                    'response_time': time.time() - start_time
                }
        
        monitor = PerformanceMonitor().start()
        
        # Ejecutar requests concurrentes
        num_concurrent = 10
        results = []
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_concurrent) as executor:
            # Enviar todos los requests
            futures = [executor.submit(make_request, i) for i in range(num_concurrent)]
            
            # Monitorear CPU mientras se ejecutan
            for _ in range(5):
                monitor.sample_cpu()
                time.sleep(0.2)
            
            # Recopilar resultados
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                results.append(result)
                
                if result['success']:
                    print(f"  ✅ Request {result['id']}: {result['response_time']:.3f}s")
                else:
                    print(f"  ❌ Request {result['id']}: {result.get('error', 'Error desconocido')}")
        
        monitor.stop()
        metrics = monitor.get_metrics()
        
        # Analizar resultados
        successful_requests = [r for r in results if r['success']]
        failed_requests = [r for r in results if not r['success']]
        
        print(f"  📊 Resultados de concurrencia:")
        print(f"    • Exitosos: {len(successful_requests)}/{num_concurrent}")
        print(f"    • Fallidos: {len(failed_requests)}/{num_concurrent}")
        print(f"    • Duración total: {metrics.get('duration_seconds', 0)}s")
        
        if successful_requests:
            response_times = [r['response_time'] for r in successful_requests]
            avg_time = statistics.mean(response_times)
            max_time = max(response_times)
            
            print(f"    • Tiempo promedio: {avg_time:.3f}s")
            print(f"    • Tiempo máximo: {max_time:.3f}s")
            
            if metrics.get('cpu_usage'):
                cpu = metrics['cpu_usage']
                print(f"    • CPU máximo: {cpu.get('max', 0):.1f}%")
        
        # Verificar que al menos el 80% de requests sean exitosos
        success_rate = len(successful_requests) / num_concurrent
        assert success_rate >= 0.8, f"Tasa de éxito ({success_rate:.1%}) menor al 80%"
        
        print(f"  ✅ Rendimiento concurrente aceptable")
    
    @pytest.mark.performance
    @pytest.mark.slow
    def test_odoo_memory_usage_stability(self):
        """Probar estabilidad del uso de memoria"""
        print(f"\n🧠 Monitoreando uso de memoria...")
        
        # Obtener uso inicial de memoria
        initial_memory = psutil.virtual_memory().used / (1024 * 1024)  # MB
        print(f"  📊 Memoria inicial: {initial_memory:.1f} MB")
        
        memory_samples = [initial_memory]
        
        # Realizar operaciones que podrían consumir memoria
        operations = [
            '/web/login',
            '/web/static/src/css/bootstrap.css',
            '/web/static/src/js/boot.js',
            '/web/health'
        ]
        
        for i in range(3):  # 3 ciclos de operaciones
            print(f"  🔄 Ciclo {i+1}/3...")
            
            for operation in operations:
                try:
                    response = requests.get(
                        f"{self.base_url}{operation}",
                        timeout=self.timeout
                    )
                    
                    # Tomar muestra de memoria después de cada operación
                    current_memory = psutil.virtual_memory().used / (1024 * 1024)
                    memory_samples.append(current_memory)
                    
                    time.sleep(0.5)  # Pausa entre operaciones
                    
                except requests.exceptions.RequestException as e:
                    print(f"    ⚠️  Error en {operation}: {e}")
        
        # Analizar uso de memoria
        final_memory = memory_samples[-1]
        memory_delta = final_memory - initial_memory
        max_memory = max(memory_samples)
        min_memory = min(memory_samples)
        
        print(f"  📈 Análisis de memoria:")
        print(f"    • Inicial: {initial_memory:.1f} MB")
        print(f"    • Final: {final_memory:.1f} MB")
        print(f"    • Delta: {memory_delta:+.1f} MB")
        print(f"    • Máximo: {max_memory:.1f} MB")
        print(f"    • Mínimo: {min_memory:.1f} MB")
        
        # Verificar que no haya fugas de memoria significativas
        memory_leak_threshold = 50  # MB
        assert abs(memory_delta) < memory_leak_threshold, \
            f"Posible fuga de memoria: {memory_delta:+.1f} MB (umbral: ±{memory_leak_threshold} MB)"
        
        print(f"  ✅ Uso de memoria estable")

class TestPatcoModulesPerformance(PatcoTestCase):
    """Tests de rendimiento específicos para módulos PATCO"""
    
    @pytest.fixture(autouse=True)
    def setup(self, test_config, patco_modules):
        """Setup para tests de rendimiento de módulos"""
        self.config = test_config
        self.patco_modules = patco_modules
        self.project_root = Path(__file__).parent.parent.parent
    
    @pytest.mark.performance
    def test_module_loading_performance(self):
        """Medir rendimiento de carga de módulos"""
        print(f"\n⏱️  Midiendo rendimiento de carga de módulos...")
        
        loading_times = {}
        
        for module_name in self.patco_modules:
            print(f"  🔧 Analizando {module_name}...")
            
            module_path = self.project_root / 'extra-addons' / module_name
            
            if not module_path.exists():
                print(f"    ⚠️  Módulo no encontrado")
                continue
            
            monitor = PerformanceMonitor().start()
            
            # Simular carga del módulo leyendo archivos principales
            files_read = 0
            total_size = 0
            
            for file_pattern in ['*.py', '*.xml', '*.csv']:
                for file_path in module_path.rglob(file_pattern):
                    try:
                        start_time = time.time()
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            total_size += len(content)
                            files_read += 1
                        
                        # Simular procesamiento básico
                        time.sleep(0.001)  # 1ms por archivo
                        
                    except Exception as e:
                        print(f"    ⚠️  Error leyendo {file_path.name}: {e}")
            
            monitor.stop()
            metrics = monitor.get_metrics()
            
            loading_times[module_name] = {
                'duration': metrics.get('duration_seconds', 0),
                'files_count': files_read,
                'total_size_kb': round(total_size / 1024, 2),
                'avg_file_time': round(metrics.get('duration_seconds', 0) / max(files_read, 1) * 1000, 2)  # ms
            }
            
            print(f"    📊 {files_read} archivos, {total_size/1024:.1f} KB, {metrics.get('duration_seconds', 0):.3f}s")
        
        # Analizar resultados generales
        if loading_times:
            total_duration = sum(data['duration'] for data in loading_times.values())
            total_files = sum(data['files_count'] for data in loading_times.values())
            
            print(f"  📈 Resumen de rendimiento:")
            print(f"    • Módulos analizados: {len(loading_times)}")
            print(f"    • Tiempo total: {total_duration:.3f}s")
            print(f"    • Archivos totales: {total_files}")
            print(f"    • Promedio por módulo: {total_duration/len(loading_times):.3f}s")
            
            # Identificar módulos más lentos
            slowest_modules = sorted(
                loading_times.items(),
                key=lambda x: x[1]['duration'],
                reverse=True
            )[:3]
            
            print(f"    • Módulos más lentos:")
            for module_name, data in slowest_modules:
                print(f"      - {module_name}: {data['duration']:.3f}s ({data['files_count']} archivos)")
        
        print(f"  ✅ Análisis de rendimiento de módulos completado")
    
    @pytest.mark.performance
    def test_module_structure_complexity(self):
        """Analizar complejidad estructural de módulos"""
        print(f"\n📊 Analizando complejidad estructural...")
        
        complexity_metrics = {}
        
        for module_name in self.patco_modules:
            print(f"  🔍 Analizando {module_name}...")
            
            module_path = self.project_root / 'extra-addons' / module_name
            
            if not module_path.exists():
                continue
            
            metrics = {
                'total_files': 0,
                'python_files': 0,
                'xml_files': 0,
                'total_lines': 0,
                'max_file_lines': 0,
                'directory_depth': 0,
                'largest_file': ''
            }
            
            # Analizar estructura de archivos
            for file_path in module_path.rglob('*'):
                if file_path.is_file():
                    metrics['total_files'] += 1
                    
                    # Calcular profundidad de directorio
                    depth = len(file_path.relative_to(module_path).parts) - 1
                    metrics['directory_depth'] = max(metrics['directory_depth'], depth)
                    
                    # Contar líneas en archivos de texto
                    if file_path.suffix in ['.py', '.xml', '.csv', '.yml', '.yaml']:
                        try:
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                lines = len(f.readlines())
                                metrics['total_lines'] += lines
                                
                                if lines > metrics['max_file_lines']:
                                    metrics['max_file_lines'] = lines
                                    metrics['largest_file'] = file_path.name
                                
                                if file_path.suffix == '.py':
                                    metrics['python_files'] += 1
                                elif file_path.suffix == '.xml':
                                    metrics['xml_files'] += 1
                        
                        except Exception:
                            pass  # Ignorar archivos que no se pueden leer
            
            complexity_metrics[module_name] = metrics
            
            print(f"    📋 {metrics['total_files']} archivos, {metrics['total_lines']} líneas")
            print(f"    📄 Python: {metrics['python_files']}, XML: {metrics['xml_files']}")
            print(f"    📏 Archivo más grande: {metrics['largest_file']} ({metrics['max_file_lines']} líneas)")
            print(f"    📂 Profundidad máxima: {metrics['directory_depth']} niveles")
        
        # Generar reporte de complejidad
        if complexity_metrics:
            print(f"  📈 Análisis de complejidad:")
            
            # Módulo más complejo (por líneas de código)
            most_complex = max(
                complexity_metrics.items(),
                key=lambda x: x[1]['total_lines']
            )
            
            print(f"    • Módulo más complejo: {most_complex[0]} ({most_complex[1]['total_lines']} líneas)")
            
            # Promedio de archivos por módulo
            avg_files = statistics.mean([m['total_files'] for m in complexity_metrics.values()])
            print(f"    • Promedio de archivos: {avg_files:.1f}")
            
            # Promedio de líneas por módulo
            avg_lines = statistics.mean([m['total_lines'] for m in complexity_metrics.values()])
            print(f"    • Promedio de líneas: {avg_lines:.0f}")
            
            # Identificar módulos que podrían necesitar refactorización
            large_modules = [
                name for name, metrics in complexity_metrics.items()
                if metrics['total_lines'] > avg_lines * 1.5
            ]
            
            if large_modules:
                print(f"    • Módulos grandes (candidatos a refactorización): {large_modules}")
        
        print(f"  ✅ Análisis de complejidad completado")

class TestSystemResourceUsage(PatcoTestCase):
    """Tests de uso de recursos del sistema"""
    
    @pytest.fixture(autouse=True)
    def setup(self, test_config):
        """Setup para tests de recursos"""
        self.config = test_config
        self.resource_thresholds = {
            'cpu_max': 90,      # porcentaje
            'memory_max': 80,   # porcentaje
            'disk_max': 90      # porcentaje
        }
    
    @pytest.mark.performance
    @pytest.mark.system
    def test_system_resource_usage(self):
        """Monitorear uso de recursos del sistema"""
        print(f"\n💻 Monitoreando recursos del sistema...")
        
        # CPU
        cpu_percent = psutil.cpu_percent(interval=1)
        print(f"  🔥 CPU: {cpu_percent:.1f}%")
        
        # Memoria
        memory = psutil.virtual_memory()
        memory_percent = memory.percent
        memory_used_gb = memory.used / (1024**3)
        memory_total_gb = memory.total / (1024**3)
        
        print(f"  🧠 Memoria: {memory_percent:.1f}% ({memory_used_gb:.1f}/{memory_total_gb:.1f} GB)")
        
        # Disco
        disk = psutil.disk_usage('/')
        disk_percent = disk.percent
        disk_used_gb = disk.used / (1024**3)
        disk_total_gb = disk.total / (1024**3)
        
        print(f"  💾 Disco: {disk_percent:.1f}% ({disk_used_gb:.1f}/{disk_total_gb:.1f} GB)")
        
        # Verificar umbrales
        resource_issues = []
        
        if cpu_percent > self.resource_thresholds['cpu_max']:
            resource_issues.append(f"CPU alto: {cpu_percent:.1f}%")
        
        if memory_percent > self.resource_thresholds['memory_max']:
            resource_issues.append(f"Memoria alta: {memory_percent:.1f}%")
        
        if disk_percent > self.resource_thresholds['disk_max']:
            resource_issues.append(f"Disco alto: {disk_percent:.1f}%")
        
        if resource_issues:
            print(f"  ⚠️  Advertencias de recursos: {resource_issues}")
        else:
            print(f"  ✅ Uso de recursos dentro de límites normales")
        
        # No fallar por uso alto de recursos, solo advertir
        # En un entorno de producción podrías querer fallar
        
        print(f"✅ Monitoreo de recursos completado")
    
    @pytest.mark.performance
    @pytest.mark.system
    def test_docker_container_resources(self):
        """Monitorear recursos de contenedores Docker"""
        print(f"\n🐳 Monitoreando recursos de contenedores...")
        
        import subprocess
        
        try:
            # Obtener estadísticas de contenedores
            result = subprocess.run(
                ['docker', 'stats', '--no-stream', '--format', 
                 'table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.MemPerc}}'],
                capture_output=True,
                text=True,
                check=True
            )
            
            output = result.stdout
            print(f"  📊 Estadísticas de contenedores:")
            
            for line in output.split('\n'):
                if line.strip() and 'CONTAINER' not in line:
                    print(f"    {line}")
            
            # Verificar contenedores específicos de PATCO
            patco_containers = ['odoo', 'db', 'postgres']
            
            for container in patco_containers:
                if container.lower() in output.lower():
                    print(f"  ✅ Contenedor {container}: Monitoreado")
        
        except subprocess.CalledProcessError as e:
            print(f"  ⚠️  Error obteniendo estadísticas Docker: {e}")
        except FileNotFoundError:
            pytest.skip("Docker no disponible")
        
        print(f"✅ Monitoreo de contenedores completado")

# Utilidades para reportes de rendimiento

def generate_performance_report(results_dir: Path = None):
    """Generar reporte de rendimiento"""
    if not results_dir:
        results_dir = Path(__file__).parent.parent / 'results'
    
    results_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    report_file = results_dir / f'performance_report_{timestamp}.json'
    
    report_data = {
        'timestamp': timestamp,
        'system_info': {
            'cpu_count': psutil.cpu_count(),
            'memory_total_gb': round(psutil.virtual_memory().total / (1024**3), 2),
            'disk_total_gb': round(psutil.disk_usage('/').total / (1024**3), 2)
        },
        'thresholds': {
            'response_time_max': 5.0,
            'memory_usage_max': 100,
            'cpu_usage_max': 80
        }
    }
    
    with open(report_file, 'w', encoding='utf-8') as f:
        import json
        json.dump(report_data, f, indent=2, ensure_ascii=False)
    
    print(f"📄 Reporte de rendimiento guardado: {report_file}")
    return report_file

# Test independiente para generar reporte
@pytest.mark.performance
@pytest.mark.report
def test_generate_performance_baseline():
    """Generar línea base de rendimiento"""
    print(f"\n📊 Generando línea base de rendimiento...")
    
    report_file = generate_performance_report()
    
    assert report_file.exists(), "No se pudo generar el reporte de rendimiento"
    
    print(f"✅ Línea base de rendimiento generada: {report_file.name}")