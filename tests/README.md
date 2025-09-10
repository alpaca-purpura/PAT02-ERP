# Tests de Compatibilidad y Regresión - PATCO ERP

## Estructura de Tests para Refactorización

Esta estructura de tests está diseñada para validar que la refactorización de módulos PATCO preserve toda la funcionalidad existente.

## Estructura de Directorios

```
tests/
├── README.md                          # Este archivo
├── compatibility/                     # Tests de compatibilidad entre módulos
│   ├── test_module_dependencies.py   # Validar dependencias
│   ├── test_module_installation.py   # Validar instalación independiente
│   └── test_data_integrity.py        # Validar integridad de datos
├── regression/                        # Tests de regresión funcional
│   ├── test_fsm_workflows.py         # Workflows de Field Service
│   ├── test_customer_equipment.py    # Gestión de equipos
│   ├── test_hr_skills.py             # Habilidades de empleados
│   ├── test_timesheet_integration.py # Integración de timesheet
│   └── test_helpdesk_integration.py  # Integración con helpdesk
├── performance/                       # Tests de rendimiento
│   ├── test_module_loading.py        # Tiempo de carga de módulos
│   └── test_database_queries.py      # Optimización de consultas
├── scripts/                          # Scripts de utilidad
│   ├── run_all_tests.py             # Ejecutar todos los tests
│   ├── validate_migration.py        # Validar migración completa
│   └── backup_test_data.py          # Backup de datos de test
└── fixtures/                         # Datos de prueba
    ├── test_companies.xml           # Empresas de prueba
    ├── test_users.xml               # Usuarios de prueba
    ├── test_equipment.xml           # Equipos de prueba
    └── test_fsm_orders.xml          # Órdenes de trabajo de prueba
```

## Tipos de Tests

### 1. Tests de Compatibilidad
**Objetivo:** Verificar que los módulos funcionen correctamente juntos

- **Dependencias:** Validar que las dependencias se resuelvan correctamente
- **Instalación:** Verificar instalación independiente de módulos
- **Integridad:** Asegurar que los datos no se corrompan

### 2. Tests de Regresión
**Objetivo:** Verificar que la funcionalidad existente se preserve

- **Workflows FSM:** Crear, asignar, completar órdenes de trabajo
- **Gestión de Equipos:** CRUD de equipos de clientes
- **Habilidades HR:** Asignación de habilidades a empleados
- **Timesheet:** Registro de tiempo en órdenes de trabajo
- **Helpdesk:** Creación de tickets vinculados a FSM

### 3. Tests de Rendimiento
**Objetivo:** Verificar que el rendimiento no se degrade

- **Carga de Módulos:** Tiempo de inicialización
- **Consultas DB:** Optimización de queries

## Estrategia de Testing

### Fase 0: Baseline (Estado Actual)
1. Ejecutar todos los tests en el estado actual
2. Documentar resultados como baseline
3. Identificar tests que fallan en estado actual

### Durante Refactorización
1. Ejecutar tests después de cada cambio mayor
2. Validar que no se introduzcan regresiones
3. Actualizar tests si cambia la API

### Fase Final: Validación Completa
1. Ejecutar suite completa de tests
2. Comparar con baseline
3. Validar que todas las funcionalidades funcionen

## Comandos de Ejecución

### Ejecutar Todos los Tests
```bash
python tests/scripts/run_all_tests.py
```

### Ejecutar Tests por Categoría
```bash
# Tests de compatibilidad
python -m pytest tests/compatibility/ -v

# Tests de regresión
python -m pytest tests/regression/ -v

# Tests de rendimiento
python -m pytest tests/performance/ -v
```

### Ejecutar Tests Específicos
```bash
# Test de dependencias
python -m pytest tests/compatibility/test_module_dependencies.py -v

# Test de workflows FSM
python -m pytest tests/regression/test_fsm_workflows.py -v
```

## Configuración de Entorno de Test

### Base de Datos de Test
- **Nombre:** `odoo_patco_test`
- **Datos:** Fixtures mínimos para tests
- **Aislamiento:** Cada test en transacción separada

### Módulos de Test
- **Instalación:** Solo módulos necesarios para cada test
- **Configuración:** Configuración mínima para funcionalidad

## Criterios de Éxito

### Tests de Compatibilidad
- ✅ Todos los módulos se instalan sin errores
- ✅ No hay dependencias circulares
- ✅ Datos se migran correctamente

### Tests de Regresión
- ✅ Todos los workflows principales funcionan
- ✅ APIs existentes responden correctamente
- ✅ Integraciones OCA funcionan

### Tests de Rendimiento
- ✅ Tiempo de carga ≤ baseline + 10%
- ✅ Consultas DB optimizadas
- ✅ Memoria utilizada ≤ baseline + 15%

## Mantenimiento de Tests

### Actualización de Tests
- Actualizar tests cuando cambie funcionalidad
- Añadir tests para nuevas funcionalidades
- Remover tests obsoletos

### Documentación
- Documentar cambios en tests
- Mantener README actualizado
- Documentar casos edge conocidos

## Herramientas Utilizadas

- **pytest:** Framework de testing principal
- **odoo-test:** Utilidades específicas de Odoo
- **coverage:** Cobertura de código
- **xmlrunner:** Reportes XML para CI/CD

---

**Creado:** 2025-01-09  
**Propósito:** Validar refactorización conservadora de módulos PATCO  
**Estado:** Estructura base creada, pendiente implementación de tests