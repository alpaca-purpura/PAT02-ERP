Plan Funcional para la Digitalización de Operaciones de Mantenimiento HORECA para la Empresa PATCO con Odoo 18 Community
# Introducción
## Objetivo
Este documento presenta un plan funcional exhaustivo y detallado, diseñado para servir como un anteproyecto estratégico para la implementación del marco operativo PATCO dentro del sistema de planificación de recursos empresariales (ERP) Odoo 18 Community Edition. El objetivo principal es traducir un modelo de negocio de servicios de mantenimiento de activos robusto y bien definido, especializado en el sector HORECA (Hoteles, Restaurantes y Cafeterías), en un ecosistema digital cohesivo, automatizado y altamente eficiente.
## Alcance
- El informe abarca el ciclo de vida operativo completo, desde la configuración de los datos maestros hasta la generación de informes de indicadores clave de rendimiento (KPI) para la mejora continua.
- El análisis y las recomendaciones se centran exclusivamente en las funcionalidades disponibles en la versión gratuita de Odoo 18 Community, proponiendo soluciones prácticas y estables a través de módulos de la Odoo Community Association (OCA) y expansión de los mismos, buscando minimizar los desarrollos propios pero hacerlos si es necesario.
- Se detallarán los procesos de negocio, las configuraciones de los módulos, los flujos de trabajo interdepartamentales y los puntos de automatización críticos para lograr una digitalización máxima.
---
## Resumen funcional
---
### MACRO-PROCESO 1: Comercial, Contratos y Onboarding
Módulo(s) Central(es) de Odoo: Contactos, Ventas, Acuerdos (OCA), Empleados y Mantenimiento (para el modelo de Activos).
Área Funcional Clave: Gestión de Clientes, Creación de Acuerdos (Contratos y Servicios Puntuales), Habilidades de Técnicos y Registro de Activos de Cliente.
Notas: La gestión de contratos recurrentes ("Pólizas") se realiza a través del módulo agreement de la OCA, que proporciona un objeto de negocio específico para este fin, reemplazando el uso del módulo de Proyectos. El onboarding de activos utiliza el modelo de Equipos del módulo de  Mantenimiento.   
---
### MACRO-PROCESO 2: Operaciones de Servicio
- Módulo(s) Central(es) de Odoo: Mesa de Ayuda (Helpdesk), Servicios de Campo (Field Service), Empleados, Inventario.
- Área Funcional Clave: Creación y clasificación de Tickets, conversión a Órdenes de Servicio de Campo (fsm.order), asignación asistida por el sistema basada en habilidades y gestión de stock en vehículos.
- Notas: El flujo operativo principal es Mesa de Ayuda -> Servicios de Campo. La gestión de inventario se extiende para incluir ubicaciones específicas para cada furgoneta de técnico.
---
### MACRO-PROCESO 3: Ejecución en Campo
Módulo(s) Central(es) de Odoo: Servicios de Campo (Field Service), módulos personalizados desarrollados para hojas de trabajo digitales.
Área Funcional Clave: Actualización de estado móvil, consumo de repuestos, registro de tiempo, cumplimentación de hojas de trabajo digitales y captura de firma del cliente.
Notas: La interfaz principal del técnico en campo es la interfaz web responsiva de Odoo Community en un dispositivo móvil (tablet o smartphone). Se elimina la dependencia de integraciones externas, centralizando toda la operación en Odoo Community con módulos OCA y desarrollos personalizados cuando sea necesario. 
---
### MACRO-PROCESO 4: Cierre, Facturación y Cobranza
- Módulo(s) Central(es) de Odoo: Servicios de Campo (Field Service), Contabilidad, Automatización.
- Área Funcional Clave: Conformidad digital del cliente, facturación precisa basada en datos de la OT, registro de pagos y seguimiento de cuentas por cobrar.
- Notas: La facturación se dispara desde la Orden de Servicio de Campo y se gestiona en Contabilidad. El proceso se fortalece con la evidencia de la hoja de trabajo firmada digitalmente.
---
# Tipos de Usuario y Permisos
---
## Administrador del Sistema (Grupo: PATCO Administrador)
- Este es el rol con el nivel más alto de acceso, responsable de la configuración y mantenimiento del ERP.
- Descripción del Rol: Superusuario con control total sobre el sistema. Generalmente asignado al Gerente General y al implementador de Odoo.
- Permisos Clave:
* Acceso Total (CRUD): Puede Crear, Leer, Modificar y Eliminar registros en todos los módulos sin excepción.
* Configuración del Sistema: Único rol que puede modificar configuraciones críticas, como crear nuevos "Tipos de Acuerdo" (agreement.type) y los modelos de la matriz PATCO (patco.service.nature, etc.).
* Gestión de Módulos Ocultos: Aunque módulos como Mantenimiento estén ocultos para los roles operativos, el Administrador retiene acceso total para configurar sus modelos base (ej. Categorías de Equipos).
---
## Gerente / Líder de Servicio (Grupo: PATCO Líder Técnico)
- Este rol supervisa las operaciones diarias, desde la recepción del ticket hasta el cierre de la orden de servicio en campo.
- Descripción del Rol: Responsable de la coordinación de servicios, la planificación, el despacho de técnicos y el análisis de KPIs.
- Permisos Clave:
* Acuerdos (Contratos): Acceso completo para crear, ver y modificar todos los acuerdos (agreement.agreement).
* Mesa de Ayuda (Helpdesk): Acceso completo para recibir, clasificar y escalar todas las solicitudes de servicio (Tickets - helpdesk.ticket).
* Servicios de Campo (Field Service): Acceso completo para crear, asignar y supervisar todas las Órdenes de Servicio de Campo (fsm.order). Esta es su herramienta principal de despacho.
* Activos de Cliente: Acceso completo para crear y gestionar el registro maestro de activos de los clientes (maintenance.equipment).
* Mantenimiento: Sin acceso a la aplicación. El menú de Mantenimiento estará oculto para este rol, ya que toda la gestión de OTs de clientes se centraliza en Servicios de Campo.
* Informes: Acceso completo a los informes de Mesa de Ayuda, Servicios de Campo y Acuerdos.
---
## Técnico de Campo (Grupo: PATCO Técnico)
- Este es el rol para el personal que ejecuta los servicios en las instalaciones del cliente. Su acceso está enfocado únicamente en las tareas que se le han despachado.
- Descripción del Rol: Ejecuta las órdenes de servicio asignadas, registra su progreso, consume repuestos y documenta la finalización del servicio a través de la interfaz móvil de Odoo.
- Permisos Clave:
* Acuerdos (Contratos): Acceso de solo lectura a los acuerdos (agreement.agreement) a los que ha sido asignado para poder consultar las condiciones del servicio.
* Órdenes de Servicio de Campo (fsm.order): Solo puede ver y modificar las órdenes que tiene asignadas a él mismo.
* Activos de Cliente (maintenance.equipment): Puede crear nuevos activos (durante el onboarding puntual) y ver/modificar los activos relacionados con sus órdenes de servicio asignadas.
* Inventario: Puede ver el stock de su propia ubicación/furgoneta (stock.location) y registrar el consumo de repuestos.
* Mesa de Ayuda (Helpdesk): Sin acceso. El técnico no gestiona los tickets iniciales, solo las órdenes de servicio que se le despachan.
* Mantenimiento: Sin acceso a la aplicación. El menú de Mantenimiento estará oculto para este rol.
# Configuración Inicial
---
Construyendo el Gemelo Digital de su Negocio. Antes de que los flujos de trabajo diarios puedan ejecutarse con eficiencia, es imperativo establecer una configuración base sólida en Odoo Community 18. Esta fase consiste en modelar digitalmente los componentes centrales de la operación: los clientes, los activos que se atienden, los técnicos que realizan el trabajo y los servicios que se ofrecen.
---
## Cliente: Grupos y Ubicaciones de Servicio
- Necesidad del Negocio: Los clientes en el sector HORECA a menudo son parte de entidades corporativas más grandes con múltiples ubicaciones físicas. Es crucial que el sistema pueda manejar esta estructura jerárquica para despachar servicios a una dirección y facturar a otra.
- Modelo de Odoo: res.partner (Contactos).
- Implementación: Se utilizarán las relaciones padre-hijo nativas del modelo.
* Entidad Principal: La empresa matriz (ej. "Cadena Hotelera Sol S.A.") se crea como un contacto principal de tipo "Empresa". Contiene la información fiscal y de facturación.
* Ubicaciones de Servicio: Cada sede física (ej. "Hotel Sol Centro") se crea como un contacto adicional, vinculado a la empresa matriz a través del campo "Empresa". A estas ubicaciones se les asignará el tipo de dirección "Entrega" para su uso en órdenes de servicio.
- Beneficio Funcional: Al crear una fsm.order, se puede seleccionar la "Ubicación de Servicio" como dirección de entrega y la "Entidad Principal" como dirección de facturación, automatizando el despacho y la contabilidad.
- Datos Maestros a Cargar: Base de datos de clientes actuales, diferenciando entre sedes corporativas y ubicaciones de servicio.
---
## Catálogo de Servicios
- Necesidad del Negocio: Contar con un listado estandarizado de servicios y productos para generar cotizaciones y facturas de manera consistente.
- Modelo de Odoo: product.product (Productos).
- Implementación: Se crearán registros de productos con diferentes configuraciones.
* Productos de tipo "Servicio":
** Servicio Correctivo H/H: Para facturar reparaciones puntuales por hora.
** Plan de Mantenimiento Fijo: Producto con precio anual cuya venta dispara la creación de un Acuerdo de Servicio.
** Instalación de Equipo Nuevo: Para proyectos de instalación.
* Productos de tipo "Almacenable":
** Venta de Repuesto: Para gestionar el stock y la venta de piezas.
Datos Maestros a Cargar: Listado de todos los servicios ofrecidos y repuestos comunes con sus precios de venta.
---
## Matriz de Competencias de Técnicos
- Necesidad del Negocio: Mapear los requisitos de un servicio con las habilidades de cada técnico para realizar asignaciones eficientes y asistidas por el sistema.
- Modelos de Odoo: hr.employee, hr.skill.type, hr.skill, hr.skill.level.
- Proceso de Configuración:
* Crear Tipos de Habilidad: Corresponden a las grandes áreas de especialización (ej. COC - Cocina).
* Crear Habilidades Específicas: Son las sub-áreas dentro de cada tipo (ej. COC-CAL).
* Definir Niveles de Competencia: Corresponden a los niveles de dominio (N1, N2, N3).
* Asignar Habilidades a los Empleados: En la ficha de cada técnico (hr.employee), se le asigna cada habilidad que posee junto con su nivel de competencia.
- Beneficio Funcional: El módulo fieldservice_skill añade un campo en la fsm.order para seleccionar las habilidades requeridas. Al asignar un técnico, el sistema puede filtrar y mostrar solo a aquellos que cumplen con los requisitos.
- Catálogo de Competencias a Precargar (Catalogo de Competencias):
        - **Tipos de Habilidad y Habilidades Específicas**:
            - **COC - Cocina y Procesamiento**: `COC-CAL`, `COC-PRE`, `COC-LAV`.
            - **REF - Refrigeración y Climatización**: `REF-COM`, `AC`.
            - **LAV - Lavandería Industrial**: `LAV-LAV`, `LAV-SEC`, `LAV-PLA`.
            - **ELEC - Eléctrico**: `ELEC-BT` (Baja Tensión), `ELEC-GEN` (Generadores).
            - **FONT - Fontanería**: `FONT-AGUA`, `FONT-GAS`.
        - **Niveles de Competencia (Aplicables a todos los tipos de habilidad)**:
            - `N1 - Básico`
            - `N2 - Intermedio`
            - `N3 - Avanzado / Especialista`
---
## Registro Maestro de Activos del Cliente
- Necesidad del Negocio: Cada equipo propiedad de un cliente debe ser identificado de forma única en el sistema para poder rastrear su historial de servicio completo y tener toda su información relevante accesible al instante.
- Modelo de Odoo: maintenance.equipment (Equipos de Mantenimiento).
- Módulo OCA Requerido: maintenance_equipment_category_hierarchy.
- Implementación: Aunque el menú de la aplicación de Mantenimiento estará oculto, su modelo de datos es el pilar del "gemelo digital".
* Campos Clave a Rellenar:
** Nombre del Equipo: Descriptor claro (ej. "Freidora Frymaster - Cocina Principal").
** Categoría de Equipo: Estructura jerárquica para agrupar equipos.
** Propietario: (vínculo al res.partner de la Ubicación de Servicio)
** Número de Serie: Identificador único del fabricante, crítico para la trazabilidad.
*  Generación de Etiquetas QR: Se configurará un informe QWeb para el modelo maintenance.equipment. Este informe imprimirá una etiqueta con un código QR que contiene la URL del portal del equipo. Al escanearlo, el técnico accederá instantáneamente a la ficha completa del activo en su dispositivo móvil.   
- Datos Maestros a Cargar (Categorización Jerárquica): Se utilizará el módulo OCA para crear una estructura anidada. La categorización detallada a precargar es la siguiente:
- **Cocina y Procesamiento de Alimentos (COC)**
    - **Equipos de Cocción**
        - Hornos: de Convección, Combinados (Vapor y Convección), de Pizza, Regeneradores, Tandoor.
        - Estufas y Planchas: Cocinas Industriales (a gas/eléctricas), Planchas, Parrillas, Fry-tops, Barbacoas de piedra volcánica.
        - Freidoras: De alto rendimiento, a presión, de sobremesa.
        - Elementos Especializados: Salamandras, Gratinadores, Roners (Cocción a baja temperatura), Marmitas, Sartenes Basculantes.
    - **Equipos de Preparación**
        - Procesamiento Mecánico: Procesadores de alimentos, Cutters, Cortadoras de hortalizas, Peladoras de patatas.
        - Mezclado y Amasado: Batidoras-amasadoras planetarias, Batidoras de brazo, Amasadoras de espiral.
        - Corte: Cortadoras de fiambres, Sierras de huesos.
        - Conservación: Máquinas de envasado al vacío.
    - **Equipos de Lavado de Vajilla (COC-LAV)**
        - Lavavajillas de Cúpula
        - Lavavajillas de Arrastre o de Túnel
        - Lava-utensilios o Perolas
    - **Sistemas de Ventilación y Extracción**
        - Campanas Extractoras
        - Sistemas de Aporte de Aire
        - Sistemas de Extinción de Incendios para Cocinas
- **Refrigeración y Climatización (REF/AC)**
    - **Refrigeración Comercial**
        - Almacenamiento Vertical: Armarios frigoríficos (refrigeración/congelación), Congeladores verticales.
        - Almacenamiento Horizontal: Arcones congeladores, Mesas frías (de preparación), Botelleros.
        - Exhibición: Vitrinas refrigeradas (pasteleras, de tapas, murales).
        - Procesos Fríos: Abatidores de temperatura, Cámaras frigoríficas (de paneles), Fabricadores de hielo.
    - **Climatización (HVAC)**
        - Unidades de Aire Acondicionado tipo Split y Multi-Split
        - Sistemas de conductos (centralizados)
        - Unidades Manejadoras de Aire (UMAs)
- **Lavandería Industrial (LAV)**
    - **Equipos de Lavado**
        - Lavadoras Industriales de carga frontal (alta, media y baja velocidad)
        - Lavadoras con barrera sanitaria
    - **Equipos de Secado**
        - Secadoras Industriales rotativas
    - **Equipos de Planchado y Acabado**
        - Calandras (Planchadoras de rodillo)
        - Prensas y Mesas de planchado
- **Equipos de Bar y Cafetería**
    - Máquinas de Café Espresso
    - Molinillos de Café
    - Licuadoras y Batidoras de vaso
    - Exprimidores de Cítricos
- **Sistemas Eléctricos y Fontanería (ELEC/FONT)**
    - **Sistemas Eléctricos**
        - Grupos Electrógenos (Generadores)
        - Sistemas de Alimentación Ininterrumpida (SAI/UPS)
    - **Sistemas de Agua y Fontanería**
        - Sistemas de Bombeo y Grupos de Presión
        - Calderas y Termotanques industriales
----
## Plantillas de Checklist y Base de Conocimiento por Categoría
Para estandarizar los procedimientos en campo y empoderar a los técnicos con información crítica, es necesario centralizar la gestión de checklists y documentación técnica. La solución consiste en vincular esta información a la **Categoría del Equipo**, asegurando que cada activo herede automáticamente los procedimientos y manuales correctos.

### 1. Gestión de Checklists por Categoría de Equipo

- **Necesidad del Negocio**: Disponer de plantillas de checklists estandarizadas (una para la entrada/diagnóstico y otra para la salida/verificación) para cada tipo de equipo. El técnico debe poder consultar estos checklists desde la orden de servicio, pero no se requiere un seguimiento punto por punto digitalmente; solo el acceso al texto del procedimiento.

- **Modelos de Odoo y Campos a Añadir**:
    * **`maintenance.equipment.category` (Categoría de Equipo)**: Se añadirán dos nuevos campos de tipo **HTML**.
        * `x_entry_checklist_template`: Para almacenar el texto enriquecido de la plantilla del checklist de entrada.
        * `x_exit_checklist_template`: Para almacenar la plantilla del checklist de salida.
    * **`fsm.order` (Orden de Servicio de Campo)**: Se añadirán dos campos de tipo **HTML** de solo lectura.
        * `x_entry_checklist`: Mostrará el checklist de entrada relevante.
        * `x_exit_checklist`: Mostrará el checklist de salida relevante.

- **Implementación y Flujo de Trabajo**:
    1.  **Configuración (Administrador)**: El Administrador del Sistema o el Líder de Servicio irá a la configuración de las Categorías de Equipos. En la ficha de cada categoría (ej. "Freidoras de alto rendimiento"), pegará el texto con los puntos a verificar en los campos "Plantilla Checklist de Entrada" y "Plantilla Checklist de Salida".
    2.  **Herencia Automática**: Se configurará que los campos `x_entry_checklist` y `x_exit_checklist` en la `fsm.order` sean campos **relacionados (related fields)** que apunten a las plantillas de la categoría del activo seleccionado en la orden (`fsm.order.equipment_id.category_id.x_entry_checklist_template`).
    3.  **Ejecución (Técnico)**: Cuando el técnico abra una Orden de Servicio de Campo en su dispositivo móvil, verá dos nuevas pestañas o secciones: "Checklist de Entrada" y "Checklist de Salida". Estas mostrarán el texto de los procedimientos que debe seguir, sirviendo como su guía operativa estándar.

- **Beneficio Funcional**: Se estandarizan los procedimientos sin añadir complejidad operativa. El técnico siempre tendrá la guía correcta para el equipo correcto, mejorando la calidad del diagnóstico y la verificación final. La gestión es centralizada y muy sencilla.

### 2. Base de Conocimiento por Categoría de Equipo

- **Necesidad del Negocio**: Crear una biblioteca central de recursos técnicos (manuales en PDF, diagramas eléctricos, guías de despiece, etc.) y asegurar que los documentos relevantes para un equipo específico sean fácilmente accesibles para el técnico en campo.

- **Modelos de Odoo y Campos a Añadir**:
    * **`maintenance.equipment.category` (Categoría de Equipo)**: Se utilizará la funcionalidad nativa de **Adjuntos** para cargar todos los documentos relevantes a esa categoría.
    * **`maintenance.equipment` (Activo de Cliente)**: Se añadirá un campo **relacionado (related field)** de solo lectura que muestre los adjuntos de su categoría.
        * `x_knowledge_base_files`: Campo que mostrará la lista de archivos adjuntos de la categoría del equipo.

- **Implementación y Flujo de Trabajo**:
    1.  **Configuración (Administrador)**: En la ficha de cada Categoría de Equipo, el administrador usará el botón del "clip" (Adjuntos) para cargar todos los manuales, imágenes y documentos relevantes para ese tipo de equipo. Por ejemplo, en "Hornos Combinados", subirá el manual de instalación, el manual de servicio y el diagrama eléctrico del modelo más común.
    2.  **Acceso en Campo (Técnico)**: Cuando el técnico esté en una `fsm.order`, podrá hacer clic en el **Activo de Cliente** asociado. En la ficha del activo, habrá una nueva pestaña o sección llamada "Base de Conocimiento" o "Documentación Técnica". Gracias al campo relacionado, esta sección mostrará **automáticamente** la lista de todos los archivos adjuntos a la categoría de ese equipo, sin que el técnico tenga que buscar en otro lugar. Podrá abrir o descargar los PDFs directamente en su móvil.

- **Beneficio Funcional**: Se elimina el tiempo perdido buscando documentación. El técnico tiene acceso contextual e inmediato a la información técnica precisa, aumentando la tasa de resolución en la primera visita y reduciendo errores.

# Comercial, Contratos y Onboarding de Clientes
---
Esta sección detalla el ciclo de vida desde la captación de un cliente hasta la gestión de sus contratos y el registro inicial de sus activos, utilizando una arquitectura estándar y escalable.
## Formalización del Acuerdo Comercial
- Necesidad del Negocio: Iniciar el proceso con un registro oficial de los servicios a prestar, ya sea para un trabajo puntual o un contrato de mantenimiento ("Póliza").
- Modelos de Odoo: res.partner, sale.order, sale.order.line.
- Flujo de Trabajo:
* Creación del Cliente y Cotización: Se crea la ficha del cliente en Contactos (res.partner). Desde Ventas, se genera una "Cotización" (sale.order en estado 'borrador') utilizando los productos del catálogo.
* Aceptación y Orden de Venta: La cotización se envía al cliente. Al confirmarse, pasa a ser una Orden de Venta (sale.order en estado 'venta'), que es el disparador oficial del proceso.
## Gestión de Acuerdos de Servicio (Contratos y Servicios Puntuales)
- Necesidad del Negocio: Se requiere una entidad central para gestionar los acuerdos comerciales a largo plazo (contratos). Esta entidad debe contener las condiciones, vigencia y servir como un contenedor para el historial de servicios, siendo conceptualmente distinta a un "proyecto de trabajo".
- Solución Propuesta (Pivote Arquitectónico): Se utilizará el módulo agreement de la OCA como herramienta central, reemplazando el módulo de Proyectos para este fin. Un "Acuerdo" (agreement.agreement) representará una "Póliza" o contrato.
- Modelos de Odoo (OCA): agreement.agreement, agreement.type.
- Módulos OCA Requeridos: agreement, agreement_sale.   
- Configuración y Campos del Acuerdo:
* Tipos de Acuerdo (agreement.type): Se crean plantillas para los diferentes planes comerciales (Mantenimiento Preventivo, Bolsa de Horas, Todo Incluido). Estos pueden predefinir cláusulas o condiciones.
* Campos Nativos del Acuerdo (agreement.agreement):
** name: Título del acuerdo.
** partner_id: Cliente con el que se firma el acuerdo.
** start_date / end_date: Fechas de inicio y fin de vigencia.
** state: Ciclo de vida nativo (Borrador, Activo, Vencido, Cancelado).
- El Acuerdo como Acuerdo Marco y Contenedor de Historial:
* Creación: Tras confirmar la Orden de Venta, el módulo agreement_sale crea automáticamente un Acuerdo en estado "Borrador", vinculado a la SO.
* Función: El Acuerdo funciona como el "paraguas" comercial que agrupa todas las fsm.order ejecutadas para ese cliente. Proporciona una trazabilidad completa desde la venta hasta el servicio y facilita los informes de rentabilidad por contrato.
## Onboarding Digital de Activos
- Necesidad del Negocio: Realizar un inventario de los equipos del cliente y crear sus registros digitales en Odoo ("gemelo digital"), que es la base para toda la trazabilidad del servicio.
- Modelos de Odoo: maintenance.equipment, project.project (para la tarea de onboarding), project.task.
- Módulo OCA Opcional: project_template.
- Escenario 1: Onboarding Completo para Nuevos Contratos: Al activar un Acuerdo, se puede crear un Proyecto puntual y estandarizado (usando project_template) con una tarea específica llamada "Levantamiento Inicial de Activos". Esta tarea se asigna a un técnico para realizar el inventario. Importante: Este proyecto es solo para la gestión de esta tarea inicial, no para el contrato en sí.

- Escenario 2: Onboarding Puntual: Para un servicio a un equipo no registrado, el onboarding es el primer paso dentro de la misma fsm.order. El técnico crea el registro del activo antes de iniciar el trabajo.
- Ejecución en Campo: Creación del "Gemelo Digital": En ambos escenarios, el técnico en sitio sigue estos pasos para cada equipo:
* Crea un nuevo registro de Activo de Cliente (maintenance.equipment).
* Rellena los campos críticos: Categoría de Equipo, Modelo, y el N.º de serie.
* Vincula el activo a la Ubicación de Servicio del cliente.
* Toma fotos del equipo y su placa y las adjunta directamente al chatter del registro.
---
# Operaciones: Gestión del Servicio de Campo
---
Esta sección aborda el núcleo de las operaciones diarias: el ciclo de recibir una solicitud, clasificarla y asignar al técnico más adecuado.
## El Flujo: Del Ticket de Soporte a la Orden de Campo
- Necesidad del Negocio: Cada solicitud de servicio debe ser capturada como un Ticket único y rastreable, que luego puede convertirse en una Orden de Servicio en Campo para despachar a un técnico.
- Modelos de Odoo: helpdesk.ticket, fsm.order.
- Flujo de Trabajo:
---
* 1. Creación del Ticket (helpdesk.ticket): El Coordinador de Servicios crea un nuevo Ticket. Campos esenciales:
**Título: Un resumen del problema.
** Cliente y Ubicación: Se selecciona la empresa y la sede del servicio.
** Activo de Cliente (maintenance.equipment): Se selecciona el equipo afectado. Este campo se configurará como obligatorio.
---
* 2. Clasificación Operativa en el Ticket: El coordinador aplica la clasificación utilizando los campos de la matriz PATCO. Los datos a precargar en el sistema para esta matriz son:
- **Naturaleza del Servicio** (`patco.service.nature`):
    - `M1-Correctivo`
    - `M2-Preventivo`
    - `M3-Instalación`
    - `M4-Inspección`
- **Área del Servicio** (`patco.service.area`):
    - `COC-CAL` (Cocina - Calor)
    - `COC-PRE` (Cocina - Preparación)
    - `COC-LAV` (Cocina - Lavado)
    - `REF-COM` (Refrigeración Comercial)
    - `AC` (Aire Acondicionado)
    - `LAV` (Lavandería Industrial)
    - `ELEC` (Eléctrico)
    - `FONT` (Fontanería)
- **Complejidad del Servicio** (`patco.service.complexity`):
    - `N1-Básico`
    - `N2-Intermedio`
    - `N3-Avanzado`
    - `N4-Crítico`
---
*  3.  Despacho (Conversión a Orden de Servicio)* Si el Ticket requiere una visita, el coordinador lo convierte con un clic en una **Orden de Servicio de Campo (`fsm.order`)**. La `fsm.order` hereda toda la información y se convierte en la OT oficial para el técnico.
---
## Asignación de Técnicos y Verificación de Repuestos
- Necesidad del Negocio: Asignar al técnico más competente y asegurar la disponibilidad de repuestos para maximizar la tasa de resolución en la primera visita.
- Modelos de Odoo: fsm.order, hr.employee, stock.location, stock.picking, stock.rule.
- Flujo de Trabajo:
    1.  Asignación Basada en Competencias: El coordinador, desde la fsm.order, utiliza el filtro de habilidades (provisto por fieldservice_skill) para asignar al técnico cualificado.   
    2.  Gestión de Stock:
* Arquitectura de Inventario: Dentro del Almacén principal (WH), se crea una ubicación de tipo "Vista" llamada "Furgonetas" (WH/Stock/Vans). Dentro de esta, se crea una ubicación interna (stock.location) para cada vehículo, ej. WH/Stock/Vans/VAN-001.   
* Reabastecimiento: Las furgonetas se reabastecen mediante Transferencias Internas (stock.picking) desde WH/Stock a WH/Stock/Vans/VAN-001. Para repuestos de alta rotación, se pueden configurar    
* Reglas de Reabastecimiento (stock.rule) para automatizar la generación de estas transferencias.   
* Verificación de Repuestos: Al añadir productos a la fsm.order, el sistema mostrará la cantidad disponible en la ubicación de la furgoneta del técnico asignado.
# Ejecución en Campo y Reporte Digital
Esta sección se centra en la perspectiva del técnico en el terreno. Detalla cómo el sistema Odoo, a través de un dispositivo móvil, le proporciona las herramientas necesarias para ejecutar el trabajo de manera eficiente, documentar sus acciones en tiempo real y, de forma crucial, integrar el informe de servicio detallado generado por el agente de IA externo.
## Evolución del Flujo Operativo en Campo: El Agente IA 2.0
Se presenta un flujo de trabajo aumentado que integra de manera nativa la ejecución de procedimientos, la consulta de conocimiento en tiempo real y la captura de datos estructurados y no estructurados.
- Mapeo Funcional Detallado del Ciclo de Servicio Aumentado. El nuevo ciclo operativo se orquesta a través de una comunicación fluida y bidireccional entre Odoo, el sistema de registro y gobernanza, y el Agente IA en Telegram, la interfaz de ejecución en campo.
---
* 1. El Disparador (Desde Odoo)
El proceso se inicia de forma automática, garantizando la consistencia y eliminando la intervención manual del coordinador. 
Evento: Asignación de una Orden de Servicio de Campo (fsm.order) a un técnico específico en Odoo. 
Acción: Una Acción Automatizada de Odoo se dispara instantáneamente, ejecutando un webhook que realiza una llamada a un endpoint seguro del Agente IA. 
Payload de Datos (JSON): La llamada transporta un payload de datos rico en contexto, que arma al Agente IA con toda la información necesaria para la misión.  La estructura crítica del payload es la siguiente:
JSON
{
  "fsm_order_id": 12345,
  "customer_name": "Hotel Sol Centro",
  "technician_telegram_id": "567890123",
  "assets": [
    {
      "asset_id": 789,
      "asset_name": "Freidora Frymaster - Cocina Principal",
      "entry_checklist_template_id": 15,
      "exit_checklist_template_id": 16,
      "knowledge_base_urls": [
        "https://odoo.patco.com/web/content/ir.attachment/101/datas/manual_frymaster.pdf",
        "https://odoo.patco.com/web/content/ir.attachment/102/datas/diagrama_electrico.png"
      ]
    }
  ]
}
---
2. La Interacción (En Telegram)
El técnico recibe la notificación en Telegram y comienza una conversación guiada, inteligente y flexible. 
Ejecución Guiada de Checklists: El Agente IA inicia la conversación presentando la orden de servicio y, tras la confirmación del técnico, comienza a guiarlo a través de los pasos del checklist de entrada recuperados desde Odoo. La interacción es dinámica y se adapta al tipo de respuesta (response_type) de cada paso.  Por ejemplo:
IA: "Paso 1/10 (Obligatorio): Verificar desconexión eléctrica del equipo. Por favor, confirme (Sí/No)." 
IA: "Paso 2/10: Tomar una foto de la placa de número de serie." (El IA esperará una imagen como respuesta). 
Soporte Inteligente con RAG (Q&A): En cualquier momento, el técnico puede interrumpir el flujo para realizar consultas técnicas. El Agente IA utiliza la capacidad RAG sobre los documentos provistos en el payload inicial. 
Técnico: "¿Cuál es el torque de apriete para los pernos de la carcasa principal en este modelo?" 
IA: "Consultando la base de conocimiento... Según el documento 'manual_frymaster.pdf', página 45, el torque recomendado es de 85 Nm. ¿Necesitas que te muestre esa sección del manual?" 
Esta capacidad transforma al agente en un asistente experto en tiempo real. 
Captura de Datos No Estructurados: Manteniendo la flexibilidad, el técnico puede seguir enviando notas de voz, fotos adicionales y descripciones textuales sobre el trabajo realizado, capturando matices que no están cubiertos por el checklist.
---
3. El Cierre del Ciclo (IA -> Odoo)
Una vez finalizado el trabajo y completado el checklist de salida, el Agente IA sincroniza toda la información con Odoo para que actúe como la fuente única de la verdad. 
Acción: El agente realiza una llamada a la API REST de Odoo. 
Sincronización de Datos:


Enlace al Informe: El enlace al Google Doc del informe final se guarda en un campo URL personalizado en la fsm.order. 
Almacenamiento de Datos Estructurados: Por cada paso del checklist, se crea un registro en un nuevo modelo (patco.fsm.checklist.result) vinculado a la fsm.order. Este registro almacena la descripción del paso, la respuesta del técnico, la marca de tiempo y un enlace a la evidencia (como una foto). Esta estructura es fundamental para la auditoría y el análisis posterior. 
Adjuntar Datos Brutos: Todas las fotos y archivos de audio originales se adjuntan al chatter de la fsm.order, proporcionando un registro inalterado y completo.
---
## Arquitectura Técnica Recomendada del Agente IA
La implementación se apoya en una arquitectura moderna, pragmática y rentable. 
Orquestador (LangGraph): Para gestionar una conversación compleja y con estado como la ejecución de un checklist, se recomienda LangGraph, que permite definir un flujo con ciclos y lógica condicional. Los nodos del grafo podrían incluir: presentar_paso, esperar_respuesta_tecnico, validar_respuesta, consulta_rag, y generar_informe_final. 
Base de Conocimiento (pgvector en Odoo): La solución más eficiente es utilizar la propia base de datos PostgreSQL de Odoo con la extensión pgvector, eliminando la necesidad de mantener una base de datos vectorial separada. 
Pipeline de Indexación: Un proceso automatizado en Odoo que, al adjuntar un documento a un equipo, dispara un microservicio que lo descarga, divide en fragmentos, genera embeddings con una API como la de Gemini y almacena los vectores en la tabla de pgvector. 
Lógica de Recuperación (Retrieval): Cuando un técnico pregunta, el Agente IA genera un embedding de la pregunta, busca por similitud en pgvector (filtrando solo los documentos relevantes para la orden actual), recupera los fragmentos de texto más relevantes y los inyecta en un prompt de un LLM (Gemini) para sintetizar la respuesta final. 
---
Esta sección se centra en la perspectiva del técnico en el terreno. Detalla cómo el sistema Odoo, a través de un dispositivo móvil, le proporciona las herramientas necesarias para ejecutar el trabajo de manera eficiente, documentar sus acciones en tiempo real y, de forma crucial, integrar el informe de servicio detallado generado por el agente de IA externo.
## El Flujo de Trabajo Móvil del Técnico
- **Necesidad del Negocio**: Los técnicos necesitan acceso móvil a sus Órdenes de Servicio de Campo asignadas, información del equipo y una forma sencilla de registrar el progreso, las piezas utilizadas y el tiempo invertido.
- **Mapeo Funcional en Odoo**: Odoo 18 Community cuenta con una interfaz web totalmente responsive, que funciona de manera fluida en navegadores de tabletas y smartphones. El técnico utilizará una combinación de dos herramientas en su móvil. Odoo será su sistema principal para gestionar las acciones oficiales de la orden de servicio, como cambiar estados, consultar historiales, consumir repuestos y registrar tiempos. En paralelo, el Asistente IA en Telegram funcionará como su compañero digital, guiándolo en la recopilación de datos en tiempo real (fotos, notas de voz, checklists) para automatizar la creación del informe final.
    * **Acceso y Punto de Partida**: El técnico inicia sesión en Odoo y accede directamente al tablero de **Servicio de Campo** . Su vista estará predeterminada para mostrar únicamente **"Mis Órdenes de Servicio"**. Al mismo tiempo, ya habrá recibido la notificación inicial de la asignación en Telegram por parte del Asistente IA.
    *  **Actualización de Estado en Tiempo Real**: Al llegar a las instalaciones del cliente, el técnico confirma el inicio del trabajo en Telegram, y en paralelo, abre la `fsm.order` correspondiente en Odoo para cambiar su etapa de "Programado" a "En Progreso" . Este cambio actualiza el estado oficial del servicio para el coordinador.
    *  **Consulta de Historial del Activo**: Desde la orden en Odoo, el técnico tiene un enlace directo a la ficha del **Activo del Cliente**. Allí puede consultar todo su historial de servicios: fallas anteriores, reparaciones y piezas cambiadas, lo que le proporciona un contexto valioso para el diagnóstico. También podrá solicitar este historial al Asistente IA vía Telegram.
    *  **Consumo de Repuestos (Flujo Simplificado)**: Directamente en una pestaña dentro de la `fsm.order` llamada "Productos" o "Materiales", el técnico añade los repuestos que ha utilizado de su furgoneta. Al hacerlo, el sistema descuenta automáticamente esas unidades del inventario de su ubicación ("Furgoneta - [Nombre Técnico]"), manteniendo el control de stock en tiempo real.
    * **Registro de Tiempos**: En la pestaña "Partes de Horas" (Timesheets) de la `fsm.order`, el técnico registra el tiempo total dedicado al trabajo al finalizar el servicio.
# El Asistente de Campo IA: Digitalización y Reporte en Tiempo Real
---
## Necesidad del Negocio
El técnico de campo necesita una herramienta que lo asista durante el servicio, no después. El objetivo es eliminar la carga administrativa de crear informes manuales, estandarizar la calidad de la documentación y capturar la información (fotos, notas, checklists) en tiempo real para evitar olvidos. El Agente IA debe actuar como un compañero digital que guía al técnico y automatiza la creación del informe final.
---
## Mapeo Funcional: El Flujo Odoo <> Telegram
La solución integra Odoo como el sistema de gestión central y Telegram como la interfaz de usuario simple y directa para el técnico en campo.
### 1. El Disparador (Desde Odoo)
- **Evento**: La asignación de una **Orden de Servicio de Campo (`fsm.order`)** a un técnico específico.
- **Acción**: Una **Acción Automatizada** (definida en el módulo `patco_core`) se dispara en Odoo. Esta acción realiza una llamada (webhook) a un endpoint del Agente IA.
- **Datos Enviados**: Se envía la información clave de la `fsm.order`: ID de la orden, datos del cliente, lista de activos a revisar (con sus categorías) y el **ID de Telegram del técnico** (un nuevo campo que se debe añadir en la ficha del empleado en Odoo).

### 2. La Interacción (En Telegram)
El técnico recibe un mensaje en Telegram y comienza el flujo de trabajo conversacional. Toda su interacción es a través del bot.
- **Paso 1: Inicio del Servicio**: El bot saluda al técnico y le presenta la `fsm.order`. Le pide que confirme el inicio del servicio.
- **Paso 2: Checklist de Entrada**: Por cada activo a revisar, el bot le entrega el checklist de entrada correspondiente a su categoría (ej. "Checklist de Entrada para Freidoras de Alto Rendimiento"). Estos checklists se configuran en Odoo.
- **Paso 3: Recopilación de Datos**: El técnico realiza el checklist y va enviando al bot la información en el formato que le sea más cómodo:
    - Fotos de los equipos.
    - Notas de voz explicando un hallazgo.
    - Texto con mediciones o comentarios.
- **Paso 4: Soporte Inteligente**: Durante el servicio, el técnico puede hacerle preguntas al bot como *"¿cuál es la presión de gas recomendada para este modelo?"* o *"muéstrame el último informe de este equipo"*. El Agente IA buscará en su base de conocimiento (manuales, historial) para responder.
- **Paso 5: Checklist de Salida**: Al finalizar el trabajo en un activo, el bot le entrega el checklist de salida para verificar que todo quedó operativo.
- **Paso 6: Generación del Borrador del Informe**: Una vez completado el servicio, el bot notifica al técnico: *"Estoy generando el borrador del informe. Te enviaré el enlace en un momento."*

### 3. El Cierre del Ciclo (Agente IA -> Odoo)
- **Creación del Informe**: El Agente IA (usando Gemini y LangGraph) procesa toda la conversación, transcribe los audios, analiza las imágenes y estructura la información según un formato predefinido. Crea un **Google Doc** con este informe.
- **Entrega al Técnico**: El bot envía un único mensaje final al técnico con el enlace al Google Doc, para que pueda revisarlo, hacer ajustes finales o simplemente validarlo.
- **Sincronización con Odoo**: De forma simultánea, el Agente IA hace una llamada a la API de Odoo para:
    1.  Guardar el enlace del Google Doc en un campo personalizado de tipo URL en la `fsm.order` llamado **"Enlace a Informe de Servicio (IA)"**.
    2.  (Opcional, pero recomendado) Adjuntar todas las fotos y audios originales al chatter de la `fsm.order` para tener un registro bruto y auditable.
---
## Arquitectura Recomendada (Enfoque MYPE)
Para implementar esto sin añadir una complejidad o costo excesivo:
- **Orquestador**: **LangGraph** es una excelente elección para manejar el flujo conversacional con estados (ej. "esperando fotos de entrada").
- **Inteligencia**: **Gemini API** para el procesamiento del lenguaje, análisis de imágenes y generación del texto del informe.
- **Base de Conocimiento (Vector DB)**: **PostgreSQL y la extensión `pgvector`**. Ya que Odoo usa PostgreSQL, se puede mantener la base de conocimiento (vectores de manuales e informes) en la misma base de datos, simplificando enormemente la infraestructura.
- **Interfaz**: **Telegram**, por su versatilidad y facilidad de uso.
# Cierre del Servicio y Conformidad del Cliente
---
## Necesidad del Negocio
El proceso de cierre tiene dos fases: primero, obtener una conformidad operativa del cliente en sitio al finalizar el trabajo, y segundo, gestionar un proceso administrativo formal que culmina con la recepción de una Orden de Compra del cliente antes de poder facturar.

## Mapeo Funcional: Flujo de Cierre en Dos Fases

### Fase 1: Cierre Operativo en Campo (Técnico)

1.  **Revisión y Presentación del Informe IA**:
    - Una vez finalizado el trabajo, el Asistente IA en Telegram genera el informe en **Google Doc** y envía el enlace al técnico.
    - El técnico lo revisa y se lo presenta al cliente en su dispositivo móvil como prueba transparente del servicio realizado.

2.  **Conformidad Verbal en Sitio**:
    - El cliente revisa el informe y el equipo, y da su **conformidad verbal** al técnico.
    - El técnico lo registra enviando un mensaje final al bot de Telegram: *"Trabajo finalizado. Cliente [Nombre del Contacto] da su conformidad verbal."*

3.  **Finalización de la Tarea en Odoo**:
    - La responsabilidad del técnico termina aquí. Su última acción en la aplicación de Odoo es mover la **Orden de Servicio de Campo (`fsm.order`)** a una nueva etapa: **"Trabajo Finalizado"**.
    - Este cambio de etapa notifica al coordinador que el trabajo en campo ha concluido y que puede iniciar el proceso administrativo de cierre.

### Fase 2: Cierre Administrativo (Coordinador)

El coordinador gestiona el resto del ciclo de vida de la `fsm.order` desde su tablero Kanban.

1.  **Envío de Informe y Solicitud de Conformidad Formal**:
    - El coordinador ve la orden en la etapa "Trabajo Finalizado".
    - Envía un correo electrónico formal al cliente, adjuntando el informe del servicio y solicitando la conformidad por escrito y el posterior envío de su Orden de Compra (OC).
    - Mueve la `fsm.order` a la etapa **"Informe Enviado"**.

2.  **Recepción de Conformidad y OC del Cliente**:
    - Cuando el cliente responde con la conformidad por correo y, posteriormente, envía su OC, el coordinador realiza dos acciones en la `fsm.order`:
        - **Adjunta los documentos**: Carga el PDF de la OC del cliente y el correo de conformidad en el chatter de la orden.
        - **Registra el N.º de OC**: Anota el número de la OC en un campo personalizado en la orden.
    - Mueve la `fsm.order` a la etapa final: **"Listo para Facturar"**.

---
# Facturación y Cobranza
---
Esta sección final describe los procesos de back-office que completan el ciclo de vida del servicio, desde la emisión de la factura hasta el registro de su pago.
## Facturación Basada en la Orden de Compra del Cliente
- Necesidad del Negocio: Un proceso de facturación controlado que se inicia solo después de recibir una OC formal del cliente y que refleja con precisión los materiales y horas consumidos.
- Modelos de Odoo: fsm.order, account.move (Factura).
- Disparador: Una Acción Automatizada se dispara cuando una fsm.order se mueve a la etapa "Listo para Facturar".
- Acción Automatizada: Creación del Borrador:
* La automatización crea un registro de "Factura de Cliente" (account.move) en estado "Borrador".
* La factura se puebla automáticamente con los datos de la fsm.order: los repuestos exactos consumidos y las horas exactas registradas.
* El número de OC del cliente se transfiere al campo "Referencia del Cliente".
- Proceso Manual de Emisión: El encargado de facturación revisa la factura borrador, adjunta los documentos de respaldo, la valida y la envía al cliente.
## Registro de Pagos y Control de Cuentas por Cobrar
- Necesidad del Negocio: Una vista simple de las facturas pendientes y una forma sencilla de registrar pagos, incluyendo parciales y detracciones.
- Modelos de Odoo: account.move, account.payment, account.journal.
- Configuración de Diarios de Pago: Se configuran "Diarios" (account.journal) de tipo "Banco" para cada cuenta bancaria (ej. "Banco Principal BCP", "Banco de la Nación - Detracciones").
- Vista de Pagos Pendientes: El encargado utiliza el filtro "No Pagadas" en la lista de facturas de cliente (Contabilidad > Clientes > Facturas).
- Registro del Pago: Al recibir un pago, se utiliza el botón "Registrar Pago" en la factura, seleccionando el diario y el importe correcto (total o parcial). Para las detracciones, se registra un segundo pago en la misma factura con el diario correspondiente.