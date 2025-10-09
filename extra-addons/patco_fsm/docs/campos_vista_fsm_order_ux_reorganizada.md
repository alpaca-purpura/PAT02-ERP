# Vista FSM Order Form PATCO - Reorganizada para Jefe de Operaciones

## Descripción General
Esta reorganización UX optimiza la vista para el flujo del jefe de operaciones: clasificación inicial, información del activo y cliente, asignación de técnico con validación de habilidades, logística de herramientas y viáticos, planificación temporal, control de ejecución y cierre, con pestañas para detalles operativos.

---

## SECCIÓN 1: INFORMACIÓN BÁSICA Y CLASIFICACIÓN

### `x_classification_code`
- **Nombre de Negocio**: "Código de Clasificación PATCO"
- **Descripción para Tooltip**: "Código único generado automáticamente que combina la naturaleza, área y complejidad del trabajo. Útil para identificación rápida y reportes estadísticos."
- **Tipo**: Char
- **Modo**: Solo lectura

### `x_nature_id`
- **Nombre de Negocio**: "Naturaleza del Trabajo"
- **Descripción para Tooltip**: "Seleccione el tipo de trabajo a realizar: Preventivo (mantenimiento programado), Correctivo (reparación de fallas), Predictivo (basado en análisis), etc. Esta clasificación es importante para reportes y planificación."
- **Tipo**: Many2one
- **Modelo relacionado**: Naturaleza del trabajo

### `x_area_id`
- **Nombre de Negocio**: "Área de Trabajo"
- **Descripción para Tooltip**: "Seleccione el área geográfica o departamental donde se ejecutará el servicio (ej: Zona Norte, Planta Industrial, Oficinas Administrativas). Ayuda a organizar rutas y asignar técnicos por zona."
- **Tipo**: Many2one
- **Modelo relacionado**: Área de trabajo

### `x_complexity_id`
- **Nombre de Negocio**: "Nivel de Complejidad"
- **Descripción para Tooltip**: "Indique la complejidad técnica del trabajo: Básica (tareas simples), Intermedia (requiere experiencia), Avanzada (especialista requerido). Ayuda a asignar el técnico adecuado y estimar tiempos."
- **Tipo**: Many2one
- **Modelo relacionado**: Complejidad del trabajo

---

## SECCIÓN 2: INFORMACIÓN DEL CLIENTE Y ACTIVO

### `x_equipment_category_name`
- **Nombre de Negocio**: "Categoría del Equipo"
- **Descripción para Tooltip**: "Muestra la categoría del equipo o activo asociado a esta orden (ej: Bomba, Motor, Compresor). Información automática que ayuda a identificar el tipo de equipo a intervenir."
- **Tipo**: Char
- **Modo**: Solo lectura

### `x_equipment_brand_model`
- **Nombre de Negocio**: "Marca y Modelo del Equipo"
- **Descripción para Tooltip**: "Información específica de la marca y modelo del equipo a intervenir. Útil para identificar repuestos compatibles y procedimientos específicos del fabricante."
- **Tipo**: Char
- **Modo**: Solo lectura

### `x_equipment_location_name`
- **Nombre de Negocio**: "Ubicación del Equipo"
- **Descripción para Tooltip**: "Ubicación física específica donde se encuentra el equipo (ej: Planta Baja - Sala de Máquinas, Piso 3 - Oficina 301). Ayuda al técnico a localizar rápidamente el activo."
- **Tipo**: Char
- **Modo**: Solo lectura

### `x_detailed_location` (PROPUESTA - NO EXISTE)
- **Nombre de Negocio**: "Ubicación Detallada"
- **Descripción para Tooltip**: "Descripción detallada de la ubicación, incluyendo indicaciones de acceso, referencias y contactos en sitio."
- **Tipo**: Text

### `x_client_contact` (PROPUESTA - NO EXISTE)
- **Nombre de Negocio**: "Contacto del Cliente"
- **Descripción para Tooltip**: "Información de contacto principal en el sitio del cliente para coordinaciones."
- **Tipo**: Many2one
- **Modelo relacionado**: res.partner

### `x_asset_ids` (PROPUESTA - NO EXISTE)
- **Nombre de Negocio**: "Activos a Revisar"
- **Descripción para Tooltip**: "Lista de activos específicos del cliente que se deben revisar, mantener o reparar en esta visita."
- **Tipo**: One2many
- **Modelo relacionado**: maintenance.equipment

---

## SECCIÓN 3: ASIGNACIÓN DE TÉCNICO Y HABILIDADES

### `person_id` (Campo base de Odoo, propuesto para extensión)
- **Nombre de Negocio**: "Técnico Asignado"
- **Descripción para Tooltip**: "Seleccione el técnico responsable de ejecutar esta orden de servicio. El sistema validará automáticamente las habilidades requeridas."
- **Tipo**: Many2one
- **Modelo relacionado**: hr.employee

### `x_required_skill_types`
- **Nombre de Negocio**: "Habilidades Técnicas Requeridas"
- **Descripción para Tooltip**: "Seleccione las competencias técnicas necesarias para realizar este trabajo (ej: Electricidad, Mecánica, Soldadura). El sistema ayudará a asignar técnicos calificados."
- **Tipo**: Many2many
- **Widget**: many2many_tags

### `x_min_skill_level`
- **Nombre de Negocio**: "Nivel Mínimo de Experiencia"
- **Descripción para Tooltip**: "Establezca el nivel mínimo de experiencia requerido para las habilidades técnicas (ej: Básico, Intermedio, Avanzado, Experto). Ayuda a filtrar técnicos apropiados."
- **Tipo**: Selection/Integer

### `x_skill_match_warning`
- **Nombre de Negocio**: "Alerta de Habilidades"
- **Descripción para Tooltip**: "Muestra advertencias automáticas cuando el técnico asignado no posee las habilidades o nivel de experiencia requeridos para este trabajo. Ayuda a prevenir asignaciones inadecuadas."
- **Tipo**: Text
- **Modo**: Solo lectura

### `x_backup_technician_id` (PROPUESTA - NO EXISTE)
- **Nombre de Negocio**: "Técnico de Respaldo"
- **Descripción para Tooltip**: "Técnico alternativo en caso de que el principal no esté disponible."
- **Tipo**: Many2one
- **Modelo relacionado**: hr.employee

---

## SECCIÓN 4: HERRAMIENTAS, RECURSOS Y VIÁTICOS

### `x_required_tools_ids` (PROPUESTA - NO EXISTE)
- **Nombre de Negocio**: "Herramientas Requeridas"
- **Descripción para Tooltip**: "Lista de herramientas que los técnicos deben llevar para completar el trabajo."
- **Tipo**: Many2many
- **Widget**: many2many_tags

### `x_special_equipment_ids` (PROPUESTA - NO EXISTE)
- **Nombre de Negocio**: "Equipos Especiales"
- **Descripción para Tooltip**: "Equipos o herramientas especiales necesarias para la visita."
- **Tipo**: Many2many

### `x_viaticos_amount` (PROPUESTA - NO EXISTE)
- **Nombre de Negocio**: "Viáticos Autorizados"
- **Descripción para Tooltip**: "Monto autorizado para viáticos y gastos de viaje."
- **Tipo**: Monetary

### `x_transport_method` (PROPUESTA - NO EXISTE)
- **Nombre de Negocio**: "Método de Transporte"
- **Descripción para Tooltip**: "Método de transporte para llegar al sitio (vehículo propio, empresa, etc.)."
- **Tipo**: Selection

---

## SECCIÓN 5: PLANIFICACIÓN TEMPORAL

### `scheduled_date_begin` (Campo base de Odoo)
- **Nombre de Negocio**: "Fecha Programada de Inicio"
- **Descripción para Tooltip**: "Fecha y hora programada para iniciar el servicio."
- **Tipo**: Datetime

### `x_estimated_duration` (PROPUESTA - NO EXISTE)
- **Nombre de Negocio**: "Duración Estimada"
- **Descripción para Tooltip**: "Tiempo estimado para completar el trabajo."
- **Tipo**: Float
- **Widget**: float_time

---

## SECCIÓN 6: CONTROL DE EJECUCIÓN Y PROGRESO

### `is_timer_running`
- **Nombre de Negocio**: "Timer Activo"
- **Descripción para Tooltip**: "Indica si actualmente hay un cronómetro en funcionamiento registrando tiempo de trabajo en esta orden. Útil para saber si un técnico está trabajando en tiempo real."
- **Tipo**: Boolean

### `current_timesheet_id`
- **Nombre de Negocio**: "Registro de Tiempo Actual"
- **Descripción para Tooltip**: "Referencia al registro de tiempo que está actualmente en curso. Permite gestionar y controlar la sesión de trabajo activa del técnico asignado."
- **Tipo**: Many2one

### `total_timesheet_time`
- **Nombre de Negocio**: "Tiempo Total Registrado"
- **Descripción para Tooltip**: "Suma total de horas trabajadas registradas por todos los técnicos en esta orden de servicio. Se utiliza para control de productividad y facturación de mano de obra."
- **Tipo**: Float

### `worksheet_completion_rate`
- **Nombre de Negocio**: "Porcentaje de Avance de Hojas de Trabajo"
- **Descripción para Tooltip**: "Muestra el progreso promedio de completitud de todas las hojas de trabajo asociadas. Un 100% indica que todas las tareas y verificaciones han sido completadas."
- **Tipo**: Float
- **Widget**: percentage

### `has_signed_worksheet`
- **Nombre de Negocio**: "Hojas de Trabajo Firmadas"
- **Descripción para Tooltip**: "Indica si el cliente o supervisor ha firmado al menos una hoja de trabajo, confirmando la conformidad con el servicio realizado. Importante para el cierre formal de la orden."
- **Tipo**: Boolean

---

## BOTONES ESTADÍSTICOS (BUTTON BOX)

### `consumed_parts_count`
- **Nombre de Negocio**: "Contador de Repuestos Utilizados"
- **Descripción para Tooltip**: "Muestra la cantidad total de repuestos y materiales que se han consumido durante la ejecución de esta orden de servicio. Haga clic para ver el detalle de cada repuesto utilizado."
- **Tipo**: Integer (contador)
- **Widget**: statinfo

### `worksheet_count`
- **Nombre de Negocio**: "Contador de Hojas de Trabajo"
- **Descripción para Tooltip**: "Indica cuántas hojas de trabajo (formularios de inspección, checklists, reportes) están asociadas a esta orden de servicio. Haga clic para acceder a todas las hojas de trabajo."
- **Tipo**: Integer (contador)
- **Widget**: statinfo

### `timesheet_count`
- **Nombre de Negocio**: "Contador de Registros de Tiempo"
- **Descripción para Tooltip**: "Muestra cuántos registros de tiempo (entradas de horas trabajadas) se han creado para esta orden de servicio. Útil para control de horas y facturación. Haga clic para ver el detalle de tiempo registrado."
- **Tipo**: Integer (contador)
- **Widget**: statinfo

---

## PESTAÑAS OPERATIVAS

### Pestaña "Checklist de Entrada"
#### `x_entry_checklist`
- **Nombre de Negocio**: "Lista de Verificación de Entrada"
- **Descripción para Tooltip**: "Checklist de seguridad y procedimientos que debe completar el técnico antes de iniciar el trabajo. Incluye verificaciones de EPP, herramientas, condiciones del sitio, etc."
- **Tipo**: Html
- **Widget**: html

### Pestaña "Hojas de Trabajo"
#### `worksheet_ids`
- **Nombre de Negocio**: "Hojas de Trabajo Asociadas"
- **Descripción para Tooltip**: "Lista completa de todas las hojas de trabajo, formularios de inspección y reportes asociados a esta orden. Permite crear, editar y revisar el progreso de cada documento."
- **Tipo**: One2many

### Pestaña "Repuestos Consumidos"
#### `x_consumed_parts_ids`
- **Nombre de Negocio**: "Registro de Repuestos Consumidos"
- **Descripción para Tooltip**: "Lista detallada de todos los repuestos, materiales y consumibles utilizados durante el servicio. Permite registrar cantidades, costos y controlar el inventario consumido."
- **Tipo**: One2many

#### `x_total_parts_cost`
- **Nombre de Negocio**: "Costo Total de Repuestos"
- **Descripción para Tooltip**: "Suma automática del valor total de todos los repuestos y materiales consumidos en esta orden. Se actualiza automáticamente al agregar o modificar items en la lista de consumos."
- **Tipo**: Monetary

### Pestaña "Checklist de Salida"
#### `x_exit_checklist`
- **Nombre de Negocio**: "Lista de Verificación de Salida"
- **Descripción para Tooltip**: "Checklist de cierre que debe completar el técnico al finalizar el trabajo. Incluye limpieza del área, pruebas finales, entrega de llaves, documentación, etc."
- **Tipo**: Html
- **Widget**: html

### Pestaña "Facturación"
#### `invoice_policy`
- **Nombre de Negocio**: "Política de Facturación"
- **Descripción para Tooltip**: "Establece cómo se generará la factura para esta orden: Manual (crear factura manualmente), Automática (al completar la orden), Por tiempo (facturar horas), etc."
- **Tipo**: Selection

#### `service_product_id`
- **Nombre de Negocio**: "Producto de Servicio"
- **Descripción para Tooltip**: "Seleccione el producto o servicio estándar que se facturará por esta orden (ej: Mantenimiento Preventivo, Reparación Correctiva, Inspección Técnica). Define precio y descripción para facturación."
- **Tipo**: Many2one

#### `auto_invoice_time`
- **Nombre de Negocio**: "Facturación Automática de Tiempo"
- **Descripción para Tooltip**: "Active esta opción para que las horas registradas en esta orden se facturen automáticamente según las tarifas configuradas. Útil para servicios por horas."
- **Tipo**: Boolean

#### `auto_invoice_materials`
- **Nombre de Negocio**: "Facturación Automática de Materiales"
- **Descripción para Tooltip**: "Active esta opción para que todos los repuestos y materiales consumidos se facturen automáticamente al cliente. Los precios se toman del catálogo de productos."
- **Tipo**: Boolean

### Pestaña "Registro de Tiempo" (Duplicados para referencia)
#### `is_timer_running` (duplicado)
- **Nombre de Negocio**: "Estado del Cronómetro" (duplicado)
- **Descripción para Tooltip**: "Indicador visual del estado del cronómetro en la pestaña de registro de tiempo. Muestra si hay una sesión de trabajo activa en curso."
- **Tipo**: Boolean

#### `total_timesheet_time` (duplicado)
- **Nombre de Negocio**: "Tiempo Total Acumulado" (duplicado)
- **Descripción para Tooltip**: "Resumen del tiempo total registrado, mostrado también en la pestaña de registro de tiempo para facilitar el control y seguimiento de horas trabajadas."
- **Tipo**: Float

---

## CAMPOS NO RECOMENDADOS (MOVER A SECCIÓN AVANZADA O CONFIGURACIÓN)

### `x_skill_match_warning` (duplicado en filtro)
- **Nombre de Negocio**: "Validación de Habilidades del Técnico"
- **Descripción para Tooltip**: "Alerta automática que aparece cuando el técnico seleccionado no cumple con las habilidades o nivel de experiencia requeridos. Ayuda a evitar asignaciones inadecuadas antes de confirmar."
- **Tipo**: Text
- **Modo**: Solo lectura

---

## Resumen de Reorganización
- Campos reorganizados: 30 existentes + 9 propuestos.
- Enfoque en flujo operativo: clasificación → activo → asignación → recursos → planificación → ejecución.
- Todo en una sola vista de formulario para eficiencia.

*Documento reorganizado para Proyecto PATCO - Odoo 18 Community Edition*