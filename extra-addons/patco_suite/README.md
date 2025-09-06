# PATCO Suite - Módulo Orquestador Principal

## Descripción

PATCO Suite es el módulo orquestador principal del ecosistema PATCO, diseñado para simplificar la instalación y configuración de la solución completa de digitalización de operaciones de mantenimiento HORECA (Hoteles, Restaurantes y Cafeterías) en Odoo 18 Community.

## Función en el Ecosistema PATCO

Este módulo actúa como el punto de entrada único para instalar todo el ecosistema PATCO. Su función principal es:

- **Orquestación de Instalación**: Instala automáticamente todos los módulos PATCO y sus dependencias OCA en el orden correcto
- **Resolución de Dependencias**: Garantiza que todos los módulos OCA de Field Service se instalen antes que los módulos PATCO
- **Configuración Base**: Proporciona la infraestructura técnica necesaria para el funcionamiento del ecosistema
- **Simplificación del Despliegue**: Permite instalar toda la solución PATCO con un solo clic

## Dependencias del Módulo

### Módulos Odoo Core
- `base`
- `fieldservice`
- `account`
- `hr`
- `maintenance`
- `helpdesk`

### Módulos OCA (Instalados Automáticamente)
- `fieldservice_account_analytic`
- `fieldservice_skill`
- `fieldservice_stock`
- `fieldservice_sale`
- `fieldservice_agreement`
- `agreement`
- `maintenance_equipment_category_hierarchy`

### Módulos PATCO (Instalados Automáticamente)
- `patco_core`
- `patco_hr_skills`
- `patco_customer_equipment`
- `fieldservice_sale_timesheet`


## Funcionalidades Principales

### 1. Extensión del Modelo Account Analytic Line
- Agrega el campo `fsm_order_id` necesario para la integración entre órdenes de servicio y líneas analíticas
- Resuelve el error "column a.fsm_order_id does not exist" que ocurre en instalaciones limpias

### 2. Hook de Post-Instalación
- Verifica automáticamente la instalación correcta de todos los módulos PATCO
- Valida la existencia del campo `fsm_order_id` en `account.analytic.line`
- Proporciona logging detallado del proceso de instalación

### 3. Gestión de Dependencias
- Instala módulos OCA en el orden correcto para evitar errores de dependencias
- Maneja la instalación de módulos PATCO después de establecer la base OCA

## Configuración Necesaria

### Instalación
1. Asegúrese de que todos los módulos OCA estén disponibles en el addons_path
2. Instale únicamente el módulo `patco_suite`
3. El sistema instalará automáticamente todas las dependencias

### Post-Instalación
- No se requiere configuración adicional
- Todos los módulos PATCO estarán disponibles y configurados
- Los menús y funcionalidades estarán accesibles según los permisos de usuario

## Relación con Otros Módulos del Ecosistema

### Módulos Centrales
- **patco_core**: Proporciona las funcionalidades centrales del sistema PATCO
- **patco_hr_skills**: Gestiona la matriz de competencias de técnicos
- **patco_customer_equipment**: Maneja el registro maestro de activos de clientes

### Módulos de Integración
- **fieldservice_sale_timesheet**: Integra hojas de tiempo con el proceso de facturación


## Casos de Uso Específicos

### Según el Documento Funcional

#### MACRO-PROCESO 1: Comercial, Contratos y Onboarding
- Facilita la instalación de módulos necesarios para gestión de clientes y acuerdos
- Habilita la matriz de competencias de técnicos
- Proporciona la base para el registro de activos de cliente

#### MACRO-PROCESO 2: Operaciones de Servicio
- Instala los módulos de Mesa de Ayuda y Servicios de Campo
- Configura la integración entre tickets y órdenes de servicio
- Habilita la asignación basada en habilidades

#### MACRO-PROCESO 3: Ejecución en Campo
- Proporciona la infraestructura para hojas de trabajo digitales
- Habilita el registro de tiempo y consumo de repuestos
- Facilita la captura de firma del cliente

#### MACRO-PROCESO 4: Cierre, Facturación y Cobranza
- Instala los módulos necesarios para facturación automática
- Configura la integración con contabilidad
- Habilita el seguimiento de cuentas por cobrar

## Tipos de Usuario Soportados

### Administrador del Sistema (PATCO Administrador)
- Acceso completo a la configuración del ecosistema
- Capacidad de gestionar todos los módulos instalados

### Gerente/Líder de Servicio (PATCO Líder Técnico)
- Acceso a herramientas de coordinación y planificación
- Supervisión de operaciones diarias

### Técnico de Campo (PATCO Técnico)
- Acceso a órdenes de servicio asignadas
- Interfaz móvil optimizada para trabajo en campo

## Beneficios de la Instalación Orquestada

1. **Simplicidad**: Un solo módulo para instalar toda la solución
2. **Confiabilidad**: Instalación en orden correcto sin errores de dependencias
3. **Completitud**: Garantiza que todos los componentes necesarios estén presentes
4. **Mantenibilidad**: Facilita actualizaciones y mantenimiento del ecosistema
5. **Trazabilidad**: Logging completo del proceso de instalación

## Soporte y Mantenimiento

Este módulo es parte integral del ecosistema PATCO y debe mantenerse actualizado junto con los demás componentes. Cualquier modificación debe considerar el impacto en todo el ecosistema.

## Versión

Compatible con Odoo 18 Community Edition.