# Estado Actual de Módulos PATCO - Fase 0 Backup

## Resumen del Backup Realizado

**Fecha:** $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
**Branch de Backup:** `backup/pre-refactoring`
**Branch de Trabajo:** `refactoring/modular-architecture`
**Commit:** 7955c1be - "Backup: Estado funcional antes de refactoring - Fase 0 PATCO"

## Inventario Completo de Módulos PATCO

### 1. patco_suite (Orquestador Principal)
- **Ubicación:** `extra-addons/patco_suite/`
- **Versión:** 18.0.1.0.0
- **Estado:** ✅ Funcional
- **Rol:** Módulo orquestador que instala toda la suite
- **Líneas Manifest:** 75
- **Dependencias Principales:**
  - Módulos base: base, sale_management, account, hr, hr_skills, maintenance, contacts
  - Módulos PATCO: patco_hr_skills, patco_core, patco_customer_equipment, patco_hr_fsm_integration
  - Módulos OCA: fieldservice, fieldservice_*, agreement, helpdesk_mgmt
- **Características:**
  - Instalación automática de dependencias en orden correcto
  - Post-init hook para configuración
  - Application=True (módulo principal)

### 2. patco_core (Módulo Sobrecargado - CRÍTICO)
- **Ubicación:** `extra-addons/patco_core/`
- **Versión:** 18.0.1.0.0
- **Estado:** ✅ Funcional pero SOBRECARGADO
- **Líneas Manifest:** 89
- **Problema Identificado:** Múltiples responsabilidades mezcladas
- **Contenido Actual:**
  - Clasificaciones PATCO (nature, area, complexity)
  - Extensiones FSM (fsm_order, worksheets)
  - Control de tiempo (account_analytic_line)
  - Gestión de stock (stock_location, transfer_request)
  - Configuraciones de seguridad
  - Datos maestros
  - 25+ archivos de vistas
- **Dependencias:** 15+ módulos OCA y Odoo
- **Archivos Críticos:**
  - `models/`: 10+ archivos de modelos
  - `data/`: 15+ archivos de datos
  - `views/`: 12+ archivos de vistas
  - `wizards/`: Múltiples wizards

### 3. patco_customer_equipment (Bien Estructurado)
- **Ubicación:** `extra-addons/patco_customer_equipment/`
- **Versión:** 18.0.1.0.0
- **Estado:** ✅ Funcional y bien estructurado
- **Líneas Manifest:** 62
- **Responsabilidad:** Gestión de activos de cliente con QR
- **Características:**
  - Códigos QR únicos para equipos
  - Trazabilidad de servicios
  - Reportes de etiquetas
  - Integración con helpdesk y FSM
- **Dependencias:** Claras y específicas
- **Evaluación:** MANTENER sin cambios mayores

### 4. patco_hr_fsm_integration (Específico y Cohesivo)
- **Ubicación:** `extra-addons/patco_hr_fsm_integration/`
- **Versión:** 18.0.1.0.0
- **Estado:** ✅ Funcional
- **Líneas Manifest:** 39
- **Responsabilidad:** Sincronización HR-FSM
- **Características:**
  - Creación automática de fsm.person
  - Sincronización bidireccional
  - Cron job de mantenimiento
- **Evaluación:** MANTENER, posible mejora menor

### 5. patco_hr_skills (Funcional, Mejora Necesaria)
- **Ubicación:** `extra-addons/patco_hr_skills/`
- **Versión:** 18.0.1.0.0
- **Estado:** ✅ Funcional
- **Líneas Manifest:** 37
- **Responsabilidad:** Habilidades técnicas HORECA
- **Problema Identificado:** Falta integración con fieldservice_skill
- **Contenido:**
  - Tipos de habilidades HORECA (COC, REF, LAV, ELEC, FONT)
  - Niveles de competencia
  - Datos maestros de habilidades
- **Evaluación:** MEJORAR integración FSM

### 6. fieldservice_sale_timesheet (Candidato a Deprecación)
- **Ubicación:** `extra-addons/fieldservice_sale_timesheet/`
- **Versión:** 18.0.1.0.0
- **Estado:** ✅ Funcional
- **Líneas Manifest:** 23
- **Responsabilidad:** Puente FSM-Timesheet
- **Problema:** Funcionalidad duplicada con patco_core
- **Evaluación:** DEPRECAR, mover funcionalidad a módulos especializados

## Análisis de Dependencias Actuales

### Grafo de Dependencias
```
patco_suite (ORQUESTADOR)
├── patco_hr_skills (INDEPENDIENTE)
├── patco_core (SOBRECARGADO)
│   ├── fieldservice
│   ├── helpdesk_mgmt
│   ├── agreement
│   ├── maintenance
│   └── hr_timesheet
├── patco_customer_equipment
│   ├── patco_core (DEPENDENCIA)
│   ├── helpdesk_mgmt
│   └── fieldservice
├── patco_hr_fsm_integration
│   ├── patco_hr_skills (DEPENDENCIA)
│   ├── fieldservice
│   └── fieldservice_skill
└── fieldservice_sale_timesheet
    ├── patco_core (DEPENDENCIA)
    ├── fieldservice_sale
    └── hr_timesheet
```

### Problemas de Dependencias Identificados
1. **patco_core como dependencia central:** Todos dependen del módulo sobrecargado
2. **Dependencias circulares potenciales:** Entre módulos PATCO
3. **Falta de modularidad:** No se pueden instalar módulos independientemente
4. **Duplicación de funcionalidades:** Entre patco_core y fieldservice_sale_timesheet

## Estructura de Archivos por Módulo

### patco_core (CRÍTICO - Refactorización Necesaria)
```
patco_core/
├── models/ (10+ archivos)
│   ├── patco_service_nature.py ➜ MOVER a patco_base
│   ├── patco_service_area.py ➜ MOVER a patco_base
│   ├── patco_service_complexity.py ➜ MOVER a patco_base
│   ├── fsm_order.py ➜ MOVER a patco_fsm
│   ├── fsm_worksheet.py ➜ MOVER a patco_worksheets
│   ├── account_analytic_line.py ➜ MOVER a patco_timesheet
│   ├── stock_*.py ➜ MOVER a patco_stock_fsm
│   └── ...
├── data/ (15+ archivos)
│   ├── patco_service_*_data.xml ➜ MOVER a patco_base
│   ├── stock_*_data.xml ➜ MOVER a patco_stock_fsm
│   └── ...
├── views/ (12+ archivos)
│   ├── fsm_*_views.xml ➜ MOVER según funcionalidad
│   └── ...
└── wizards/ ➜ DISTRIBUIR según funcionalidad
```

### Módulos Bien Estructurados (MANTENER)
- **patco_customer_equipment:** Estructura clara, responsabilidad específica
- **patco_hr_fsm_integration:** Cohesivo, funcionalidad delimitada
- **patco_hr_skills:** Base sólida, necesita mejoras menores

## Plan de Migración Identificado

### Arquitectura Objetivo
```
patco_suite (ORQUESTADOR)
├── patco_base (NUEVO - Fundación)
│   ├── Clasificaciones PATCO
│   ├── Configuraciones base
│   └── Datos maestros
├── patco_fsm (NUEVO - Field Service)
│   ├── Extensiones fsm_order
│   ├── Worksheets
│   └── Funcionalidades FSM
├── patco_timesheet (NUEVO - Control Tiempo)
│   ├── account_analytic_line
│   └── Reportes tiempo
├── patco_stock_fsm (NUEVO - Inventario Campo)
│   ├── Stock en vehículos
│   ├── Transfer requests
│   └── Consumo repuestos
├── patco_worksheets (NUEVO - Documentos)
│   ├── Plantillas digitales
│   ├── Firmas
│   └── Aprobaciones
├── patco_customer_equipment (MANTENER)
├── patco_hr_skills (MEJORAR)
└── patco_hr_fsm_integration (MANTENER)
```

## Riesgos Identificados

### Alto Riesgo
1. **Refactorización de patco_core:** Módulo crítico con múltiples dependencias
2. **Migración de datos:** Preservar datos existentes durante la separación
3. **Dependencias cruzadas:** Resolver dependencias circulares

### Medio Riesgo
1. **Sincronización de módulos:** Mantener compatibilidad durante migración
2. **Tests de regresión:** Asegurar funcionalidad existente

### Bajo Riesgo
1. **Módulos bien estructurados:** patco_customer_equipment, patco_hr_fsm_integration
2. **Deprecación controlada:** fieldservice_sale_timesheet

## Validaciones Realizadas

### ✅ Backup Completado
- [x] Branch `backup/pre-refactoring` creado
- [x] Commit completo del estado funcional
- [x] Branch de trabajo `refactoring/modular-architecture` creado

### ✅ Inventario de Módulos
- [x] 6 módulos PATCO identificados
- [x] Manifests analizados
- [x] Dependencias documentadas
- [x] Estructura de archivos mapeada

### ⏳ Pendiente
- [ ] Verificación de funcionamiento del sistema
- [ ] Creación de tests de compatibilidad
- [ ] Documentación de configuración actual

## Conclusiones de la Fase 0

### Estado Actual Preservado
- **Sistema funcional:** Todos los módulos están operativos
- **Backup seguro:** Estado actual preservado en branch dedicado
- **Documentación completa:** Inventario detallado realizado

### Problemas Confirmados
- **patco_core sobrecargado:** Confirma necesidad de refactorización
- **Dependencias complejas:** Requiere reorganización cuidadosa
- **Duplicación de código:** Entre módulos identificada

### Preparación para Fase 1
- **Arquitectura objetivo definida:** Plan de módulos especializados
- **Riesgos identificados:** Estrategias de mitigación planificadas
- **Enfoque conservador:** Preservación de funcionalidad garantizada

---

**Próximo Paso:** Iniciar Fase 1 - Creación de `patco_base` como fundación modular
**Responsable:** Equipo de desarrollo PATCO
**Fecha Objetivo:** Según cronograma de hoja de ruta