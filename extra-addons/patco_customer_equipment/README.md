# PATCO Customer Equipment - Gestión de Activos de Clientes

## Descripción

PATCO Customer Equipment es el módulo especializado en la gestión integral de activos y equipos de clientes dentro del ecosistema PATCO. Este módulo extiende las capacidades del módulo de mantenimiento de Odoo para proporcionar un registro maestro completo de equipos HORECA (Hoteles, Restaurantes y Cafeterías), incluyendo trazabilidad mediante códigos QR, historial de servicios y métricas de rendimiento.

## Función en el Ecosistema PATCO

Este módulo es el corazón del registro maestro de activos, proporcionando:

- **Registro Maestro de Equipos**: Base de datos completa de todos los activos de clientes
- **Trazabilidad con QR**: Identificación única y acceso rápido a información del equipo
- **Historial de Servicios**: Registro completo de mantenimientos y reparaciones
- **Métricas de Rendimiento**: KPIs de disponibilidad, confiabilidad y costos
- **Gestión de Ubicaciones**: Control preciso de ubicación de equipos en instalaciones del cliente
- **Integración con Servicios**: Vinculación directa con órdenes de servicio y tickets
- **Planificación Predictiva**: Base para mantenimientos preventivos y predictivos

## Dependencias del Módulo

### Módulos Odoo Core
- `base`
- `maintenance`
- `fieldservice`
- `helpdesk`
- `partner`

### Módulos OCA
- `maintenance_equipment_category_hierarchy`
- `fieldservice_maintenance`

### Módulos PATCO
- `patco_core` (para integración con órdenes de servicio)

## Funcionalidades Principales

### 1. Extensión del Modelo de Equipos (maintenance.equipment)

#### Campos Específicos PATCO
- **Código PATCO**: Identificador único interno del sistema
- **Cliente**: Relación directa con el partner propietario del equipo
- **Ubicación de Servicio**: Ubicación específica dentro de las instalaciones del cliente
- **Código QR**: Generado automáticamente para identificación rápida
- **Fecha de Instalación**: Control de antigüedad y garantías
- **Estado Operacional**: Operativo, Fuera de Servicio, En Mantenimiento

#### Campos Calculados
- **Número de Servicios**: Contador automático de servicios realizados
- **Fecha del Último Servicio**: Timestamp del último mantenimiento
- **Próximo Mantenimiento**: Cálculo automático basado en frecuencia
- **Tiempo Promedio de Servicio**: Métrica de eficiencia
- **Costo Total de Mantenimiento**: Acumulado de costos de servicios

### 2. Sistema de Códigos QR

#### Generación Automática
- Código QR único por equipo
- Generación automática al crear el equipo
- Regeneración manual cuando sea necesario
- Formato optimizado para lectura móvil

#### Información Codificada
- ID del equipo en el sistema
- Código PATCO del equipo
- URL de acceso directo a la ficha del equipo
- Información básica para trabajo offline

#### Casos de Uso del QR
- **Identificación Rápida**: Escaneo para acceso inmediato a información
- **Creación de Tickets**: Generación automática de tickets desde el equipo
- **Registro de Servicios**: Inicio directo de órdenes de servicio
- **Verificación de Ubicación**: Confirmación de que el técnico está en el equipo correcto

### 3. Gestión de Ubicaciones de Servicio

#### Estructura Jerárquica
- **Edificio/Sucursal**: Nivel superior de ubicación
- **Piso/Área**: Subdivisión del edificio
- **Zona Específica**: Ubicación exacta (Cocina, Comedor, Bar, etc.)
- **Posición**: Descripción detallada de la ubicación

#### Beneficios
- Localización rápida de equipos
- Optimización de rutas de técnicos
- Planificación eficiente de mantenimientos
- Control de acceso por áreas

### 4. Historial y Trazabilidad

#### Registro de Servicios
- Vinculación automática con órdenes de servicio
- Historial completo de mantenimientos
- Registro de repuestos utilizados
- Tiempo invertido por servicio
- Técnicos que han trabajado en el equipo

#### Métricas Automáticas
- **MTBF (Mean Time Between Failures)**: Tiempo promedio entre fallas
- **MTTR (Mean Time To Repair)**: Tiempo promedio de reparación
- **Disponibilidad**: Porcentaje de tiempo operativo
- **Costo por Hora de Operación**: Eficiencia económica

### 5. Integración con Tickets de Soporte

#### Creación Automática
- Generación de tickets desde códigos QR
- Vinculación automática equipo-ticket
- Información pre-poblada del equipo
- Escalamiento automático según criticidad

#### Seguimiento
- Estado de tickets por equipo
- Historial de incidencias
- Patrones de fallas
- Análisis de tendencias

## Configuración Necesaria

### Configuración Inicial de Equipos

1. **Categorías de Equipos HORECA**
   ```
   - Refrigeración
     - Cámaras frigoríficas
     - Vitrinas refrigeradas
     - Congeladores
   - Cocina
     - Hornos
     - Freidoras
     - Planchas
   - Ventilación
     - Campanas extractoras
     - Sistemas HVAC
   - Lavado
     - Lavavajillas
     - Sistemas de limpieza
   ```

2. **Estados Operacionales**
   - Operativo
   - Fuera de Servicio
   - En Mantenimiento
   - Pendiente de Instalación
   - Dado de Baja

3. **Tipos de Ubicación**
   - Cocina Principal
   - Cocina Auxiliar
   - Comedor
   - Bar/Cafetería
   - Almacén
   - Área Técnica
   - Oficinas

### Configuración de Códigos QR

1. **Formato de Códigos**
   - Tamaño optimizado para impresión
   - Nivel de corrección de errores
   - Formato de datos codificados

2. **Etiquetas Físicas**
   - Material resistente a ambientes HORECA
   - Tamaño apropiado para cada tipo de equipo
   - Información adicional impresa

### Configuración de Mantenimientos

1. **Frecuencias de Mantenimiento**
   - Mantenimiento preventivo por tipo de equipo
   - Calendarios de inspección
   - Alertas automáticas

2. **Procedimientos Estándar**
   - Checklists por tipo de equipo
   - Procedimientos de seguridad
   - Documentación técnica

## Relación con Otros Módulos del Ecosistema

### Integración con patco_core
- **Órdenes de Servicio**: Vinculación automática equipo-servicio
- **Naturalezas de Servicio**: Clasificación de trabajos por tipo de equipo
- **Checklists**: Procedimientos específicos por modelo de equipo

### Integración con patco_hr_skills
- **Habilidades Requeridas**: Cada equipo requiere habilidades específicas
- **Asignación de Técnicos**: Matching basado en experiencia con el tipo de equipo
- **Especialización**: Desarrollo de expertise por categoría de equipo

### Integración con fieldservice
- **Creación de Órdenes**: Generación automática desde equipos
- **Planificación**: Optimización basada en ubicación de equipos
- **Reportes**: Análisis de servicios por equipo y ubicación

### Integración con helpdesk
- **Tickets de Soporte**: Creación automática desde códigos QR
- **Escalamiento**: Basado en criticidad del equipo
- **SLA**: Tiempos de respuesta según tipo de equipo

## Casos de Uso Específicos

### Según el Documento Funcional

#### MACRO-PROCESO 1: Comercial y Onboarding

**Registro de Activos del Cliente**
- Inventario completo de equipos durante onboarding
- Generación de códigos QR para todos los equipos
- Configuración de ubicaciones y responsables
- Establecimiento de planes de mantenimiento

**Configuración de Servicios**
- Definición de SLAs por tipo de equipo
- Configuración de mantenimientos preventivos
- Asignación de técnicos especializados

#### MACRO-PROCESO 2: Operaciones de Servicio

**Identificación Rápida**
- Escaneo de QR para identificar equipo
- Acceso inmediato a historial de servicios
- Información técnica y manuales
- Contactos de emergencia

**Creación de Tickets**
- Generación automática desde código QR
- Pre-población de datos del equipo
- Clasificación automática por tipo de equipo
- Asignación basada en ubicación y habilidades

#### MACRO-PROCESO 3: Ejecución en Campo

**Verificación de Equipo**
- Confirmación de ubicación mediante QR
- Acceso a información técnica específica
- Historial de servicios anteriores
- Procedimientos de seguridad

**Registro de Servicios**
- Vinculación automática servicio-equipo
- Actualización de métricas de rendimiento
- Registro de repuestos utilizados
- Actualización de estado operacional

#### MACRO-PROCESO 4: Análisis y Optimización

**Análisis de Rendimiento**
- Métricas de disponibilidad por equipo
- Análisis de costos de mantenimiento
- Identificación de equipos problemáticos
- Optimización de frecuencias de mantenimiento

**Planificación Predictiva**
- Análisis de patrones de fallas
- Predicción de necesidades de mantenimiento
- Optimización de inventarios de repuestos
- Planificación de reemplazos

## Tipos de Usuario y Permisos

### PATCO Administrador
- Configuración completa de equipos y ubicaciones
- Gestión de códigos QR y etiquetas
- Acceso a todos los reportes y métricas
- Configuración de mantenimientos preventivos

### PATCO Líder Técnico
- Gestión de equipos de su área
- Planificación de mantenimientos
- Análisis de rendimiento de equipos
- Asignación de servicios por equipo

### PATCO Técnico
- Acceso a información de equipos asignados
- Escaneo de códigos QR
- Registro de servicios realizados
- Actualización de estado de equipos

### Cliente/Usuario Final
- Visualización de sus equipos (solo lectura)
- Creación de tickets mediante QR
- Consulta de historial de servicios
- Acceso a manuales y documentación

## Flujos de Trabajo Principales

### 1. Registro de Nuevo Equipo
1. Creación del registro de equipo
2. Asignación de código PATCO
3. Configuración de ubicación
4. Generación automática de código QR
5. Impresión y colocación de etiqueta
6. Configuración de mantenimiento preventivo

### 2. Servicio desde Código QR
1. Escaneo del código QR del equipo
2. Acceso automático a ficha del equipo
3. Creación de ticket o orden de servicio
4. Ejecución del servicio
5. Registro de actividades realizadas
6. Actualización de métricas del equipo

### 3. Mantenimiento Preventivo
1. Generación automática de orden de mantenimiento
2. Asignación basada en habilidades requeridas
3. Ejecución según checklist del equipo
4. Registro de estado y observaciones
5. Programación del próximo mantenimiento
6. Actualización de métricas de confiabilidad

## Métricas y KPIs Soportados

### Métricas por Equipo
- **Disponibilidad**: Tiempo operativo vs. tiempo total
- **MTBF**: Tiempo promedio entre fallas
- **MTTR**: Tiempo promedio de reparación
- **Costo de Mantenimiento**: Acumulado por período
- **Eficiencia Energética**: Consumo vs. rendimiento

### Métricas por Cliente
- Disponibilidad promedio de la flota
- Costo total de mantenimiento
- Número de incidencias por período
- Cumplimiento de SLAs
- Satisfacción con el servicio

### Métricas Operacionales
- Equipos por técnico
- Utilización de códigos QR
- Tiempo de respuesta promedio
- Efectividad de mantenimientos preventivos

## Reportes Disponibles

### Reportes de Equipos
- Inventario completo de equipos por cliente
- Estado operacional de la flota
- Equipos próximos a mantenimiento
- Historial de servicios por equipo

### Reportes de Rendimiento
- Análisis de disponibilidad
- Costos de mantenimiento por equipo
- Tendencias de fallas
- Eficiencia de mantenimientos preventivos

### Reportes de Ubicación
- Equipos por ubicación
- Optimización de rutas de servicio
- Análisis de densidad de equipos
- Planificación de recursos por área

## Beneficios del Módulo

1. **Trazabilidad Completa**: Historial detallado de cada equipo
2. **Identificación Rápida**: Acceso inmediato mediante códigos QR
3. **Optimización de Mantenimientos**: Planificación basada en datos reales
4. **Reducción de Costos**: Mantenimiento predictivo vs. correctivo
5. **Mejora de SLAs**: Respuesta más rápida y efectiva
6. **Satisfacción del Cliente**: Mejor disponibilidad de equipos
7. **Análisis Predictivo**: Identificación temprana de problemas
8. **Optimización de Inventarios**: Control preciso de repuestos

## Integración con Tecnologías Móviles

### Aplicaciones Móviles
- Escaneo de códigos QR desde dispositivos móviles
- Acceso offline a información básica del equipo
- Sincronización automática al recuperar conectividad
- Interfaz optimizada para técnicos en campo

### IoT y Sensores
- Integración con sensores de equipos inteligentes
- Monitoreo en tiempo real de parámetros críticos
- Alertas automáticas por condiciones anómalas
- Mantenimiento predictivo basado en datos de sensores

## Versión

Compatible con Odoo 18 Community Edition.

## Soporte e Implementación

La implementación exitosa de este módulo requiere:

1. **Inventario Inicial**: Registro completo de todos los equipos existentes
2. **Configuración de Ubicaciones**: Mapeo detallado de instalaciones del cliente
3. **Generación de QRs**: Creación e instalación de códigos QR en todos los equipos
4. **Capacitación de Usuarios**: Entrenamiento en uso de códigos QR y sistema
5. **Integración con Procesos**: Adaptación de procedimientos existentes
6. **Monitoreo Inicial**: Seguimiento cercano durante las primeras semanas

Este módulo es fundamental para la digitalización completa de las operaciones de mantenimiento y la base para implementar estrategias de mantenimiento predictivo en el ecosistema PATCO.