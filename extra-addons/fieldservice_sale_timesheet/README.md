# Field Service Sale Timesheet - Módulo Puente para Integración de Hojas de Tiempo

## Descripción

**NOTA IMPORTANTE**: Este es un módulo puente (bridge) que facilita la integración automática entre `fieldservice_sale` y `hr_timesheet`. La funcionalidad principal de integración de hojas de tiempo con ventas se ha movido al módulo `patco_core` para una mejor organización arquitectónica.

Field Service Sale Timesheet es un módulo de auto-instalación que se activa automáticamente cuando están presentes tanto `fieldservice_sale` como `hr_timesheet`, proporcionando las extensiones mínimas necesarias para que funcionen correctamente juntos en el ecosistema PATCO.

## Función en el Ecosistema PATCO

Este módulo actúa como un **conector técnico** entre los módulos OCA de Field Service y las funcionalidades de timesheet, proporcionando:

- **Auto-instalación**: Se instala automáticamente cuando se detectan las dependencias necesarias
- **Extensiones de Vista**: Añade campos de FSM Order al análisis de timesheets
- **Compatibilidad**: Asegura que los módulos OCA funcionen correctamente con las extensiones PATCO
- **Delegación**: Redirige la lógica de negocio compleja al módulo `patco_core`

> **Para funcionalidades avanzadas de facturación y análisis de rentabilidad, consulte el módulo `patco_core`.**

## Dependencias del Módulo

### Módulos Core de Odoo
- `hr_timesheet`: Gestión de hojas de tiempo por empleado
- `sale_timesheet`: Facturación basada en tiempo (opcional)

### Módulos OCA (Odoo Community Association)
- `fieldservice`: Gestión de órdenes de servicio de campo
- `fieldservice_sale`: Integración de field service con ventas

### Módulos PATCO
- `patco_core`: **Contiene la lógica principal de integración timesheet-ventas**

## Funcionalidades Técnicas

### 1. Extensión de Vistas
- Añade el campo `fsm_order_id` al modelo `timesheets.analysis.report`
- Permite análisis de timesheets vinculados a órdenes de servicio
- Mantiene compatibilidad con reportes estándar de OCA

### 2. Auto-instalación Inteligente
- Se instala automáticamente cuando se detectan `fieldservice_sale` y `hr_timesheet`
- No requiere instalación manual
- Configuración mínima necesaria

### 3. Delegación a PATCO Core
- **Importante**: Las funcionalidades de facturación, análisis de rentabilidad y gestión avanzada de timesheet están implementadas en `patco_core`
- Este módulo solo proporciona la "cola" técnica necesaria para la integración

## Estructura del Módulo

### Archivos Principales
- `__manifest__.py`: Configuración de auto-instalación
- `views/timesheets_analysis_views.xml`: Extensión de vistas de análisis
- `models/`: Vacío (funcionalidad delegada a patco_core)

### Dependencias Técnicas
```python
'depends': [
    'fieldservice_sale',
    'hr_timesheet', 
    'patco_core'
],
'auto_install': True  # Instalación automática
```

## Notas Técnicas

### Arquitectura
Este módulo sigue el patrón de "módulo puente" donde:
- **Responsabilidad mínima**: Solo extensiones de vista necesarias
- **Delegación**: Lógica de negocio en `patco_core`
- **Auto-instalación**: Activación automática por dependencias

### Mantenimiento
- **Actualizaciones**: Compatible con actualizaciones de módulos OCA
- **Extensibilidad**: Puede extenderse sin modificar código base
- **Migración**: Datos y configuraciones se mantienen en `patco_core`

---

**Importante**: Para implementar funcionalidades de facturación, análisis de rentabilidad, configuración de tarifas y gestión avanzada de timesheet, consulte la documentación del módulo `patco_core`.

## Configuración

### Instalación Automática
Este módulo se instala automáticamente cuando están presentes:
- `fieldservice_sale`
- `hr_timesheet`
- `patco_core`

### Configuración Avanzada
Para configuraciones avanzadas de facturación, productos de servicio, tarifas y análisis de rentabilidad, consulte la documentación del módulo `patco_core`.

### Verificación de Instalación
Puede verificar que el módulo está funcionando correctamente accediendo a:
```
Timesheet > Reportes > Análisis de Timesheets
```
Debe ver el campo "FSM Order" disponible en las vistas de análisis.

### Configuración de Tarifas

1. **Tarifas Base**
   - Tarifa estándar por hora
   - Tarifa nocturna (recargo %)
   - Tarifa festiva (recargo %)
   - Tarifa de emergencia (recargo %)

2. **Tarifas por Cliente**
   - Descuentos contractuales
   - Tarifas preferenciales
   - Condiciones especiales
   - Límites de facturación

### Configuración Contable

1. **Cuentas Contables**
   - Ingresos por servicios de mantenimiento
   - Costos de mano de obra
   - Cuentas analíticas por proyecto
   - Centros de costo por área

2. **Configuración de Impuestos**
   - IVA aplicable a servicios
   - Retenciones según cliente
   - Exenciones especiales

## Relación con Otros Módulos del Ecosistema

### Integración con patco_core
- **Naturalezas de Servicio**: Cada naturaleza tiene tarifas específicas
- **Órdenes de Servicio**: Fuente de información para facturación
- **Clasificación de Trabajos**: Base para aplicar tarifas correctas

### Integración con fieldservice_timesheet
- **Registro de Tiempo**: Fuente de datos para facturación
- **Validación de Horas**: Verificación antes de conversión a venta
- **Aprobación de Tiempo**: Workflow de autorización

### Integración con patco_customer_equipment
- **Equipos Facturables**: Identificación de activos sujetos a facturación
- **Historial de Servicios**: Base para análisis de rentabilidad por equipo
- **Contratos por Equipo**: Aplicación de condiciones específicas

### Integración con Sale y Account
- **Órdenes de Venta**: Creación automática desde servicios
- **Facturas**: Generación basada en tiempo aprobado
- **Análisis Financiero**: Reportes de rentabilidad

## Casos de Uso Específicos

### Según el Documento Funcional

#### MACRO-PROCESO 4: Cierre, Facturación y Cobranza

**Facturación Automática de Servicios**
1. **Consolidación de Tiempo**
   - Recopilación de todas las horas trabajadas en el período
   - Validación y aprobación de tiempo registrado
   - Aplicación de tarifas según tipo de servicio y cliente
   - Generación automática de líneas de factura

2. **Facturación de Materiales**
   - Integración con consumos registrados en órdenes de servicio
   - Aplicación de márgenes sobre costo de materiales
   - Consolidación con tiempo trabajado
   - Generación de factura integral

3. **Validación Contractual**
   - Verificación contra límites de acuerdos de servicio
   - Identificación de servicios adicionales
   - Aplicación de descuentos contractuales
   - Generación de reportes de consumo

**Análisis de Rentabilidad**
1. **Por Cliente**
   - Análisis de margen por cliente
   - Identificación de clientes más rentables
   - Optimización de tarifas
   - Negociación de contratos

2. **Por Tipo de Servicio**
   - Rentabilidad por naturaleza de servicio
   - Optimización de procesos
   - Ajuste de tarifas
   - Mejora de eficiencia

3. **Por Técnico**
   - Productividad individual
   - Rentabilidad por técnico
   - Identificación de necesidades de capacitación
   - Optimización de asignaciones

#### Integración con Procesos Comerciales

**Cotizaciones y Contratos**
- Base histórica para cotización de nuevos servicios
- Análisis de costos reales vs. estimados
- Mejora en precisión de cotizaciones
- Optimización de márgenes comerciales

**Seguimiento de Acuerdos**
- Monitoreo de consumo vs. límites contractuales
- Alertas tempranas de excesos
- Oportunidades de venta adicional
- Renovación proactiva de contratos

## Tipos de Usuario y Permisos

### PATCO Administrador
- Configuración completa de tarifas y productos
- Acceso a todos los reportes de rentabilidad
- Configuración de reglas de facturación
- Gestión de excepciones y ajustes

### Gerente Comercial
- Análisis de rentabilidad por cliente
- Configuración de descuentos y condiciones especiales
- Reportes de facturación y cobranza
- Seguimiento de acuerdos comerciales

### Gerente de Operaciones
- Análisis de eficiencia operacional
- Reportes de productividad por técnico
- Optimización de procesos
- Control de costos operacionales

### Contador/Facturación
- Generación y revisión de facturas
- Conciliación de tiempo vs. facturación
- Reportes contables y fiscales
- Gestión de cuentas por cobrar

### PATCO Líder Técnico
- Aprobación de tiempo de su equipo
- Reportes de productividad del área
- Validación de servicios realizados
- Control de calidad de registros

## Flujos de Trabajo Principales

### 1. Facturación Periódica
1. **Consolidación de Tiempo**
   - Recopilación de tiempo registrado en el período
   - Validación por supervisores
   - Aplicación de reglas de redondeo
   - Cálculo de tarifas aplicables

2. **Generación de Órdenes de Venta**
   - Creación automática por cliente/proyecto
   - Aplicación de descuentos contractuales
   - Validación de límites y condiciones
   - Aprobación comercial si es necesaria

3. **Facturación**
   - Generación de facturas desde órdenes aprobadas
   - Aplicación de impuestos y retenciones
   - Envío automático al cliente
   - Registro en cuentas por cobrar

### 2. Facturación por Proyecto
1. **Cierre de Proyecto**
   - Consolidación de todo el tiempo del proyecto
   - Validación de entregables
   - Cálculo de costos totales
   - Aplicación de términos contractuales

2. **Facturación Final**
   - Generación de factura integral
   - Conciliación con anticipos recibidos
   - Liquidación de saldos
   - Cierre contable del proyecto

### 3. Facturación de Emergencias
1. **Identificación Automática**
   - Detección de servicios fuera de horario
   - Aplicación automática de recargos
   - Validación de autorización del cliente
   - Generación de factura express

## Métricas y KPIs Soportados

### Métricas de Facturación
- **Tiempo Facturable vs. Trabajado**: Eficiencia de facturación
- **Valor Promedio por Hora**: Tarifa efectiva promedio
- **Tiempo de Ciclo de Facturación**: Desde servicio hasta cobro
- **Tasa de Aprobación**: Porcentaje de tiempo aprobado para facturación

### Métricas de Rentabilidad
- **Margen Bruto por Servicio**: Rentabilidad individual
- **Margen por Cliente**: Rentabilidad por relación comercial
- **Margen por Técnico**: Productividad individual
- **ROI por Proyecto**: Retorno sobre inversión

### Métricas Operacionales
- **Utilización de Técnicos**: Tiempo facturable vs. disponible
- **Eficiencia de Procesos**: Tiempo productivo vs. total
- **Calidad de Registros**: Precisión en registro de tiempo
- **Cumplimiento de SLA**: Tiempos de respuesta vs. comprometidos

## Reportes Disponibles

### Reportes de Facturación
- Resumen de facturación por período
- Detalle de tiempo facturado por técnico
- Análisis de tarifas aplicadas
- Seguimiento de órdenes de venta

### Reportes de Rentabilidad
- Análisis de margen por cliente
- Rentabilidad por tipo de servicio
- Comparativo de rentabilidad por período
- Análisis de desviaciones vs. presupuesto

### Reportes Operacionales
- Utilización de recursos humanos
- Eficiencia por técnico y área
- Análisis de productividad
- Identificación de oportunidades de mejora

## Beneficios del Módulo

1. **Automatización Completa**: Eliminación de facturación manual
2. **Precisión en Costos**: Facturación basada en tiempo real trabajado
3. **Mejora de Márgenes**: Optimización de tarifas y eficiencia
4. **Transparencia**: Trazabilidad completa de tiempo a factura
5. **Cumplimiento Contractual**: Validación automática de acuerdos
6. **Análisis Estratégico**: Base de datos para decisiones comerciales
7. **Reducción de Errores**: Minimización de errores de facturación manual
8. **Mejora de Flujo de Caja**: Facturación más rápida y precisa

## Integración con Sistemas Externos

### Sistemas Contables
- Exportación automática de asientos contables
- Integración con sistemas ERP corporativos
- Sincronización con software de nómina
- Conexión con plataformas de facturación electrónica

### Sistemas de Cobranza
- Integración con plataformas de gestión de cobranza
- Automatización de seguimiento de cuentas por cobrar
- Alertas de vencimientos y morosidad
- Reportes de aging de cartera

## Versión

Compatible con Odoo 18 Community Edition.

## Soporte e Implementación

La implementación exitosa de este módulo requiere:

1. **Configuración Detallada**: Setup preciso de tarifas y productos
2. **Capacitación de Usuarios**: Entrenamiento en procesos de facturación
3. **Integración Contable**: Configuración de cuentas y centros de costo
4. **Validación de Procesos**: Pruebas exhaustivas antes de go-live
5. **Monitoreo Inicial**: Seguimiento cercano de primeras facturaciones
6. **Optimización Continua**: Ajustes basados en resultados operacionales

Este módulo es crítico para la viabilidad económica del ecosistema PATCO, asegurando que todos los servicios prestados se conviertan eficientemente en ingresos facturados y cobrados.