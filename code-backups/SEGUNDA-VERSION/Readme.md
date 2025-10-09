# PATCO - Solución Integral de Mantenimiento HORECA

## Descripción del Proyecto

PATCO es una solución completa de digitalización para operaciones de mantenimiento en el sector HORECA (Hoteles, Restaurantes y Cafeterías), construida sobre Odoo 18 Community. El sistema optimiza todo el ciclo de vida del servicio técnico, desde la recepción del ticket hasta la facturación, integrando gestión de activos, competencias técnicas y operaciones de campo.

## Arquitectura de Módulos

La arquitectura PATCO sigue principios de modularidad y separación de responsabilidades, organizando las funcionalidades en módulos especializados:

### 1. `patco_suite` - Solución Completa de Mantenimiento HORECA
- **Propósito**: Suite completa de módulos PATCO para gestión de mantenimiento en sector HORECA
- **Funcionalidad**: 
  - Instalación automática de dependencias OCA en orden correcto
  - Configuración de campos faltantes (fsm_order_id en account_analytic_line)
  - Gestión centralizada de la suite completa
  - Cumple con documento_funcional_wannabe.md
- **Dependencias**: `patco_base`, `patco_skills_mgmt`, `patco_equipment`, `patco_fsm`, `patco_stock_fsm`, `patco_timesheet`
- **Beneficio**: Instalación automática de todos los módulos PATCO necesarios con sus dependencias en el orden correcto
- **Categoría**: Services/Field Service

### 2. `patco_base` - Core Functionalities and Base Models
- **Propósito**: Módulo base que proporciona las funcionalidades fundamentales para el sistema PATCO
- **Funcionalidades principales**:
  - Clasificación de Áreas de Servicio
  - Niveles de Complejidad de Servicio
  - Tipos de Naturaleza de Servicio
  - Clasificación de Órdenes de Servicio (Helpdesk & FSM)
  - Extensiones de Categorías de Equipos de Mantenimiento
  - Grupos de seguridad y permisos
  - Categorías de productos para servicios de mantenimiento
  - Configuraciones maestras y modelos base
- **Dependencias**: `base`, `product`, `maintenance`, `web_responsive`, `mail_debrand`, `disable_odoo_online`
- **Categoría**: Services/Field Service

### 3. `patco_equipment` - Gestión Avanzada de Equipos
- **Propósito**: Gestión avanzada de equipos y categorías para servicios técnicos
- **Funcionalidades clave**:
  - Categorías de equipos con plantillas de checklist personalizables
  - Base de conocimiento integrada por categoría de equipo
  - Plantillas HTML para checklists de entrada y salida
  - Gestión de documentación técnica mediante adjuntos
  - Integración con módulos de mantenimiento y FSM
  - Categorías predefinidas: Cocina, Refrigeración, Lavandería, Bar/Cafetería, Sistemas Eléctricos
- **Dependencias**: `base`, `maintenance`, `maintenance_equipment_category_hierarchy`
- **Categoría**: Maintenance

### 4. `patco_fsm` - Field Service Management
- **Propósito**: Extensiones PATCO para Field Service Management
- **Funcionalidades principales**:
  - Órdenes de servicio en campo (FSM)
  - Listas de verificación personalizadas
  - Consumo de partes y materiales
  - Hojas de trabajo digitales
  - Integración con equipos de clientes
- **Dependencias**: `base`, `patco_base`, `patco_core`, `fieldservice`, `fieldservice_skill`, `maintenance`, `helpdesk_mgmt`
- **Categoría**: Field Service
- **Nota**: Migrado desde patco_core como parte de la reestructuración modular

### 5. `patco_skills_mgmt` - Gestión Avanzada de Habilidades
- **Propósito**: Gestión avanzada de habilidades y competencias técnicas
- **Funcionalidades clave**:
  - Catálogo de habilidades técnicas por categorías
  - Niveles de competencia y certificaciones
  - Asignación de habilidades a empleados
  - Evaluación y seguimiento de competencias
  - Integración con órdenes de servicio FSM
  - Reportes de capacidades del equipo técnico
  - Gestión de habilidades requeridas por tipo de servicio
  - Matching automático de técnicos por competencias
  - Seguimiento de certificaciones y vencimientos
  - Planes de capacitación y desarrollo
  - Análisis de brechas de habilidades
- **Dependencias**: `base`, `hr`, `hr_skills`, `fieldservice`, `patco_base`
- **Categoría**: Human Resources

### 6. `patco_stock_fsm` - Gestión de Stock para Servicios de Campo
- **Propósito**: Gestión de Stock para Servicios de Campo PATCO
- **Funcionalidades principales**:
  - Gestión de ubicaciones de vehículos
  - Transferencias de stock a vehículos
  - Control de inventario móvil
  - Integración con órdenes de servicio FSM
- **Dependencias**: `base`, `stock`, `fieldservice`, `fieldservice_stock`, `patco_base`
- **Categoría**: Field Service

### 7. `patco_timesheet` - Extensiones de Registro de Tiempo
- **Propósito**: Extensiones de timesheet para Field Service Management PATCO
- **Funcionalidades clave**:
  - Extensiones del modelo account.analytic.line con campos FSM
  - Sistema de timer integrado para técnicos de campo
  - Reportes de análisis de timesheet con datos FSM
  - Integración con órdenes de servicio FSM
  - Vistas especializadas para registro de tiempo en campo
- **Dependencias**: `patco_base`, `hr_timesheet`, `fieldservice`
- **Categoría**: Services/Timesheets

## Macro-Procesos Implementados

El sistema digitaliza el flujo completo de operaciones de mantenimiento HORECA:

### 1. Ciclo Comercial
- **Formalización de Acuerdos**: Integración con módulo `agreement` de OCA
- **Onboarding de Activos**: Registro masivo de equipos con códigos QR
- **Gestión de Contratos**: Vinculación de activos a acuerdos comerciales

### 2. Flujo Operativo
- **Recepción de Tickets**: `helpdesk.ticket` como punto de entrada
- **Clasificación PATCO**: Naturaleza, área y complejidad del servicio
- **Conversión a FSM**: Generación automática de `fsm.order`
- **Asignación por Competencias**: Filtrado de técnicos según habilidades

### 3. Gestión de Inventario
- **Arquitectura de Furgonetas**: Ubicaciones específicas por vehículo (WH/Stock/Vans/VAN-001)
- **Reabastecimiento**: Transferencias internas automatizadas
- **Verificación de Stock**: Disponibilidad en tiempo real por técnico

### 4. Ejecución en Campo
- **Interfaz Móvil**: Odoo responsive para gestión oficial
- **Preparado para IA**: Estructura para integración con asistente Telegram
- **Registro de Tiempos**: Timesheets integrados con FSM
- **Consumo de Materiales**: Control de stock por furgoneta

### 5. Cierre y Facturación
- **Conformidad Dual**: Operativa (campo) y administrativa (formal)
- **Gestión de OC**: Recepción y validación de órdenes de compra
- **Facturación Automatizada**: Generación basada en materiales y horas reales
- **Control de Cobranza**: Seguimiento de pagos y detracciones

## Dependencias OCA Integradas

El sistema aprovecha módulos especializados de la Odoo Community Association:

### Dependencias Principales
- **`fieldservice`**: Gestión de órdenes de servicio de campo (usado por patco_fsm, patco_skills_mgmt, patco_stock_fsm, patco_timesheet)
- **`fieldservice_skill`**: Sistema de habilidades técnicas (usado por patco_fsm)
- **`fieldservice_stock`**: Integración de stock con FSM (usado por patco_stock_fsm)
- **`hr_timesheet`**: Registro de tiempos (extendido por patco_timesheet)
- **`hr_skills`**: Gestión de habilidades de empleados (usado por patco_skills_mgmt)
- **`maintenance`**: Gestión de mantenimiento (usado por patco_base, patco_fsm)
- **`maintenance_equipment_category_hierarchy`**: Jerarquía de categorías de equipos (usado por patco_equipment)

### Dependencias de Interfaz y Funcionalidad
- **`web_responsive`**: Interfaz responsive (usado por patco_base)
- **`mail_debrand`**: Eliminación de branding de Odoo en emails (usado por patco_base)
- **`disable_odoo_online`**: Deshabilitación de funciones online de Odoo (usado por patco_base)
- **`helpdesk_mgmt`**: Sistema de tickets de soporte (usado por patco_fsm)
- **`partner_firstname`**: Gestión de nombres de contactos (usado por patco_suite)
- **`base_location`**: Gestión de ubicaciones (usado por patco_suite)
- **`base_location_geonames_import`**: Importación de datos geográficos (usado por patco_suite)
- **`web_widget_x2many_2d_matrix`**: Widget de matriz 2D (usado por patco_suite)

## Beneficios de la Arquitectura Modular

### Técnicos
- **Separación de Responsabilidades**: Cada módulo tiene un propósito específico
- **Eliminación de Dependencias Circulares**: Flujo unidireccional limpio
- **Reutilización de Código**: Componentes centralizados en `patco_core`
- **Escalabilidad**: Preparado para futuras expansiones
- **Mantenibilidad**: Código organizado y documentado

### Operativos
- **Instalación Simplificada**: Un solo módulo instala todo el ecosistema
- **Flexibilidad de Despliegue**: Posibilidad de instalación modular
- **Integración Nativa**: Aprovecha funcionalidades estándar de Odoo
- **Preparación para IA**: Estructura lista para asistente inteligente

## Instalación y Configuración

### Instalación Completa (Recomendada)
```bash
# Instalar el orquestador principal
Módulo a instalar: patco_suite

# Esto instalará automáticamente:
# - patco_base (funcionalidades base)
# - patco_equipment (gestión de equipos)
# - patco_fsm (órdenes de servicio)
# - patco_skills_mgmt (gestión de habilidades)
# - patco_stock_fsm (integración stock-FSM)
# - patco_timesheet (registro de tiempos)
# - Todas las dependencias OCA necesarias
```

### Configuración Inicial
1. **Datos Maestros**: Las naturalezas de servicio se cargan automáticamente
2. **Tipos de Habilidades**: Configurar competencias HORECA específicas
3. **Ubicaciones de Furgonetas**: Crear ubicaciones por vehículo
4. **Empleados**: Asignar habilidades técnicas a técnicos
5. **Equipos**: Registrar activos de clientes con códigos QR

### Flujo de Uso
1. **Recepción**: Crear ticket en Helpdesk
2. **Clasificación**: Aplicar matriz PATCO (naturaleza, área, complejidad)
3. **Conversión**: Generar orden FSM desde ticket
4. **Asignación**: Seleccionar técnico por competencias
5. **Ejecución**: Gestión móvil de la orden
6. **Cierre**: Conformidad y facturación

## Estructura de Datos PATCO

### Tipos de Servicio HORECA
- **Correctivo**: Reparación de fallas y averías
- **Preventivo**: Mantenimiento programado y rutinario
- **Instalación**: Montaje de nuevos equipos
- **Inspección**: Revisiones técnicas y auditorías

### Áreas de Servicio (Configurables)
- **COC-CAL**: Cocina - Calor
- **COC-PRE**: Cocina - Preparación
- **COC-LAV**: Cocina - Lavado
- **REF-COM**: Refrigeración Comercial
- **AC**: Aire Acondicionado
- **LAV**: Lavandería Industrial
- **ELEC**: Eléctrico
- **FONT**: Fontanería

### Niveles de Complejidad
- **N1-Básico**: Servicios rutinarios
- **N2-Intermedio**: Reparaciones estándar
- **N3-Avanzado**: Intervenciones especializadas
- **N4-Crítico**: Servicios de alta complejidad

## Validación de Arquitectura

✅ **Modularidad**: Responsabilidades claramente definidas
✅ **Integración OCA**: Aprovecha estándares de la comunidad
✅ **Escalabilidad**: Preparado para crecimiento
✅ **Mantenibilidad**: Código limpio y documentado
✅ **Flexibilidad**: Instalación completa o modular
✅ **Preparación IA**: Estructura para asistente inteligente

---

*PATCO - Digitalizando el mantenimiento HORECA con Odoo 18 Community*