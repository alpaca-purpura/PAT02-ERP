# PATCO Core - Funcionalidades Centrales del Sistema

## Descripción

PATCO Core es el módulo central del ecosistema PATCO que proporciona las funcionalidades fundamentales para la digitalización de operaciones de mantenimiento HORECA (Hoteles, Restaurantes y Cafeterías). Este módulo extiende las capacidades de Field Service de Odoo con características específicas para el sector de mantenimiento de equipos comerciales.

## Función en el Ecosistema PATCO

Este módulo actúa como el núcleo funcional del sistema PATCO, proporcionando:

- **Clasificación de Servicios**: Sistema de naturalezas de servicio para categorizar trabajos
- **Gestión Avanzada de Órdenes**: Extensiones a las órdenes de servicio con campos específicos PATCO
- **Checklists Digitales**: Sistema de verificación para garantizar calidad del servicio
- **Gestión de Stock en Vehículos**: Control de repuestos y materiales en vehículos de técnicos
- **Integración con Hojas de Trabajo**: Base para el registro de tiempo y actividades
- **Base de Conocimiento**: Acceso rápido a información técnica durante el servicio

## Dependencias del Módulo

### Módulos Odoo Core
- `base`
- `fieldservice`
- `stock`
- `hr`
- `knowledge` (opcional)

### Módulos OCA
- `fieldservice_stock`
- `fieldservice_skill`
- `fieldservice_account_analytic`

## Funcionalidades Principales

### 1. Modelo de Naturaleza de Servicio (patco.service.nature)

#### Características
- **Código único**: Identificador alfanumérico para cada naturaleza
- **Nombre descriptivo**: Descripción clara del tipo de servicio
- **Secuenciación**: Orden de presentación en interfaces
- **Validación**: Restricciones de unicidad para código y nombre

#### Casos de Uso
- Clasificación de servicios (Preventivo, Correctivo, Instalación, etc.)
- Reportes por tipo de servicio
- Asignación automática basada en naturaleza
- Análisis de tendencias de mantenimiento

### 2. Extensión de Órdenes de Servicio (fsm.order)

#### Campos Agregados
- **Naturaleza del Servicio**: Clasificación del tipo de trabajo
- **Área de Servicio**: Zona específica donde se realiza el trabajo
- **Complejidad**: Nivel de dificultad del servicio (Baja, Media, Alta)
- **Checklist de Verificación**: Lista de tareas a completar
- **Observaciones del Checklist**: Notas adicionales sobre verificaciones
- **Vehículo Asignado**: Vehículo del técnico para gestión de stock

#### Funcionalidades Avanzadas
- **Consumo de Repuestos**: Botón para registrar materiales utilizados
- **Acceso a Base de Conocimiento**: Enlace directo a información técnica
- **Validación de Campos**: Controles de integridad de datos
- **Integración con Stock**: Movimientos automáticos de inventario

### 3. Gestión de Stock en Vehículos

#### Características
- Asignación de vehículos a órdenes de servicio
- Control de inventario móvil
- Registro de consumos en campo
- Trazabilidad de materiales utilizados

#### Beneficios
- Optimización de rutas de reabastecimiento
- Control preciso de costos por servicio
- Reducción de tiempos muertos por falta de repuestos
- Mejora en la planificación de inventarios

### 4. Sistema de Checklists

#### Funcionalidad
- Listas de verificación personalizables por tipo de servicio
- Registro de cumplimiento de tareas
- Observaciones específicas por ítem
- Validación de completitud antes del cierre

#### Aplicaciones
- Verificaciones de seguridad
- Controles de calidad
- Procedimientos estándar
- Cumplimiento normativo

## Configuración Necesaria

### Configuración Inicial
1. **Naturalezas de Servicio**: Crear las clasificaciones necesarias
   - Mantenimiento Preventivo
   - Mantenimiento Correctivo
   - Instalación
   - Garantía
   - Emergencia

2. **Áreas de Servicio**: Definir zonas de trabajo
   - Cocina
   - Comedor
   - Bar
   - Almacén
   - Área Técnica

3. **Niveles de Complejidad**: Configurar escalas
   - Baja: Servicios rutinarios
   - Media: Servicios especializados
   - Alta: Servicios complejos o críticos

### Configuración de Vehículos
1. Registrar vehículos de la flota
2. Asignar técnicos a vehículos
3. Configurar ubicaciones de stock móvil
4. Establecer niveles mínimos de inventario

## Relación con Otros Módulos del Ecosistema

### Integración con patco_hr_skills
- Las naturalezas de servicio se relacionan con habilidades requeridas
- Asignación automática basada en competencias del técnico
- Validación de capacidades antes de asignación

### Integración con patco_customer_equipment
- Órdenes de servicio vinculadas a equipos específicos
- Historial de servicios por activo
- Programación de mantenimientos preventivos

### Integración con fieldservice_timesheet
- Registro de tiempo por naturaleza de servicio
- Análisis de productividad por tipo de trabajo
- Costeo preciso de servicios

### Integración con fieldservice_sale_timesheet
- Facturación diferenciada por naturaleza
- Precios específicos por complejidad
- Integración con contratos de mantenimiento

## Casos de Uso Específicos

### Según el Documento Funcional

#### MACRO-PROCESO 2: Operaciones de Servicio

**Clasificación y Asignación**
- Recepción de tickets con naturaleza de servicio
- Asignación automática basada en habilidades y complejidad
- Planificación optimizada de rutas

**Gestión de Recursos**
- Control de stock en vehículos
- Asignación de materiales por tipo de servicio
- Optimización de inventarios móviles

#### MACRO-PROCESO 3: Ejecución en Campo

**Trabajo Estructurado**
- Checklists específicos por naturaleza de servicio
- Registro sistemático de actividades
- Validación de procedimientos estándar

**Control de Calidad**
- Verificaciones obligatorias por tipo de trabajo
- Documentación de observaciones
- Trazabilidad completa del servicio

**Gestión de Materiales**
- Consumo directo desde vehículo
- Registro automático de costos
- Control de inventario en tiempo real

#### MACRO-PROCESO 4: Cierre y Análisis

**Análisis de Servicios**
- Reportes por naturaleza de servicio
- Análisis de tendencias por complejidad
- Métricas de eficiencia por área

**Optimización Continua**
- Identificación de patrones de fallas
- Mejora de procedimientos
- Optimización de recursos

## Tipos de Usuario y Permisos

### PATCO Administrador
- Configuración de naturalezas de servicio
- Gestión de checklists
- Configuración de vehículos y stock
- Acceso a todos los reportes

### PATCO Líder Técnico
- Asignación de órdenes de servicio
- Supervisión de checklists
- Gestión de inventarios móviles
- Reportes operacionales

### PATCO Técnico
- Ejecución de órdenes asignadas
- Completado de checklists
- Consumo de repuestos
- Acceso a base de conocimiento

## Flujos de Trabajo Principales

### 1. Creación de Orden de Servicio
1. Selección de naturaleza de servicio
2. Definición de área y complejidad
3. Asignación de técnico y vehículo
4. Generación de checklist automático

### 2. Ejecución en Campo
1. Acceso a información del equipo
2. Consulta de base de conocimiento
3. Ejecución de checklist
4. Consumo de repuestos
5. Registro de observaciones

### 3. Cierre de Servicio
1. Validación de checklist completo
2. Confirmación de consumos
3. Registro de tiempo total
4. Generación de reporte de servicio

## Métricas y KPIs Soportados

### Operacionales
- Tiempo promedio por naturaleza de servicio
- Tasa de completitud de checklists
- Consumo de materiales por tipo de trabajo
- Eficiencia por técnico y área

### Estratégicos
- Distribución de servicios por naturaleza
- Tendencias de complejidad
- Optimización de inventarios móviles
- Análisis de productividad

## Beneficios del Módulo

1. **Estandarización**: Procedimientos uniformes para todos los servicios
2. **Trazabilidad**: Registro completo de actividades y recursos
3. **Eficiencia**: Optimización de tiempos y recursos
4. **Calidad**: Garantía de cumplimiento de estándares
5. **Control**: Visibilidad completa de operaciones
6. **Análisis**: Base de datos para mejora continua

## Versión

Compatible con Odoo 18 Community Edition.

## Soporte Técnico

Este módulo requiere configuración inicial y puede necesitar personalización según las necesidades específicas del negocio. Se recomienda trabajar con un consultor especializado en PATCO para la implementación óptima.