# PATCO - Solución Integral de Mantenimiento HORECA

## Descripción del Proyecto

PATCO es una solución completa de digitalización para operaciones de mantenimiento en el sector HORECA (Hoteles, Restaurantes y Cafeterías), construida sobre Odoo 18 Community. El sistema optimiza todo el ciclo de vida del servicio técnico, desde la recepción del ticket hasta la facturación, integrando gestión de activos, competencias técnicas y operaciones de campo.

## Arquitectura de Módulos

La arquitectura PATCO sigue principios de modularidad y separación de responsabilidades, organizando las funcionalidades en módulos especializados:

### 1. `patco_suite` - Orquestador Principal
- **Propósito**: Módulo meta que coordina la instalación completa del ecosistema PATCO
- **Funcionalidad**: Instalación automática de todos los componentes con sus dependencias OCA
- **Dependencias**: `patco_core`, `patco_customer_equipment`, `patco_hr_skills`
- **Beneficio**: Despliegue simplificado con un solo clic

### 2. `patco_core` - Motor Central
- **Propósito**: Núcleo del sistema con funcionalidades base y modelos centrales
- **Modelos principales**:
  - `patco.service.nature`: Clasificación de servicios (Correctivo, Preventivo, Instalación, Inspección)
  - Extensiones de `account.analytic.line`: Gestión de tiempos FSM con timers
  - Extensiones de `maintenance.equipment.category`: Categorización de equipos HORECA
- **Datos iniciales**: Naturalezas de servicio preconfiguradas según matriz PATCO

### 3. `patco_customer_equipment` - Gestión de Activos
- **Propósito**: Administración especializada de equipos de clientes HORECA
- **Funcionalidades clave**:
  - Códigos QR automáticos para identificación de equipos
  - Campos personalizados: código PATCO, cliente, ubicación, estado operativo
  - Integración con `helpdesk.ticket` y `fsm.order`
  - Cómputo automático de estadísticas de servicio
  - Validaciones de integridad de datos

### 4. `patco_hr_skills` - Matriz de Competencias
- **Propósito**: Sistema de habilidades técnicas especializado para HORECA
- **Integración**: Extiende `fieldservice_skill` de OCA
- **Tipos de habilidades**: COC (Cocina), REF (Refrigeración), AC (Aire Acondicionado), etc.
- **Niveles de competencia**: Básico, Intermedio, Avanzado, Experto

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

- **`fieldservice`**: Gestión de órdenes de servicio de campo
- **`fieldservice_skill`**: Sistema de habilidades técnicas
- **`fieldservice_sale_timesheet`**: Módulo puente para integración timesheet (funcionalidad en patco_core)
- **`agreement`**: Gestión de contratos y acuerdos
- **`helpdesk`**: Sistema de tickets de soporte

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
# - patco_core (modelos base)
# - patco_customer_equipment (gestión de activos)
# - patco_hr_skills (competencias técnicas)
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

### Naturalezas de Servicio (`patco.service.nature`)
- **M1-Correctivo**: Reparación de fallas
- **M2-Preventivo**: Mantenimiento programado
- **M3-Instalación**: Nuevos equipos
- **M4-Inspección**: Revisiones técnicas

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