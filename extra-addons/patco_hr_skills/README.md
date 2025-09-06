# PATCO HR Skills - Gestión de Habilidades de Técnicos

## Descripción

PATCO HR Skills es el módulo especializado en la gestión de competencias y habilidades de técnicos dentro del ecosistema PATCO. Este módulo extiende las capacidades de Field Service Skills de OCA para proporcionar una matriz de competencias específica para el sector de mantenimiento HORECA (Hoteles, Restaurantes y Cafeterías), permitiendo la asignación optimizada de servicios basada en las habilidades requeridas y disponibles.

## Función en el Ecosistema PATCO

Este módulo es fundamental para la optimización de recursos humanos en operaciones de mantenimiento, proporcionando:

- **Matriz de Competencias**: Sistema completo de habilidades técnicas y certificaciones
- **Asignación Inteligente**: Matching automático entre requerimientos de servicio y capacidades del técnico
- **Gestión de Certificaciones**: Control de vigencia y renovación de certificaciones
- **Planificación de Capacitación**: Identificación de brechas de habilidades y necesidades de entrenamiento
- **Análisis de Productividad**: Métricas de desempeño por habilidad y técnico
- **Cumplimiento Normativo**: Garantía de que los técnicos tienen las certificaciones requeridas

## Dependencias del Módulo

### Módulos Odoo Core
- `base`
- `hr`
- `fieldservice`
- `hr_skills` (si está disponible)

### Módulos OCA
- `fieldservice_skill`
- `hr_skill`

### Módulos PATCO
- `patco_core` (para integración con naturalezas de servicio)

## Funcionalidades Principales

### 1. Gestión de Habilidades Técnicas

#### Categorías de Habilidades HORECA
- **Refrigeración Comercial**
  - Sistemas de refrigeración
  - Cámaras frigoríficas
  - Vitrinas refrigeradas
  - Equipos de congelación

- **Equipos de Cocina**
  - Hornos industriales
  - Freidoras
  - Planchas y parrillas
  - Equipos de vapor

- **Sistemas de Ventilación**
  - Campanas extractoras
  - Sistemas HVAC
  - Ventilación industrial
  - Control de calidad del aire

- **Equipos de Lavado**
  - Lavavajillas industriales
  - Sistemas de lavado
  - Equipos de saneamiento

- **Sistemas Eléctricos**
  - Instalaciones eléctricas
  - Sistemas de control
  - Automatización
  - Seguridad eléctrica

#### Niveles de Competencia
- **Básico**: Conocimientos fundamentales
- **Intermedio**: Capacidad de trabajo independiente
- **Avanzado**: Expertise y capacidad de liderazgo
- **Experto**: Conocimiento especializado y certificaciones

### 2. Sistema de Certificaciones

#### Tipos de Certificaciones
- **Certificaciones de Fabricante**: Específicas por marca de equipo
- **Certificaciones de Seguridad**: Manejo de gases, electricidad, etc.
- **Certificaciones Normativas**: Cumplimiento de regulaciones sanitarias
- **Certificaciones Técnicas**: Especialización en tecnologías específicas

#### Gestión de Vigencia
- Control automático de fechas de vencimiento
- Alertas de renovación próxima
- Bloqueo de asignaciones con certificaciones vencidas
- Historial completo de certificaciones

### 3. Matriz de Competencias por Técnico

#### Perfil de Habilidades
- Evaluación individual por habilidad
- Nivel de competencia actual
- Fecha de última evaluación
- Certificaciones asociadas
- Plan de desarrollo personal

#### Evaluación y Seguimiento
- Evaluaciones periódicas de competencias
- Registro de mejoras y capacitaciones
- Métricas de desempeño por habilidad
- Identificación de fortalezas y áreas de mejora

### 4. Asignación Inteligente de Servicios

#### Matching Automático
- Análisis de requerimientos de la orden de servicio
- Comparación con habilidades disponibles
- Sugerencia de técnicos más calificados
- Consideración de carga de trabajo actual

#### Criterios de Asignación
- Nivel de habilidad requerido vs. disponible
- Certificaciones necesarias
- Experiencia previa con el tipo de equipo
- Proximidad geográfica
- Disponibilidad de agenda

## Configuración Necesaria

### Configuración Inicial de Habilidades

1. **Creación de Categorías de Habilidades**
   ```
   - Refrigeración
   - Cocina
   - Ventilación
   - Lavado
   - Eléctrico
   - Seguridad
   ```

2. **Definición de Habilidades Específicas**
   ```
   Refrigeración:
   - Diagnóstico de sistemas de frío
   - Reparación de compresores
   - Manejo de gases refrigerantes
   - Instalación de equipos
   ```

3. **Configuración de Niveles**
   - Definir escalas de competencia
   - Establecer criterios de evaluación
   - Configurar requisitos por nivel

### Configuración de Certificaciones

1. **Tipos de Certificación**
   - Crear categorías de certificaciones
   - Definir organismos certificadores
   - Establecer períodos de vigencia

2. **Requisitos por Habilidad**
   - Asociar certificaciones obligatorias
   - Definir certificaciones recomendadas
   - Establecer equivalencias

### Configuración de Evaluaciones

1. **Criterios de Evaluación**
   - Definir métricas de desempeño
   - Establecer frecuencia de evaluaciones
   - Configurar escalas de calificación

2. **Proceso de Evaluación**
   - Definir evaluadores autorizados
   - Establecer procedimientos
   - Configurar aprobaciones

## Relación con Otros Módulos del Ecosistema

### Integración con patco_core
- **Naturalezas de Servicio**: Cada naturaleza requiere habilidades específicas
- **Órdenes de Servicio**: Asignación automática basada en habilidades
- **Análisis de Servicios**: Métricas de eficiencia por habilidad

### Integración con fieldservice
- **Asignación de Técnicos**: Filtrado por habilidades requeridas
- **Planificación**: Optimización basada en competencias
- **Reportes**: Análisis de utilización de habilidades

### Integración con HR
- **Perfiles de Empleado**: Extensión con matriz de competencias
- **Evaluaciones**: Integración con sistema de evaluación de desempeño
- **Capacitación**: Identificación de necesidades de entrenamiento

## Casos de Uso Específicos

### Según el Documento Funcional

#### MACRO-PROCESO 1: Comercial y Onboarding

**Evaluación de Capacidades**
- Análisis de habilidades disponibles vs. requerimientos del cliente
- Identificación de necesidades de capacitación
- Planificación de recursos humanos

**Certificación de Técnicos**
- Validación de competencias para nuevos contratos
- Obtención de certificaciones específicas del cliente
- Cumplimiento de requisitos normativos

#### MACRO-PROCESO 2: Operaciones de Servicio

**Asignación Optimizada**
- Matching automático técnico-servicio
- Consideración de habilidades y certificaciones
- Optimización de rutas y cargas de trabajo

**Escalamiento Inteligente**
- Identificación automática de servicios complejos
- Asignación a técnicos con mayor experiencia
- Soporte de especialistas cuando es necesario

#### MACRO-PROCESO 3: Ejecución en Campo

**Validación de Competencias**
- Verificación de habilidades antes del servicio
- Acceso a información técnica específica
- Soporte remoto de especialistas

**Registro de Experiencia**
- Actualización automática de experiencia
- Registro de nuevas habilidades adquiridas
- Feedback de calidad del servicio

#### MACRO-PROCESO 4: Análisis y Mejora

**Análisis de Competencias**
- Identificación de brechas de habilidades
- Planificación de capacitaciones
- Análisis de ROI de entrenamientos

**Optimización de Recursos**
- Redistribución de cargas de trabajo
- Identificación de especialistas clave
- Planificación de sucesión

## Tipos de Usuario y Permisos

### PATCO Administrador
- Configuración completa del sistema de habilidades
- Gestión de certificaciones y evaluaciones
- Acceso a todos los reportes y análisis
- Configuración de criterios de asignación

### PATCO Líder Técnico
- Evaluación de competencias de su equipo
- Asignación manual considerando habilidades
- Reportes de utilización de competencias
- Identificación de necesidades de capacitación

### PATCO Técnico
- Visualización de su perfil de habilidades
- Registro de nuevas certificaciones
- Acceso a materiales de capacitación
- Autoevaluación de competencias

### Gerente de RRHH
- Gestión de evaluaciones de desempeño
- Planificación de capacitaciones
- Análisis de competencias organizacionales
- Reportes de certificaciones

## Flujos de Trabajo Principales

### 1. Evaluación de Competencias
1. Programación de evaluación
2. Ejecución de evaluación técnica
3. Registro de resultados
4. Actualización del perfil del técnico
5. Identificación de brechas
6. Planificación de capacitación

### 2. Asignación Basada en Habilidades
1. Análisis de requerimientos del servicio
2. Búsqueda de técnicos calificados
3. Evaluación de disponibilidad
4. Asignación automática o manual
5. Validación de certificaciones
6. Confirmación de asignación

### 3. Gestión de Certificaciones
1. Registro de nueva certificación
2. Validación de documentos
3. Actualización del perfil
4. Configuración de alertas de vencimiento
5. Programación de renovaciones
6. Seguimiento de cumplimiento

## Métricas y KPIs Soportados

### Métricas de Competencias
- Distribución de habilidades por técnico
- Cobertura de habilidades por área geográfica
- Tiempo promedio de servicio por nivel de habilidad
- Tasa de éxito por competencia

### Métricas de Certificaciones
- Porcentaje de técnicos certificados por habilidad
- Certificaciones próximas a vencer
- Cumplimiento normativo por cliente
- ROI de programas de certificación

### Métricas de Asignación
- Efectividad del matching automático
- Tiempo de resolución por nivel de habilidad
- Satisfacción del cliente por competencia del técnico
- Utilización de habilidades especializadas

## Reportes Disponibles

### Reportes Operacionales
- Matriz de competencias por técnico
- Disponibilidad de habilidades por región
- Servicios pendientes por falta de habilidades
- Utilización de competencias especializadas

### Reportes Estratégicos
- Análisis de brechas de competencias
- Plan de desarrollo de habilidades
- ROI de programas de capacitación
- Proyección de necesidades futuras

### Reportes de Cumplimiento
- Estado de certificaciones por técnico
- Cumplimiento normativo por cliente
- Certificaciones próximas a vencer
- Historial de evaluaciones

## Beneficios del Módulo

1. **Optimización de Asignaciones**: Técnico correcto para cada servicio
2. **Mejora de Calidad**: Servicios realizados por personal calificado
3. **Cumplimiento Normativo**: Garantía de certificaciones vigentes
4. **Desarrollo del Personal**: Identificación clara de necesidades de capacitación
5. **Eficiencia Operacional**: Reducción de tiempos de servicio
6. **Satisfacción del Cliente**: Mejor calidad de servicio
7. **Gestión de Riesgos**: Control de competencias críticas
8. **Planificación Estratégica**: Visibilidad de capacidades organizacionales

## Integración con Sistemas Externos

### Plataformas de Capacitación
- Integración con LMS (Learning Management Systems)
- Sincronización de certificaciones
- Tracking de progreso de capacitaciones

### Organismos Certificadores
- Validación automática de certificaciones
- Actualización de estados de vigencia
- Notificaciones de renovaciones

## Versión

Compatible con Odoo 18 Community Edition.

## Soporte y Implementación

Este módulo requiere configuración detallada de la matriz de competencias específica para cada organización. Se recomienda:

1. **Análisis de Competencias**: Identificar habilidades críticas del negocio
2. **Definición de Niveles**: Establecer criterios claros de evaluación
3. **Capacitación de Usuarios**: Entrenar a evaluadores y administradores
4. **Implementación Gradual**: Comenzar con habilidades críticas
5. **Monitoreo Continuo**: Ajustar criterios basado en resultados

La implementación exitosa de este módulo es clave para maximizar la eficiencia operacional y la calidad del servicio en el ecosistema PATCO.