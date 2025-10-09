# Plan de Acción Funcional - Refactorización Módulos FSM y Equipment

## 1. Análisis del Estado Actual

### 1.1 Módulo patco_fsm
**Estado:** Funcional con dependencias de proyecto/tarea
- **Fortalezas:** Sistema completo de clasificación, gestión de habilidades, control de tiempo, checklists dinámicos
- **Debilidades:** Dependencia de project.project y project.task que complica el flujo para MYPES
- **Campos críticos:** `x_nature_id`, `x_area_id`, `x_consumed_parts_ids`, `has_signed_worksheet`
- **Funcionalidades clave:** Timesheet automático, hojas de trabajo digitales, gestión de repuestos

### 1.2 Módulo patco_equipment
**Estado:** Robusto con integración FSM básica
- **Fortalezas:** Gestión avanzada de equipos, códigos QR, categorías con herencia, base de conocimiento
- **Debilidades:** Relación 1:1 equipo-orden (no soporta múltiples activos por servicio)
- **Campos críticos:** `x_equipment_id`, `x_customer_id`, `x_service_location_id`
- **Funcionalidades clave:** Códigos PATCO únicos, checklists por categoría, métricas automáticas

### 1.3 Problemática Identificada
1. **Complejidad innecesaria:** Dependencia de proyectos/tareas para servicios simples
2. **Limitación de activos:** Solo un equipo por orden de servicio
3. **Gestión de técnicos:** Falta sistema de líder y equipo estructurado
4. **Flujo MYPE:** Demasiado complejo para pequeñas empresas de servicios

## 2. Plan Funcional de Mejora

### 2.1 Eliminación de Dependencias Proyecto/Tarea

#### Objetivo
Simplificar el flujo de trabajo eliminando la complejidad de gestión de proyectos para servicios directos.

#### Acciones Funcionales
1. **Remover campos obsoletos:**
   - Eliminar `project_id` y `task_id` de las vistas FSM
   - Ocultar pestañas y secciones relacionadas con proyectos
   - Mantener funcionalidad de timesheet directo en la orden

2. **Simplificar navegación:**
   - Acceso directo desde cliente a órdenes de servicio
   - Menú principal centrado en "Órdenes de Servicio" no en "Proyectos"
   - Dashboard operativo sin métricas de proyecto

3. **Flujo de creación simplificado:**
   - Crear orden → Asignar cliente → Seleccionar activos → Asignar técnicos → Ejecutar
   - Eliminar paso intermedio de creación de proyecto/tarea

### 2.2 Sistema de Múltiples Activos por Orden

#### Objetivo
Permitir que una sola orden de servicio pueda atender múltiples equipos del mismo cliente.

#### Diseño Funcional
1. **Modelo de asignación activo-técnico:**
   - Tabla intermedia que relaciona: Orden ↔ Activo ↔ Técnico Responsable
   - Permite asignar técnicos específicos a activos específicos dentro de la misma orden
   - Facilita servicios integrales (ej: mantenimiento completo de cocina industrial)

2. **Vista de gestión:**
   - Pestaña "Activos y Asignaciones" en la orden de servicio
   - Lista editable: Activo | Técnico Asignado | Estado | Observaciones
   - Filtros por estado de activo y técnico disponible

3. **Flujo operativo:**
   - Jefe de operaciones crea orden y selecciona múltiples activos
   - Asigna técnico líder y técnicos específicos por activo
   - Cada técnico ve solo sus activos asignados en la app móvil
   - Control centralizado del progreso por activo

### 2.3 Sistema de Técnicos con Líder y Equipo

#### Objetivo
Estructurar la gestión de técnicos con roles claros y jerarquía operativa.

#### Estructura Funcional
1. **Roles definidos:**
   - **Líder Técnico:** Responsable general de la orden, toma decisiones, reporta al jefe
   - **Técnicos Asignados:** Ejecutan tareas específicas en activos asignados
   - **Técnico de Respaldo:** Disponible en caso de ausencias o emergencias

2. **Gestión de disponibilidad:**
   - Campo "Técnicos Disponibles" que muestra solo técnicos con habilidades requeridas
   - Filtro por ubicación geográfica y disponibilidad horaria
   - Sistema de notificaciones para cambios de asignación

3. **Flujo de asignación:**
   - Jefe selecciona líder técnico basado en complejidad del servicio
   - Líder puede sugerir técnicos adicionales según necesidades
   - Sistema de escalamiento automático si se requieren más recursos

### 2.4 Relación Cliente-Ubicación Mejorada

#### Objetivo
Optimizar la gestión de ubicaciones de servicio para clientes con múltiples sedes.

#### Mejoras Funcionales
1. **Gestión de ubicaciones:**
   - Cliente principal con múltiples ubicaciones de servicio
   - Cada ubicación puede tener equipos específicos
   - Historial de servicios por ubicación

2. **Selección inteligente:**
   - Al seleccionar cliente, mostrar ubicaciones disponibles
   - Al seleccionar ubicación, filtrar equipos de esa ubicación
   - Sugerencias basadas en servicios anteriores

3. **Optimización logística:**
   - Agrupación de órdenes por zona geográfica
   - Sugerencias de rutas optimizadas para técnicos
   - Alertas de proximidad para servicios adicionales

## 3. Flujo de Trabajo Optimizado para MYPES

### 3.1 Proceso Simplificado

#### Flujo Principal
1. **Recepción de solicitud:**
   - Cliente llama o envía solicitud
   - Recepcionista crea orden con datos básicos
   - Sistema sugiere técnicos disponibles

2. **Planificación (Jefe de Operaciones):**
   - Revisa órdenes pendientes
   - Asigna líder técnico y equipo
   - Define prioridades y tiempos estimados
   - Confirma disponibilidad de repuestos

3. **Ejecución (Técnicos):**
   - Líder técnico recibe orden en móvil
   - Coordina con equipo asignado
   - Ejecuta checklists por activo
   - Registra tiempo y materiales
   - Obtiene firma digital del cliente

4. **Cierre (Administrativo):**
   - Revisión automática de completitud
   - Generación de reporte de servicio
   - Facturación automática
   - Programación de próximo mantenimiento

### 3.2 Roles y Responsabilidades

#### Jefe de Operaciones
- **Dashboard principal:** Órdenes pendientes, técnicos disponibles, alertas de SLA
- **Funciones clave:** Asignación de recursos, monitoreo en tiempo real, resolución de conflictos
- **Métricas importantes:** Tiempo promedio de servicio, satisfacción del cliente, utilización de técnicos

#### Técnico Líder
- **Vista móvil optimizada:** Detalles de orden, activos asignados, contacto del cliente
- **Funciones clave:** Coordinación del equipo, toma de decisiones técnicas, comunicación con cliente
- **Herramientas:** Checklists digitales, cámara para evidencias, acceso a base de conocimiento

#### Técnico Asignado
- **Vista enfocada:** Solo sus activos asignados, tareas específicas, materiales requeridos
- **Funciones clave:** Ejecución técnica, registro de tiempo, reporte de incidencias
- **Simplicidad:** Interfaz mínima, flujo guiado, confirmaciones simples

## 4. Consideraciones de UX y Usabilidad

### 4.1 Principios de Diseño

#### Para Jefe de Operaciones
- **Vista panorámica:** Dashboard con información crítica en una sola pantalla
- **Acciones rápidas:** Botones de acción directa para tareas frecuentes
- **Alertas inteligentes:** Notificaciones solo para situaciones que requieren atención
- **Filtros dinámicos:** Capacidad de filtrar por técnico, cliente, zona, urgencia

#### Para Técnicos
- **Diseño móvil-first:** Optimizado para tablets y smartphones
- **Navegación simple:** Máximo 3 niveles de profundidad
- **Entrada de datos mínima:** Códigos QR, selección múltiple, valores predeterminados
- **Modo offline:** Funcionalidad básica sin conexión a internet

### 4.2 Mejoras de Interfaz

#### Reorganización de Vistas
1. **Vista de orden simplificada:**
   - Información esencial en la parte superior
   - Pestañas organizadas por flujo de trabajo
   - Campos agrupados lógicamente
   - Botones de acción contextuales

2. **Formularios inteligentes:**
   - Campos que se auto-completan basados en selecciones anteriores
   - Validaciones en tiempo real
   - Sugerencias basadas en historial
   - Mensajes de ayuda contextuales

3. **Reportes visuales:**
   - Gráficos de progreso por orden
   - Métricas de rendimiento por técnico
   - Análisis de tendencias por cliente
   - Alertas de mantenimiento preventivo

## 5. Beneficios Esperados

### 5.1 Operacionales
- **Reducción de tiempo de creación de órdenes:** 60% menos pasos
- **Mejor utilización de técnicos:** Asignación optimizada por habilidades y ubicación
- **Mayor flexibilidad:** Servicios multi-activo en una sola visita
- **Control mejorado:** Seguimiento granular por activo y técnico

### 5.2 Estratégicos
- **Escalabilidad:** Estructura preparada para crecimiento de la empresa
- **Satisfacción del cliente:** Servicios más completos y coordinados
- **Eficiencia operativa:** Menos overhead administrativo
- **Competitividad:** Capacidad de manejar servicios más complejos

### 5.3 Técnicos
- **Mantenibilidad:** Código más limpio sin dependencias innecesarias
- **Flexibilidad:** Estructura modular para futuras extensiones
- **Rendimiento:** Menos consultas a la base de datos
- **Usabilidad:** Interfaz más intuitiva y eficiente

## 6. Consideraciones de Implementación

### 6.1 Fases de Desarrollo

#### Fase 1: Limpieza y Simplificación
- Remover dependencias de proyecto/tarea
- Simplificar vistas existentes
- Actualizar flujos de navegación

#### Fase 2: Múltiples Activos
- Crear modelo de asignación activo-técnico
- Implementar vistas de gestión
- Adaptar lógica de negocio

#### Fase 3: Sistema de Técnicos
- Implementar roles de líder y equipo
- Crear sistema de disponibilidad
- Optimizar asignación automática

#### Fase 4: UX y Optimización
- Rediseñar interfaces
- Implementar mejoras móviles
- Optimizar rendimiento

### 6.2 Riesgos y Mitigaciones

#### Riesgos Identificados
1. **Pérdida de funcionalidad:** Al remover proyectos/tareas
   - **Mitigación:** Análisis detallado de uso actual antes de remover

2. **Complejidad de migración:** Datos existentes
   - **Mitigación:** Estrategia de migración gradual con respaldo

3. **Resistencia al cambio:** Usuarios acostumbrados al flujo actual
   - **Mitigación:** Capacitación progresiva y documentación clara

4. **Rendimiento:** Nuevas relaciones complejas
   - **Mitigación:** Optimización de consultas y uso de índices

### 6.3 Criterios de Éxito

#### Métricas Cuantitativas
- Tiempo de creación de orden < 3 minutos
- Adopción del nuevo flujo > 90% en 30 días
- Reducción de errores de asignación > 50%
- Satisfacción del usuario > 4.5/5

#### Métricas Cualitativas
- Facilidad de uso percibida
- Reducción de consultas de soporte
- Mejora en coordinación de equipos
- Mayor control operativo

## 7. Archivos y Componentes a Modificar

### 7.1 Archivos XML de Vistas a Modificar

#### patco_fsm/views/fsm_order_views.xml
- **Vista principal:** `fsm_order_form_view_patco`
- **Modificaciones:** Sección de múltiples activos, asignación de técnicos con líder, eliminación de campos de proyecto/tarea
- **Impacto:** Reestructuración completa del formulario principal de órdenes de servicio

#### patco_equipment/views/fsm_order_views.xml
- **Vista heredada:** `view_fsm_order_form_patco`
- **Modificaciones:** Campos de relación activo-técnico, integración con sistema de múltiples activos
- **Impacto:** Extensión de funcionalidad para gestión de equipos múltiples

#### patco_equipment/views/maintenance_equipment_views.xml
- **Vistas afectadas:** `view_maintenance_equipment_form_patco`, `view_maintenance_equipment_tree_patco`
- **Modificaciones:** Botones estadísticos, relaciones con órdenes de servicio, columnas de servicios y técnicos
- **Impacto:** Mejora en la visualización de métricas y relaciones de equipos

### 7.2 Modelos Python a Modificar

#### patco_fsm/models/fsm_order.py
- **Clase:** `FSMOrder`
- **Modificaciones:** Agregar campos para múltiples activos y técnicos, sistema de líder técnico, eliminación de dependencias de proyecto/tarea
- **Campos nuevos:** `x_asset_technician_ids`, `x_lead_technician_id`, `x_team_technician_ids`
- **Impacto:** Cambio fundamental en la estructura de datos de órdenes de servicio

#### patco_equipment/models/fsm_order.py
- **Clase:** `FSMOrder` (extensión)
- **Modificaciones:** Modificar relación de activos de 1:1 a 1:N, integración con modelo intermedio
- **Campos modificados:** `x_equipment_id` (deprecado), nuevos campos de relación múltiple
- **Impacto:** Soporte para múltiples equipos por orden de servicio

#### patco_equipment/models/patco_equipment.py
- **Clase:** `MaintenanceEquipment`
- **Modificaciones:** Ajustes menores en relaciones, métodos de cálculo de métricas
- **Impacto:** Compatibilidad con nuevo sistema de asignaciones múltiples

### 7.3 Vistas Específicas Dentro de XML

#### fsm_order_form_view_patco (Vista Principal)
- **Sección "Información Básica":** Eliminación de campos de proyecto/tarea
- **Nueva sección "Múltiples Activos":** Lista editable de activos con técnicos asignados
- **Sección "Asignación de Técnicos":** Campo de líder técnico y equipo de trabajo
- **Pestañas operativas:** Reorganización para flujo simplificado

#### view_fsm_order_form_patco (Vista Heredada)
- **Campos de relación:** Integración con modelo intermedio activo-técnico
- **Botones de acción:** Accesos rápidos para gestión de equipos múltiples
- **Filtros dinámicos:** Selección inteligente de activos por cliente/ubicación

#### view_maintenance_equipment_form_patco (Formulario de Equipos)
- **Botones estadísticos:** Métricas de órdenes de servicio relacionadas
- **Sección de relaciones:** Historial de técnicos asignados
- **Campos de ubicación:** Integración mejorada con sistema de múltiples ubicaciones

#### view_maintenance_equipment_tree_patco (Lista de Equipos)
- **Columnas nuevas:** Último técnico asignado, próximo mantenimiento
- **Indicadores visuales:** Estado de servicio, disponibilidad
- **Filtros avanzados:** Por técnico, cliente, ubicación

### 7.4 Nuevos Archivos a Crear

#### patco_fsm/models/fsm_order_asset_technician.py
- **Modelo intermedio:** Relación Many2Many entre órdenes, activos y técnicos
- **Campos principales:** `order_id`, `asset_id`, `technician_id`, `is_lead`, `status`, `notes`
- **Funcionalidad:** Gestión granular de asignaciones activo-técnico

#### patco_fsm/views/fsm_order_asset_technician_views.xml
- **Vistas del modelo intermedio:** Formulario y lista para gestión de asignaciones
- **Integración:** Embebido en vista principal de órdenes de servicio
- **Funcionalidad:** Interfaz para asignación y seguimiento de técnicos por activo

### 7.5 Archivos de Configuración a Actualizar

#### patco_fsm/__manifest__.py
- **Dependencias:** Verificar compatibilidad con nuevos modelos
- **Datos:** Actualizar referencias a vistas modificadas

#### patco_equipment/__manifest__.py
- **Dependencias:** Agregar dependencia del nuevo modelo intermedio
- **Versión:** Incrementar por cambios estructurales

### 7.6 Consideraciones de Migración

#### Datos Existentes
- **Órdenes actuales:** Script de migración para convertir relaciones 1:1 a 1:N
- **Asignaciones de técnicos:** Preservar asignaciones existentes como líder técnico
- **Historial:** Mantener trazabilidad de servicios anteriores

#### Compatibilidad
- **Vistas personalizadas:** Verificar herencias de terceros
- **Reportes:** Actualizar consultas que usen campos deprecados
- **Integraciones:** Revisar APIs que accedan a campos modificados

---

**Documento generado:** Plan de Acción Funcional para Refactorización de Módulos FSM y Equipment  
**Fecha:** Diciembre 2024  
**Versión:** 1.1  
**Estado:** Listo para implementación con detalles técnicos