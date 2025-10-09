# Campos de la Vista FSM Order Form PATCO

## Descripción General
Este documento detalla todos los campos que se muestran en la vista extendida `fsm_order_form_view_patco` del módulo `patco_fsm`. La vista extiende el formulario base de Field Service para agregar funcionalidades específicas del proyecto PATCO.

---

## 1. Botones Estadísticos (Button Box)

### `consumed_parts_count`
- **Nombre de Negocio**: "Contador de Repuestos Utilizados"
- **Descripción para Tooltip**: "Muestra la cantidad total de repuestos y materiales que se han consumido durante la ejecución de esta orden de servicio. Haga clic para ver el detalle de cada repuesto utilizado."
- **Tipo**: Integer (contador)
- **Widget**: statinfo
- **Etiqueta**: "Repuestos"
- **Función**: Muestra el número total de repuestos consumidos en la orden de servicio
- **Acción**: Al hacer clic, abre la vista de repuestos consumidos

### `worksheet_count`
- **Nombre de Negocio**: "Contador de Hojas de Trabajo"
- **Descripción para Tooltip**: "Indica cuántas hojas de trabajo (formularios de inspección, checklists, reportes) están asociadas a esta orden de servicio. Haga clic para acceder a todas las hojas de trabajo."
- **Tipo**: Integer (contador)
- **Widget**: statinfo
- **Etiqueta**: "Hojas de Trabajo"
- **Función**: Muestra el número de hojas de trabajo asociadas a la orden
- **Acción**: Al hacer clic, abre la vista de hojas de trabajo

### `timesheet_count`
- **Nombre de Negocio**: "Contador de Registros de Tiempo"
- **Descripción para Tooltip**: "Muestra cuántos registros de tiempo (entradas de horas trabajadas) se han creado para esta orden de servicio. Útil para control de horas y facturación. Haga clic para ver el detalle de tiempo registrado."
- **Tipo**: Integer (contador)
- **Widget**: statinfo
- **Etiqueta**: "Registros Tiempo"
- **Función**: Muestra el número de registros de tiempo asociados
- **Acción**: Al hacer clic, abre la vista de registros de tiempo

---

## 2. Sección "Clasificación PATCO"

### `x_nature_id`
- **Nombre de Negocio**: "Naturaleza del Trabajo"
- **Descripción para Tooltip**: "Seleccione el tipo de trabajo a realizar: Preventivo (mantenimiento programado), Correctivo (reparación de fallas), Predictivo (basado en análisis), etc. Esta clasificación es importante para reportes y planificación."
- **Tipo**: Many2one
- **Modelo relacionado**: Naturaleza del trabajo
- **Función**: Clasifica el tipo de naturaleza del trabajo (preventivo, correctivo, etc.)
- **Opciones**: No permite crear ni editar desde la vista
- **Propósito**: Categorización para reportes y análisis

### `x_area_id`
- **Nombre de Negocio**: "Área de Trabajo"
- **Descripción para Tooltip**: "Seleccione el área geográfica o departamental donde se ejecutará el servicio (ej: Zona Norte, Planta Industrial, Oficinas Administrativas). Ayuda a organizar rutas y asignar técnicos por zona."
- **Tipo**: Many2one
- **Modelo relacionado**: Área de trabajo
- **Función**: Define el área específica donde se realizará el trabajo
- **Opciones**: No permite crear ni editar desde la vista
- **Propósito**: Organización territorial y asignación de recursos

### `x_complexity_id`
- **Nombre de Negocio**: "Nivel de Complejidad"
- **Descripción para Tooltip**: "Indique la complejidad técnica del trabajo: Básica (tareas simples), Intermedia (requiere experiencia), Avanzada (especialista requerido). Ayuda a asignar el técnico adecuado y estimar tiempos."
- **Tipo**: Many2one
- **Modelo relacionado**: Complejidad del trabajo
- **Función**: Indica el nivel de complejidad técnica requerida
- **Opciones**: No permite crear ni editar desde la vista
- **Propósito**: Planificación de recursos y tiempo estimado

### `x_classification_code`
- **Nombre de Negocio**: "Código de Clasificación PATCO"
- **Descripción para Tooltip**: "Código único generado automáticamente que combina la naturaleza, área y complejidad del trabajo. Útil para identificación rápida y reportes estadísticos."
- **Tipo**: Char
- **Modo**: Solo lectura
- **Función**: Código automático generado basado en la clasificación PATCO
- **Propósito**: Identificación rápida y codificación estándar

---

## 3. Sección "Estado de Hojas de Trabajo"

### `has_signed_worksheet`
- **Nombre de Negocio**: "Hojas de Trabajo Firmadas"
- **Descripción para Tooltip**: "Indica si el cliente o supervisor ha firmado al menos una hoja de trabajo, confirmando la conformidad con el servicio realizado. Importante para el cierre formal de la orden."
- **Tipo**: Boolean
- **Modo**: Solo lectura
- **Función**: Indica si existe al menos una hoja de trabajo firmada
- **Propósito**: Control de calidad y validación de trabajos completados

### `worksheet_completion_rate`
- **Nombre de Negocio**: "Porcentaje de Avance de Hojas de Trabajo"
- **Descripción para Tooltip**: "Muestra el progreso promedio de completitud de todas las hojas de trabajo asociadas. Un 100% indica que todas las tareas y verificaciones han sido completadas."
- **Tipo**: Float
- **Widget**: percentage
- **Modo**: Solo lectura
- **Función**: Muestra el porcentaje promedio de completitud de todas las hojas de trabajo
- **Propósito**: Seguimiento del progreso del trabajo

### `total_timesheet_time`
- **Nombre de Negocio**: "Tiempo Total Registrado"
- **Descripción para Tooltip**: "Suma total de horas trabajadas registradas por todos los técnicos en esta orden de servicio. Se utiliza para control de productividad y facturación de mano de obra."
- **Tipo**: Float
- **Función**: Suma total del tiempo registrado en la orden
- **Propósito**: Control de horas trabajadas y facturación

### `is_timer_running`
- **Nombre de Negocio**: "Timer Activo"
- **Descripción para Tooltip**: "Indica si actualmente hay un cronómetro en funcionamiento registrando tiempo de trabajo en esta orden. Útil para saber si un técnico está trabajando en tiempo real."
- **Tipo**: Boolean
- **Función**: Indica si hay un timer activo registrando tiempo
- **Propósito**: Control en tiempo real del registro de horas

### `current_timesheet_id`
- **Nombre de Negocio**: "Registro de Tiempo Actual"
- **Descripción para Tooltip**: "Referencia al registro de tiempo que está actualmente en curso. Permite gestionar y controlar la sesión de trabajo activa del técnico asignado."
- **Tipo**: Many2one
- **Modelo relacionado**: account.analytic.line (timesheet)
- **Función**: Referencia al registro de tiempo actualmente activo
- **Propósito**: Gestión del timer y registro actual

---

## 4. Sección "Habilidades Requeridas"

### `x_required_skill_types`
- **Nombre de Negocio**: "Habilidades Técnicas Requeridas"
- **Descripción para Tooltip**: "Seleccione las competencias técnicas necesarias para realizar este trabajo (ej: Electricidad, Mecánica, Soldadura). El sistema ayudará a asignar técnicos calificados."
- **Tipo**: Many2many
- **Widget**: many2many_tags
- **Modelo relacionado**: Tipos de habilidades
- **Función**: Define las habilidades técnicas necesarias para completar el trabajo
- **Propósito**: Asignación inteligente de técnicos

### `x_min_skill_level`
- **Nombre de Negocio**: "Nivel Mínimo de Experiencia"
- **Descripción para Tooltip**: "Establezca el nivel mínimo de experiencia requerido para las habilidades técnicas (ej: Básico, Intermedio, Avanzado, Experto). Ayuda a filtrar técnicos apropiados."
- **Tipo**: Selection/Integer
- **Función**: Nivel mínimo de habilidad requerido
- **Propósito**: Filtrado de técnicos calificados

### `x_skill_match_warning`
- **Nombre de Negocio**: "Alerta de Habilidades"
- **Descripción para Tooltip**: "Muestra advertencias automáticas cuando el técnico asignado no posee las habilidades o nivel de experiencia requeridos para este trabajo. Ayuda a prevenir asignaciones inadecuadas."
- **Tipo**: Text
- **Modo**: Solo lectura
- **Visibilidad**: Condicional (solo si hay advertencia)
- **Función**: Muestra advertencias cuando el técnico asignado no cumple los requisitos
- **Propósito**: Alerta temprana de posibles problemas de asignación

---

## 5. Sección "Información del Activo"

### `x_equipment_category_name`
- **Nombre de Negocio**: "Categoría del Equipo"
- **Descripción para Tooltip**: "Muestra la categoría del equipo o activo asociado a esta orden (ej: Bomba, Motor, Compresor). Información automática que ayuda a identificar el tipo de equipo a intervenir."
- **Tipo**: Char
- **Modo**: Solo lectura
- **Etiqueta**: "Categoría"
- **Función**: Muestra la categoría del equipo asociado
- **Visibilidad**: Solo cuando hay equipo seleccionado
- **Propósito**: Información contextual del activo

### `x_equipment_brand_model`
- **Nombre de Negocio**: "Marca y Modelo del Equipo"
- **Descripción para Tooltip**: "Información específica de la marca y modelo del equipo a intervenir. Útil para identificar repuestos compatibles y procedimientos específicos del fabricante."
- **Tipo**: Char
- **Modo**: Solo lectura
- **Etiqueta**: "Marca/Modelo"
- **Función**: Información de marca y modelo del equipo
- **Propósito**: Identificación específica del activo

### `x_equipment_location_name`
- **Nombre de Negocio**: "Ubicación del Equipo"
- **Descripción para Tooltip**: "Ubicación física específica donde se encuentra el equipo (ej: Planta Baja - Sala de Máquinas, Piso 3 - Oficina 301). Ayuda al técnico a localizar rápidamente el activo."
- **Tipo**: Char
- **Modo**: Solo lectura
- **Etiqueta**: "Ubicación"
- **Función**: Ubicación física del equipo
- **Propósito**: Logística y planificación de rutas

---

## 6. Pestañas Adicionales

### Pestaña "Checklist de Entrada"
#### `x_entry_checklist`
- **Nombre de Negocio**: "Lista de Verificación de Entrada"
- **Descripción para Tooltip**: "Checklist de seguridad y procedimientos que debe completar el técnico antes de iniciar el trabajo. Incluye verificaciones de EPP, herramientas, condiciones del sitio, etc."
- **Tipo**: Html
- **Widget**: html
- **Función**: Lista de verificación que debe completarse al iniciar el trabajo
- **Propósito**: Estandarización de procedimientos de inicio

### Pestaña "Checklist de Salida"
#### `x_exit_checklist`
- **Nombre de Negocio**: "Lista de Verificación de Salida"
- **Descripción para Tooltip**: "Checklist de cierre que debe completar el técnico al finalizar el trabajo. Incluye limpieza del área, pruebas finales, entrega de llaves, documentación, etc."
- **Tipo**: Html
- **Widget**: html
- **Función**: Lista de verificación que debe completarse al finalizar el trabajo
- **Propósito**: Estandarización de procedimientos de cierre

### Pestaña "Hojas de Trabajo"
#### `worksheet_ids`
- **Nombre de Negocio**: "Hojas de Trabajo Asociadas"
- **Descripción para Tooltip**: "Lista completa de todas las hojas de trabajo, formularios de inspección y reportes asociados a esta orden. Permite crear, editar y revisar el progreso de cada documento."
- **Tipo**: One2many
- **Modelo relacionado**: Hojas de trabajo
- **Función**: Lista de todas las hojas de trabajo asociadas
- **Campos mostrados**:
  - `name`: Nombre de la hoja
  - `template_id`: Plantilla utilizada
  - `state`: Estado actual
  - `completion_percentage`: Porcentaje de completitud

### Pestaña "Repuestos Consumidos"
#### `x_consumed_parts_ids`
- **Nombre de Negocio**: "Registro de Repuestos Consumidos"
- **Descripción para Tooltip**: "Lista detallada de todos los repuestos, materiales y consumibles utilizados durante el servicio. Permite registrar cantidades, costos y controlar el inventario consumido."
- **Tipo**: One2many
- **Modo**: Lista editable
- **Función**: Registro de repuestos utilizados en el trabajo
- **Campos editables**:
  - `product_id`: Producto/repuesto
  - `quantity`: Cantidad utilizada
  - `product_uom_id`: Unidad de medida
  - `unit_cost`: Costo unitario (calculado)
  - `total_cost`: Costo total (calculado)
  - `state`: Estado del consumo

#### `x_total_parts_cost`
- **Nombre de Negocio**: "Costo Total de Repuestos"
- **Descripción para Tooltip**: "Suma automática del valor total de todos los repuestos y materiales consumidos en esta orden. Se actualiza automáticamente al agregar o modificar items en la lista de consumos."
- **Tipo**: Monetary
- **Modo**: Solo lectura
- **Etiqueta**: "Total Repuestos"
- **Función**: Suma total del costo de todos los repuestos consumidos
- **Propósito**: Control de costos y facturación

### Pestaña "Facturación"
#### `invoice_policy`
- **Nombre de Negocio**: "Política de Facturación"
- **Descripción para Tooltip**: "Establece cómo se generará la factura para esta orden: Manual (crear factura manualmente), Automática (al completar la orden), Por tiempo (facturar horas), etc."
- **Tipo**: Selection
- **Función**: Define la política de facturación (manual, automática, etc.)
- **Propósito**: Control del proceso de facturación

#### `service_product_id`
- **Nombre de Negocio**: "Producto de Servicio"
- **Descripción para Tooltip**: "Seleccione el producto o servicio estándar que se facturará por esta orden (ej: Mantenimiento Preventivo, Reparación Correctiva, Inspección Técnica). Define precio y descripción para facturación."
- **Tipo**: Many2one
- **Modelo relacionado**: product.product
- **Función**: Producto de servicio a facturar
- **Propósito**: Estandarización de servicios facturables

#### `auto_invoice_time`
- **Nombre de Negocio**: "Facturación Automática de Tiempo"
- **Descripción para Tooltip**: "Active esta opción para que las horas registradas en esta orden se facturen automáticamente según las tarifas configuradas. Útil para servicios por horas."
- **Tipo**: Boolean
- **Función**: Activa la facturación automática del tiempo registrado
- **Propósito**: Automatización de procesos de facturación

#### `auto_invoice_materials`
- **Nombre de Negocio**: "Facturación Automática de Materiales"
- **Descripción para Tooltip**: "Active esta opción para que todos los repuestos y materiales consumidos se facturen automáticamente al cliente. Los precios se toman del catálogo de productos."
- **Tipo**: Boolean
- **Función**: Activa la facturación automática de materiales consumidos
- **Propósito**: Automatización de facturación de repuestos

### Pestaña "Registro de Tiempo"
#### `is_timer_running` (duplicado)
- **Nombre de Negocio**: "Estado del Cronómetro" (duplicado)
- **Descripción para Tooltip**: "Indicador visual del estado del cronómetro en la pestaña de registro de tiempo. Muestra si hay una sesión de trabajo activa en curso."
- **Tipo**: Boolean
- **Modo**: Solo lectura
- **Función**: Estado del timer (duplicado para control)

#### `total_timesheet_time` (duplicado)
- **Nombre de Negocio**: "Tiempo Total Acumulado" (duplicado)
- **Descripción para Tooltip**: "Resumen del tiempo total registrado, mostrado también en la pestaña de registro de tiempo para facilitar el control y seguimiento de horas trabajadas."
- **Tipo**: Float
- **Widget**: float_time
- **Modo**: Solo lectura
- **Función**: Tiempo total registrado (duplicado para control)

---

## 7. Campo con Filtro Extendido

### `x_skill_match_warning` (en filtro de person_id)
- **Nombre de Negocio**: "Validación de Habilidades del Técnico"
- **Descripción para Tooltip**: "Alerta automática que aparece cuando el técnico seleccionado no cumple con las habilidades o nivel de experiencia requeridos. Ayuda a evitar asignaciones inadecuadas antes de confirmar."
- **Ubicación**: Después del campo person_id
- **Tipo**: Text
- **Modo**: Solo lectura
- **Función**: Advertencia contextual sobre coincidencia de habilidades
- **Visibilidad**: Solo cuando hay advertencia y habilidades requeridas
- **Propósito**: Validación en tiempo real de asignaciones

---

## Resumen Estadístico

- **Total de campos únicos**: 30
- **Campos de solo lectura**: 12
- **Campos editables**: 18
- **Campos con widgets especiales**: 8
- **Relaciones Many2one**: 8
- **Relaciones One2many**: 2
- **Relaciones Many2many**: 1
- **Campos booleanos**: 6
- **Campos de texto/HTML**: 2
- **Campos monetarios**: 3

---

## Notas Técnicas

1. **Herencia**: La vista extiende `fieldservice.fsm_order_form` usando xpath
2. **Visibilidad condicional**: Varios campos usan atributos `invisible` para mostrar/ocultar según contexto
3. **Widgets especializados**: Se utilizan widgets como `statinfo`, `percentage`, `html`, `many2many_tags`
4. **Integración**: Los campos se integran con módulos OCA de Field Service, HR Skills y Timesheet
5. **Automatización**: Varios campos son calculados automáticamente (códigos, totales, contadores)

---

*Documento generado automáticamente para el Proyecto PATCO - Odoo 18 Community Edition*