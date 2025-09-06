# Field Service Sale Timesheet - Integración de Hojas de Tiempo con Ventas

## Descripción

Field Service Sale Timesheet es un módulo especializado que integra las hojas de tiempo de servicios de campo con el sistema de ventas y facturación de Odoo. Este módulo es esencial en el ecosistema PATCO para automatizar el proceso de facturación basado en tiempo real trabajado, materiales consumidos y servicios prestados en operaciones de mantenimiento HORECA.

## Función en el Ecosistema PATCO

Este módulo actúa como el puente entre la ejecución operacional y la facturación comercial, proporcionando:

- **Facturación Automática**: Conversión automática de tiempo trabajado en líneas de factura
- **Integración Tiempo-Venta**: Vinculación directa entre órdenes de servicio y órdenes de venta
- **Costeo Preciso**: Cálculo automático de costos basado en tiempo real y materiales
- **Análisis de Rentabilidad**: Métricas de margen por servicio y cliente
- **Facturación Diferenciada**: Tarifas específicas por tipo de servicio y técnico
- **Cumplimiento Contractual**: Validación automática contra acuerdos de servicio

## Dependencias del Módulo

### Módulos Odoo Core
- `base`
- `sale`
- `account`
- `hr_timesheet`
- `fieldservice`
- `sale_timesheet`

### Módulos OCA
- `fieldservice_sale`
- `fieldservice_account_analytic`
- `sale_timesheet_existing_project`

### Módulos PATCO
- `patco_core` (para naturalezas de servicio)
- `fieldservice_timesheet` (para registro de tiempo)

## Funcionalidades Principales

### 1. Integración Automática Tiempo-Facturación

#### Conversión Automática
- **Tiempo a Líneas de Venta**: Conversión automática de horas trabajadas en líneas facturables
- **Tarifas Dinámicas**: Aplicación de tarifas específicas por tipo de servicio, técnico y cliente
- **Agrupación Inteligente**: Consolidación de tiempo por período, proyecto o tipo de servicio
- **Validación de Tiempo**: Verificación de horas registradas antes de facturación

#### Configuración de Tarifas
- **Tarifas por Naturaleza de Servicio**: Precios diferenciados según tipo de trabajo
- **Tarifas por Técnico**: Valorización según nivel de experiencia y certificaciones
- **Tarifas por Cliente**: Precios contractuales específicos
- **Tarifas por Horario**: Diferenciación entre horario normal, nocturno y festivos

### 2. Gestión de Órdenes de Venta Vinculadas

#### Creación Automática
- Generación automática de órdenes de venta desde órdenes de servicio
- Pre-población con información del cliente y proyecto
- Configuración automática de productos y servicios
- Aplicación de descuentos y condiciones contractuales

#### Seguimiento de Facturación
- Estado de facturación por orden de servicio
- Seguimiento de tiempo facturable vs. facturado
- Control de límites contractuales
- Alertas de excesos o desviaciones

### 3. Análisis de Rentabilidad

#### Métricas por Servicio
- **Costo Real**: Tiempo invertido valorizado + materiales + gastos
- **Precio de Venta**: Valor facturado al cliente
- **Margen Bruto**: Diferencia entre precio de venta y costo
- **Margen Porcentual**: Rentabilidad relativa del servicio

#### Análisis Comparativo
- Rentabilidad por cliente
- Rentabilidad por tipo de servicio
- Rentabilidad por técnico
- Tendencias de margen por período

### 4. Facturación Diferenciada

#### Tipos de Facturación
- **Por Tiempo**: Facturación basada en horas trabajadas
- **Por Servicio**: Tarifa fija por tipo de trabajo realizado
- **Mixta**: Combinación de tiempo base + materiales + extras
- **Contractual**: Según términos de acuerdos de servicio

#### Configuración Avanzada
- Redondeo de tiempo (15 min, 30 min, 1 hora)
- Tiempo mínimo facturable por servicio
- Descuentos automáticos por volumen
- Recargos por servicios de emergencia

### 5. Integración con Contratos de Servicio

#### Validación Contractual
- Verificación de límites de horas incluidas
- Control de servicios cubiertos vs. adicionales
- Aplicación automática de tarifas contractuales
- Alertas de excesos de consumo

#### Facturación de Excesos
- Identificación automática de servicios fuera de contrato
- Aplicación de tarifas de exceso
- Generación de facturas separadas para adicionales
- Notificación automática al cliente

## Configuración Necesaria

### Configuración de Productos de Servicio

1. **Productos por Naturaleza de Servicio**
   ```
   - Mantenimiento Preventivo
     - Precio: $X por hora
     - Cuenta contable: Ingresos por Mantenimiento
   - Mantenimiento Correctivo
     - Precio: $Y por hora
     - Cuenta contable: Ingresos por Reparación
   - Servicio de Emergencia
     - Precio: $Z por hora (recargo incluido)
     - Cuenta contable: Ingresos por Emergencia
   ```

2. **Configuración de Empleados**
   - Costo por hora de cada técnico
   - Tarifa de venta por técnico
   - Categoría de facturación
   - Cuenta analítica por defecto

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