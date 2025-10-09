# Flujo Operativo para Servicios Multi-Activo y Multi-Técnico
## Proyecto PATCO - Odoo 18 Community

---

## Introducción

Este documento define el flujo operativo específico para escenarios donde **un técnico o múltiples técnicos** se desplazan a una **ubicación de cliente** para realizar mantenimiento a **múltiples activos del cliente** en una sola visita. Este enfoque optimiza los recursos, reduce costos de desplazamiento y mejora la eficiencia operativa.

### Conceptos Clave
- **Activo del Cliente**: Se refiere a `maintenance.equipment` - maquinaria, equipamiento o dispositivos del cliente
- **Ubicación de Cliente**: Sede física donde se encuentran múltiples activos del cliente
- **Servicio Multi-Activo**: Una intervención que abarca varios activos del cliente en la misma ubicación
- **Equipo de Técnicos**: Uno o más técnicos trabajando coordinadamente en la misma ubicación

---

## FLUJO OPERATIVO PRINCIPAL

### 1. PLANIFICACIÓN Y DESPACHO

#### 1.1 Creación de Tickets Agrupados
**Responsable**: Coordinador de Servicios  
**Herramienta**: Mesa de Ayuda (Helpdesk)

**Escenarios de Agrupación**:
- **Mantenimiento Preventivo Programado**: El cliente solicita revisión general de todos sus activos
- **Múltiples Fallas Reportadas**: Varios activos del cliente presentan problemas simultáneamente
- **Optimización de Ruta**: Se agrupan servicios pendientes de la misma ubicación

**Proceso**:
1. **Ticket Principal**: Se crea un ticket maestro con:
   - Título: "Servicio Multi-Activo - [Nombre Ubicación]"
   - Cliente: Entidad principal (ej. "Cadena Hotelera Sol S.A.")
   - Ubicación: Sede específica (ej. "Hotel Sol Centro")
   - Descripción: Resumen de todos los activos del cliente a atender

2. **Tickets Individuales por Activo**: Para cada activo del cliente se crea un ticket específico:
   - Vinculado al ticket principal (campo "Ticket Relacionado")
   - Activo del cliente específico seleccionado
   - Clasificación PATCO aplicada (Naturaleza, Área, Complejidad)
   - Habilidades requeridas definidas

#### 1.2 Conversión a Órdenes de Servicio de Campo
**Proceso**:
1. **Orden Principal**: El ticket maestro se convierte en una `fsm.order` coordinadora
2. **Órdenes Individuales**: Cada ticket de activo del cliente genera su propia `fsm.order`
3. **Vinculación**: Todas las órdenes individuales se relacionan con la orden principal

#### 1.3 Asignación de Técnicos
**Estrategias de Asignación**:

**Opción A: Técnico Único Multi-Competencia**
- Un técnico con habilidades transversales atiende todos los activos del cliente
- Ideal para: Mantenimientos preventivos, activos de baja complejidad

**Opción B: Equipo Especializado**
- Múltiples técnicos, cada uno especializado en tipos específicos de activos del cliente
- Ideal para: Servicios correctivos complejos, activos críticos

**Opción C: Técnico Principal + Apoyo**
- Un técnico líder coordina y un técnico junior asiste
- Ideal para: Entrenamiento, servicios de alta complejidad

**Implementación en Odoo**:
- **Técnico Principal**: Asignado en la orden coordinadora
- **Técnicos Adicionales**: Asignados en órdenes individuales según especialización
- **Coordinación**: Campo "Equipo de Trabajo" en la orden principal lista todos los técnicos involucrados

### 2. PREPARACIÓN PRE-SERVICIO

#### 2.1 Verificación de Competencias
**Proceso Automatizado**:
- El sistema valida que las habilidades requeridas estén cubiertas por el equipo asignado
- Alerta si falta alguna competencia crítica
- Sugiere reasignaciones si es necesario

#### 2.2 Gestión de Stock Multi-Activo
**Preparación de Repuestos**:
1. **Análisis Predictivo**: El sistema analiza el historial de cada activo del cliente
2. **Lista Consolidada**: Genera una lista unificada de repuestos probables
3. **Carga de Furgoneta**: Los repuestos se transfieren a la ubicación del vehículo del técnico principal
4. **Verificación**: Se confirma disponibilidad antes del despacho

#### 2.3 Documentación Técnica
**Preparación Automática**:
- Checklists de entrada y salida para cada categoría de activo del cliente
- Manuales técnicos y diagramas relevantes
- Historial de servicios de cada activo del cliente
- Información de garantías y contratos

### 3. EJECUCIÓN EN CAMPO

#### 3.1 Llegada y Coordinación
**Protocolo de Inicio**:
1. **Check-in Coordinado**: Todos los técnicos confirman llegada en sus respectivas órdenes
2. **Reunión de Coordinación**: El técnico principal distribuye tareas y activos del cliente
3. **Activación del Asistente IA**: Cada técnico recibe notificación en Telegram para sus activos del cliente asignados

#### 3.2 Ejecución Paralela por Activos del Cliente
**Flujo Individual por Técnico/Activo**:

**Para cada `fsm.order` individual**:
1. **Inicio de Trabajo**: 
   - Cambio de estado a "En Progreso" en Odoo
   - Confirmación en Telegram con el Asistente IA

2. **Checklist de Entrada**:
   - El Asistente IA presenta el checklist específico del activo del cliente
   - Captura de fotos, mediciones y observaciones iniciales
   - Registro de estado previo del activo del cliente

3. **Diagnóstico y Trabajo**:
   - Consulta de historial del activo del cliente en Odoo
   - Soporte técnico inteligente vía Telegram (consulta de manuales, procedimientos)
   - Ejecución del trabajo de mantenimiento/reparación

4. **Consumo de Repuestos**:
   - Registro en tiempo real en la `fsm.order` individual
   - Descuento automático del stock de la furgoneta
   - Coordinación con otros técnicos si se requieren repuestos compartidos

5. **Checklist de Salida**:
   - Verificación de funcionamiento post-servicio
   - Pruebas operativas específicas del activo del cliente
   - Captura de evidencias de trabajo completado

#### 3.3 Coordinación Entre Técnicos
**Comunicación y Sincronización**:
- **Canal de Coordinación**: Grupo de Telegram para el equipo de trabajo
- **Compartir Recursos**: Coordinación para repuestos, herramientas especializadas
- **Escalamiento**: Procedimiento para solicitar apoyo técnico entre especialistas
- **Sincronización de Tiempos**: Coordinación para activos del cliente interdependientes

#### 3.4 Gestión de Tiempos
**Registro Detallado**:
- **Tiempo por Activo del Cliente**: Cada técnico registra tiempo específico por `fsm.order`
- **Tiempo de Coordinación**: Tiempo compartido registrado en la orden principal
- **Tiempo de Desplazamiento**: Registrado una sola vez en la orden coordinadora

### 4. CONSOLIDACIÓN Y CIERRE

#### 4.1 Finalización Individual
**Por cada Activo del Cliente/Técnico**:
1. **Cierre de Orden Individual**: Estado "Trabajo Finalizado" en cada `fsm.order`
2. **Informe Individual**: El Asistente IA genera informe específico por activo del cliente
3. **Sincronización**: Datos estructurados se envían a Odoo

#### 4.2 Consolidación del Servicio
**Responsable**: Técnico Principal

**Proceso**:
1. **Verificación de Completitud**: Confirma que todos los activos del cliente han sido atendidos
2. **Informe Consolidado**: El Asistente IA genera un informe maestro que incluye:
   - Resumen ejecutivo del servicio multi-activo
   - Estado individual de cada activo del cliente
   - Repuestos consumidos consolidados
   - Recomendaciones generales para la ubicación
   - Próximos mantenimientos sugeridos

3. **Presentación al Cliente**: 
   - Revisión del informe consolidado con el responsable del cliente
   - Explicación del estado de cada activo del cliente
   - Entrega de recomendaciones y plan de mantenimiento

4. **Conformidad Global**: 
   - El cliente da conformidad verbal para todo el servicio
   - Registro en la orden coordinadora
   - Finalización de todas las órdenes individuales

### 5. PROCESO ADMINISTRATIVO POST-SERVICIO

#### 5.1 Gestión Documental
**Coordinador de Servicios**:
1. **Revisión de Informes**: Valida informes individuales y consolidado
2. **Envío al Cliente**: Remite documentación completa
3. **Solicitud de OC**: Gestiona orden de compra única para todo el servicio

#### 5.2 Facturación Consolidada
**Proceso**:
1. **Factura Única**: Se genera una factura que consolida:
   - Horas de todos los técnicos
   - Repuestos consumidos en todos los activos del cliente
   - Servicios específicos por cada activo del cliente
2. **Detalle por Activo del Cliente**: La factura incluye desglose detallado por activo del cliente atendido
3. **Referencia Única**: Número de OC del cliente para todo el servicio

---

## BENEFICIOS DEL FLUJO MULTI-ACTIVO

### Operativos
- **Eficiencia de Desplazamiento**: Un solo viaje para múltiples servicios
- **Optimización de Recursos**: Mejor utilización de técnicos especializados
- **Coordinación Mejorada**: Trabajo en equipo para casos complejos
- **Servicio Integral**: Atención completa de la ubicación del cliente

### Administrativos
- **Facturación Simplificada**: Una sola factura por ubicación
- **Gestión Documental Eficiente**: Informes consolidados
- **Trazabilidad Completa**: Historial detallado por equipo y servicio general
- **Análisis de Rentabilidad**: Métricas por ubicación y por equipo

### Para el Cliente
- **Menor Interrupción**: Una sola visita para múltiples activos
- **Servicio Coordinado**: Atención integral de sus activos
- **Documentación Completa**: Informe consolidado del estado de todos sus activos
- **Planificación Mejorada**: Recomendaciones integrales de mantenimiento

---

## CONSIDERACIONES TÉCNICAS

### Configuración en Odoo
1. **Campos Adicionales**:
   - `fsm.order`: Campo "Orden Principal" para vinculación
   - `fsm.order`: Campo "Equipo de Trabajo" (Many2many con hr.employee)
   - `helpdesk.ticket`: Campo "Ticket Relacionado" para agrupación

2. **Vistas Personalizadas**:
   - Vista Kanban agrupada por "Orden Principal"
   - Dashboard de servicios multi-activo
   - Reportes consolidados por ubicación

3. **Automatizaciones**:
   - Creación automática de órdenes vinculadas
   - Notificaciones coordinadas al Asistente IA
   - Validación de completitud antes del cierre

### Integración con Asistente IA
1. **Payload Extendido**: Incluye información de coordinación y otros técnicos
2. **Canal de Coordinación**: Grupo de Telegram para el equipo de trabajo
3. **Informes Consolidados**: Capacidad de generar reportes multi-activo
4. **Sincronización Coordinada**: Envío de datos estructurados para múltiples órdenes

---

## MÉTRICAS Y KPIs

### Eficiencia Operativa
- **Tiempo Promedio por Activo del Cliente**: Comparación individual vs. multi-activo
- **Utilización de Técnicos**: Horas productivas vs. tiempo de desplazamiento
- **Tasa de Resolución**: Porcentaje de activos del cliente resueltos en primera visita
- **Consumo de Repuestos**: Optimización de stock por servicio consolidado

### Satisfacción del Cliente
- **Tiempo de Interrupción**: Reducción vs. servicios individuales
- **Calidad del Servicio**: Evaluación por activo del cliente y servicio general
- **Conformidad**: Tasa de aceptación de informes consolidados

### Rentabilidad
- **Costo por Servicio**: Comparación de modelos individual vs. consolidado
- **Margen por Ubicación**: Rentabilidad integral del cliente
- **Eficiencia de Facturación**: Tiempo de cobro de servicios consolidados

Este flujo operativo maximiza la eficiencia de PATCO mientras mantiene la calidad del servicio y la satisfacción del cliente, aprovechando al máximo las capacidades de Odoo 18 Community y la integración con el Asistente IA para la gestión integral de activos del cliente.