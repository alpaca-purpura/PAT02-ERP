
Plan Funcional para la Digitalización de Operaciones de Mantenimiento HORECA con Odoo 18 Community


Introducción


Objetivo

Este documento presenta un plan funcional exhaustivo y detallado, diseñado para servir como un anteproyecto estratégico para la implementación del marco operativo PATCO dentro del sistema de planificación de recursos empresariales (ERP) Odoo 18 Community Edition. El objetivo principal es traducir un modelo de negocio de mantenimiento robusto y bien definido, especializado en el sector HORECA (Hoteles, Restaurantes y Cafeterías), en un ecosistema digital cohesivo, automatizado y altamente eficiente.

Alcance

El informe abarca el ciclo de vida operativo completo, desde la configuración fundamental de los datos maestros hasta la generación de informes de indicadores clave de rendimiento (KPI) para la mejora continua. El análisis y las recomendaciones se centran exclusivamente en las funcionalidades disponibles en la versión gratuita de Odoo 18 Community, proponiendo soluciones prácticas y estables para las brechas funcionales en comparación con la edición Enterprise. Se detallarán los procesos de negocio, las configuraciones de los módulos, los flujos de trabajo interdepartamentales y los puntos de automatización críticos para lograr una digitalización máxima.

Audiencia

Este plan está dirigido a propietarios de empresas, directores de operaciones y gerentes de servicio que buscan transformar su modelo operativo actual en una plataforma escalable, eficiente y basada en datos. Se asume un profundo conocimiento del negocio de mantenimiento, pero no se requiere experiencia previa como desarrollador de ERP.

Resultado Clave

El resultado final es un plan de implementación práctico que alinea directamente la lógica de negocio del framework PATCO con la estructura funcional de Odoo. Al seguir esta guía, la empresa podrá establecer una única fuente de verdad para todas sus actividades de mantenimiento, optimizar la asignación de recursos, mejorar la calidad del servicio y sentar las bases para un crecimiento estratégico basado en el análisis de datos operativos.

Tabla 1: Mapeo de Fases PATCO a Módulos de Odoo

Número de Fase
Nombre de la Fase
Módulo(s) Central(es) de Odoo
Área Funcional Clave
Notas / Solución Alternativa Requerida
FASE 1
Comercial y Onboarding
Contactos, CRM, Ventas, Empleados, Mantenimiento
Gestión de Clientes, Contratos, Habilidades de Técnicos, Registro de Activos
Se requiere una solución alternativa para contratos recurrentes ("Pólizas") en la edición Community.
FASE 2
Gestión de la Solicitud
Mantenimiento, Mesa de Ayuda (Helpdesk)
Creación y Clasificación de Órdenes de Trabajo (OT)
La clasificación se implementará mediante el sistema de etiquetas de Odoo.
FASE 3
Planificación y Despacho
Mantenimiento, Empleados, Inventario
Asignación basada en habilidades, Programación, Verificación de Repuestos
La asignación es un proceso manual guiado por el sistema, no una asignación automática.
FASE 4
Ejecución en Campo
Mantenimiento, Proyectos (para Tareas)
Actualización de estado móvil, Consumo de partes, Registro de tiempo, Integración de informe IA
Se requiere una personalización menor (campo URL) para el enlace del informe de la IA.
FASE 5
Cierre y Seguimiento
Mantenimiento, Facturación, Automatización
Facturación, Encuestas de Satisfacción, Análisis de KPI
Se requiere una solución alternativa para las encuestas CSAT (herramienta externa).


Sección 1: Configuración Fundacional - Construyendo el Gemelo Digital de su Negocio

Antes de que los flujos de trabajo diarios puedan ejecutarse con eficiencia, es imperativo establecer una configuración base sólida en Odoo. Esta fase inicial consiste en modelar digitalmente los componentes centrales de la operación: los clientes, los activos que se atienden, los técnicos que realizan el trabajo y los servicios que se ofrecen. Esta configuración, realizada una sola vez, es el cimiento sobre el cual se construirá todo el ecosistema digital.

1.1. Modelando el Ecosistema de Clientes: Grupos HORECA y Ubicaciones de Servicio

Necesidad del Negocio: Los clientes en el sector HORECA a menudo son parte de entidades corporativas más grandes (como una cadena hotelera) con múltiples ubicaciones físicas donde se presta el servicio. La facturación puede estar centralizada en la oficina corporativa, mientras que las órdenes de trabajo se generan para establecimientos específicos. Es crucial que el sistema pueda manejar esta estructura jerárquica para una gestión operativa y administrativa precisa.
Mapeo Funcional en Odoo: Esta estructura se implementará utilizando el modelo res.partner en el módulo nativo de Contactos.1 El modelo
res.partner de Odoo está diseñado para gestionar de forma unificada a cualquier entidad con la que la empresa se relacione, ya sean clientes, proveedores o empleados, lo que simplifica la gestión de datos.3
La configuración se realizará de la siguiente manera:
Creación de la Entidad Principal: La empresa matriz (ej. "Cadena Hotelera Sol S.A.") se creará como un registro principal de res.partner. Este registro contendrá la información fiscal y de facturación centralizada.
Creación de Ubicaciones de Servicio: Cada ubicación física (ej. "Hotel Sol Centro", "Hotel Sol Playa") se creará como un registro de contacto adicional. En el formulario de cada ubicación, se utilizará el campo Compañía para vincularlo al registro de la empresa matriz. Esto establece una relación padre-hijo nativa en Odoo.4
Tipificación de Direcciones: A cada ubicación de servicio se le asignará un tipo de dirección específico, como "Dirección de Entrega" o, preferiblemente, un tipo personalizado como "Ubicación de Servicio" para mayor claridad.
Esta relación padre-hijo no es meramente organizativa; es un motor funcional clave. Cuando se crea una Orden de Trabajo (OT) para el "Hotel Sol Centro" (el hijo), el sistema conoce de inmediato la dirección física precisa para el despacho del técnico. Sin embargo, al momento de generar la factura, el sistema puede configurarse para que esta se emita y envíe a la entidad matriz, "Cadena Hotelera Sol S.A.", automatizando y simplificando el proceso de cobro a clientes corporativos. Al estructurar los datos de esta manera desde el principio, se construye una base de datos potente para la inteligencia de negocio. Permite analizar ingresos, frecuencia de servicios y costos por ubicación individual, pero también agregar estos datos a nivel de la cuenta corporativa. Esta capacidad facilita una gestión estratégica de cuentas, permitiendo identificar qué clientes corporativos son más rentables o problemáticos y fundamentando con datos las negociaciones de futuros contratos de servicio.

1.2. Definiendo el Catálogo de Servicios: Configuración de Productos de Servicio

Necesidad del Negocio: La empresa ofrece una variedad de servicios con diferentes modelos de tarificación: mantenimiento correctivo por hora, planes de mantenimiento preventivo con tarifa fija, servicios de instalación, y la venta de contratos de servicio anuales ("Pólizas"). Cada uno de estos debe ser un elemento vendible dentro del ERP para poder generar cotizaciones, órdenes de venta y facturas de manera estandarizada.
Mapeo Funcional en Odoo: En el módulo de Ventas o Inventario, se crearán registros de Producto con el Tipo de Producto configurado como "Servicio".5 Esto indica al sistema que no se gestionará stock para estos artículos.
Se crearán productos distintos para cada oferta comercial:
Servicio Correctivo H/H: Un producto de servicio con un precio de venta por hora.
Plan de Mantenimiento Preventivo - Básico: Un producto de servicio con un precio fijo mensual o anual.
Instalación de Equipo Nuevo: Un producto de servicio que puede tener un precio fijo o facturarse por tiempo y materiales.
La configuración de estos productos de servicio es un paso fundamental que impacta directamente los procesos posteriores. Un producto como "Plan de Mantenimiento Preventivo" no es solo una línea en una factura. Al configurarlo adecuadamente, la confirmación de una orden de venta que contenga este producto puede actuar como un disparador para crear automáticamente un conjunto de tareas o solicitudes de mantenimiento preventivo recurrentes en el módulo de Mantenimiento. De esta manera, el producto en el catálogo de ventas se convierte en el catalizador que inicia todo el flujo de trabajo de la prestación del servicio.

1.3. Implementando la Matriz de Competencias de Técnicos

Necesidad del Negocio: El núcleo de la eficiencia en el despacho se basa en la capacidad de asignar la OT correcta al técnico correcto. Esto requiere un sistema que pueda mapear los requisitos de una tarea (Eje 2: Área de Especialización y Eje 3: Nivel de Complejidad) con las habilidades certificadas de cada técnico.
Mapeo Funcional en Odoo: Esta matriz se configurará íntegramente dentro del módulo de Empleados, que en Odoo 18 incluye una funcionalidad nativa para la gestión de habilidades (Skills Management).7
El proceso de configuración es el siguiente:
Crear Tipos de Habilidad (Eje 2): Navegar a Empleados > Configuración > Tipos de Habilidad. Aquí se creará un "Tipo de Habilidad" para cada una de las áreas de especialización técnica: "COC - Cocina y Procesamiento", "REF - Refrigeración y Climatización", "LAV - Lavandería Industrial", etc..8
Crear Habilidades Específicas: Dentro de cada "Tipo de Habilidad", se añadirán las sub-áreas como habilidades individuales. Por ejemplo, bajo el tipo "COC - Cocina", se crearán las habilidades "COC-CAL", "COC-PRE" y "COC-LAV".
Definir Niveles de Competencia (Eje 3): Para cada "Tipo de Habilidad", se definirán los niveles de competencia que corresponden al Eje 3: "N1 - Básico", "N2 - Intermedio", y "N3 - Avanzado / Especialista". A cada nivel se le puede asignar un progreso porcentual (ej. 33%, 66%, 100%) para una visualización clara.8
Asignar Habilidades a los Empleados: En el registro de cada técnico, dentro de la pestaña "Currículum", se añadirán las habilidades específicas que posee y el nivel que ha alcanzado en cada una de ellas.8 Por ejemplo, al técnico Juan Pérez se le asignaría la habilidad "COC-CAL" con el nivel "N3 - Avanzado".
Esta configuración transforma el módulo de Empleados de una simple base de datos de RRHH en una herramienta operativa dinámica y consultable. El trabajo del coordinador de servicios ya no dependerá de hojas de cálculo o de su memoria, sino de un mecanismo de filtrado preciso y en tiempo real dentro del ERP. Esto aumenta directamente la probabilidad de una reparación en la primera visita (First-Time Fix Rate) al garantizar que se envía a la persona adecuada, reduce el tiempo de desplazamiento innecesario y, de forma crucial, proporciona una hoja de ruta clara para la capacitación y el desarrollo del personal (ej. "Tenemos una escasez de técnicos con nivel N3 en Refrigeración Comercial"). Los datos de competencias se convierten en un activo estratégico para la planificación de la capacidad operativa.

1.4. Creando el Registro Maestro de Activos

Necesidad del Negocio: Cada equipo perteneciente a un cliente debe ser identificado de forma única, su historial de servicio debe ser rastreado meticulosamente y toda la información relevante debe estar accesible. Este es el corazón del paso de "Asset Onboarding".
Mapeo Funcional en Odoo: Se utilizará el modelo maintenance.equipment dentro del módulo de Mantenimiento.11
Cada equipo (una freidora, una cámara frigorífica, etc.) será un registro individual en este modelo. Los campos clave a rellenar durante el onboarding son:
Nombre del Equipo: Un descriptor claro (ej. "Freidora Frymaster - Cocina Principal").
Categoría de Equipo: Para agrupar equipos similares.
Propietario: Se vinculará al registro res.partner de la ubicación del cliente (ej. "Hotel Sol Centro").
N.º de serie: Este es un campo crítico. Se registrará el número de serie del fabricante, que es el identificador único del activo.13
Modelo: El modelo específico del equipo.
Fecha de Puesta en Marcha: La fecha de instalación o inicio del servicio.
El campo N.º de serie será la base para la generación de etiquetas QR. Una vez guardado el registro del equipo, Odoo le asigna un ID único en la base de datos. Se puede configurar un informe simple para imprimir una etiqueta QR duradera que contenga la URL directa a la vista de ese registro de equipo en Odoo. Al escanear esta etiqueta con un dispositivo móvil, se abrirá instantáneamente la ficha completa del equipo, con todo su historial.13
La categorización de equipos por defecto en Odoo es plana, lo cual es insuficiente para un entorno HORECA complejo con cientos de activos. Para solucionar esto, se recomienda encarecidamente la instalación del módulo gratuito maintenance_equipment_category_hierarchy de la Odoo Community Association (OCA). Este módulo permite crear una estructura de categorías anidada (ej. Cocina > Equipos de Cocción > Hornos de Convección), lo que facilita enormemente la navegación, el filtrado y la generación de informes.15
Un registro de activos completo y preciso, donde cada solicitud de servicio (OT) está vinculada a un número de serie específico, es el requisito previo para evolucionar de un mantenimiento reactivo a uno proactivo. Con el tiempo, el sistema acumulará un historial detallado para cada activo: número y tipo de fallas, piezas reemplazadas, tiempo de inactividad, etc..16 Esta base de datos histórica es la materia prima indispensable para, en el futuro, implementar estrategias de Mantenimiento Predictivo (M3). Establecer correctamente este registro desde el primer día es una inversión estratégica a largo plazo.

Sección 2: Fase 1 - El Flujo de Trabajo Comercial y de Onboarding de Clientes en Odoo

Esta sección detalla el proceso completo para adquirir un nuevo cliente, formalizar la relación comercial a través de propuestas y contratos, y realizar el levantamiento inicial de sus activos físicos para integrarlos en el sistema ERP. Es la fase donde se sientan las bases para una gestión de servicio fluida y sin fricciones.

2.1. Del Contacto Inicial a la Propuesta de Servicio

Necesidad del Negocio: Es necesario gestionar el embudo de ventas, desde el primer contacto con un cliente potencial hasta la presentación de una propuesta formal de servicios, ya sea para trabajos puntuales o para contratos de mantenimiento preventivo ("Pólizas").
Mapeo Funcional en Odoo: Este proceso se gestionará de forma nativa utilizando la sinergia entre los módulos de CRM y Ventas.
Captura del Lead: Una nueva consulta o contacto comercial se registra como un "Lead" en el módulo de CRM.17 En esta etapa se recopila la información inicial.
Calificación y Oportunidad: Una vez que se determina que el lead tiene un potencial real, se convierte en una "Oportunidad". La oportunidad se gestiona a través de un pipeline de ventas personalizable (ej. Contacto Inicial > Calificación > Propuesta > Negociación).
Generación de la Cotización: Desde la ficha de la Oportunidad, se puede crear directamente una "Cotización" (que es un borrador de Orden de Venta) en el módulo de Ventas. Esta cotización se poblará utilizando los productos de servicio definidos en la Sección 1.2. Se pueden incluir diferentes niveles de servicio (SLAs) como líneas de producto distintas.19
Aceptación Digital: La cotización puede ser enviada al cliente por correo electrónico directamente desde Odoo. El cliente puede revisarla y aceptarla con una firma digital, lo que convierte automáticamente la cotización en una Orden de Venta confirmada, formalizando el acuerdo.19

2.2. Gestión de Contratos de Servicio ("Pólizas") en la Edición Community

Necesidad del Negocio: La venta de contratos de mantenimiento anuales o mensuales ("Pólizas") es un pilar del negocio, generando ingresos recurrentes que requieren una facturación periódica y automática.
El Desafío: Odoo Community Edition no incluye el módulo de Suscripciones, una funcionalidad clave que es exclusiva de la edición Enterprise.20 Por lo tanto, se necesita una solución alternativa robusta para gestionar estos acuerdos.
Solución Propuesta (Automatización Nativa): En lugar de depender de módulos de terceros que pueden tener costos adicionales o problemas de mantenimiento (aunque existen opciones 23), se puede construir un sistema de gestión de contratos utilizando las herramientas de automatización nativas de Odoo.
Crear la Orden de Venta Maestra: Para cada cliente con una "Póliza", se crea una Orden de Venta (OV) que representa el contrato marco anual. En esta OV se detallan los servicios recurrentes (ej. 12 unidades del producto "Mantenimiento Preventivo Mensual - Básico"). Esta OV se mantiene en estado "Confirmado" y sirve como el registro contractual central.
Configurar una Acción Planificada: Se utilizará el motor de automatización de Odoo. Navegando a Ajustes > Técnico > Acciones Planificadas, se crea una nueva acción.26 Esta acción se configurará para ejecutarse de forma periódica (ej. diariamente o semanalmente).
Definir la Lógica de la Automatización: La acción planificada ejecutará un pequeño fragmento de código Python (reutilizable y de bajo mantenimiento) que realizará la siguiente lógica:
Buscará todas las Órdenes de Venta maestras que estén marcadas como una "Póliza" activa (esto se puede hacer usando una etiqueta específica en la OV).
Para cada Póliza, verificará la fecha de la última factura o de la última OV de facturación generada.
Si ha transcurrido el período de facturación (ej. un mes), el script creará automáticamente una nueva Orden de Venta para ese período, copiando las líneas de servicio correspondientes del contrato maestro. Esta nueva OV estará lista para ser facturada por el departamento de administración.
Esta aproximación, aunque requiere una configuración inicial, ofrece un control total sobre la lógica de negocio y evita la dependencia de código externo. Modela perfectamente el proceso real: la OV maestra es el contrato, y las OVs generadas mensualmente son los eventos facturables derivados de ese contrato. Es una solución escalable y robusta que utiliza las capacidades centrales de Odoo.

2.3. El Proceso de Onboarding Digital de Activos

Necesidad del Negocio: Como se identificó en el framework, este es el paso más crítico. Un técnico debe visitar las instalaciones del nuevo cliente, realizar un inventario exhaustivo de todos los equipos cubiertos por el servicio y crear sus registros digitales correspondientes en Odoo.
Mapeo Funcional en Odoo:
Disparador del Proceso: La confirmación de la Orden de Venta maestra (la "Póliza") puede configurarse para disparar automáticamente la creación de una tarea en el módulo de Proyectos. Esto se logra configurando el producto de servicio "Onboarding de Cliente" para que, al venderse, cree una tarea.5 Esta tarea, llamada "Levantamiento Inicial de Activos - [Nombre del Cliente]", se asigna a un técnico o supervisor.
Ejecución en Campo con la App Móvil: El técnico asignado utiliza la interfaz web responsiva de Odoo en su tableta o teléfono móvil directamente en las instalaciones del cliente. Por cada equipo a inventariar, el técnico realizará los siguientes pasos:
Creará un nuevo registro de maintenance.equipment en el módulo de Mantenimiento.12
Rellenará los campos críticos: Categoría, Modelo, y fundamentalmente, el N.º de serie del fabricante.13
Vinculará el equipo a la ubicación correcta del cliente a través del campo Propietario.
Utilizando la cámara de su dispositivo, tomará una foto del equipo y de su placa de características y las adjuntará directamente al registro en Odoo.
Generación e Impresión de Etiquetas QR: Una vez que el registro del equipo se guarda, Odoo le asigna un identificador único. Desde la oficina, se puede ejecutar un informe preconfigurado que imprime una etiqueta duradera y resistente. Esta etiqueta contendrá un código QR que, al ser escaneado, redirige directamente a la URL de la ficha de ese equipo específico en Odoo. La etiqueta se adhiere físicamente a la máquina.
Este paso inicial, aunque intensivo en mano de obra, es el que crea el "gemelo digital" de las instalaciones del cliente. Este gemelo digital es lo que desbloquea la eficiencia en todas las operaciones futuras. Cuando un cliente reporte una avería, puede simplemente escanear el código QR del equipo afectado. Esto comunica instantáneamente al coordinador de servicios de qué máquina específica se trata, cuál es su historial completo de mantenimiento, su estado de garantía y las piezas que se han utilizado en ella anteriormente. Se elimina la ambigüedad, se acelera el diagnóstico y se mejora drásticamente la experiencia del cliente y la eficiencia del técnico.

Sección 3: Fases 2 y 3 - El Flujo Integrado de Solicitud de Servicio, Triage y Despacho

Esta sección aborda el núcleo de las operaciones diarias: el ciclo de recibir una llamada de servicio, clasificarla sistemáticamente según la matriz PATCO, y asignar al técnico más adecuado con la información y los recursos necesarios para resolver la incidencia de la manera más eficiente posible.

3.1. La "Orden de Trabajo" (OT) como Eje Central

Necesidad del Negocio: Cada solicitud de servicio, independientemente de su origen (llamada telefónica, correo electrónico, portal del cliente), debe ser capturada y registrada como una Orden de Trabajo (OT) única y rastreable. Nada se trabaja si no tiene una OT asociada.
Mapeo Funcional en Odoo: El modelo maintenance.request del módulo de Mantenimiento servirá como la Orden de Trabajo digital.28
Creación de la OT: El Coordinador de Servicios, al recibir una llamada, hará clic en el botón "Crear" en el tablero de Mantenimiento.
Campos Esenciales: Se rellenarán los campos críticos para iniciar el proceso:
Solicitud: Un título descriptivo del problema (ej. "La freidora no enciende").
Equipo: Se seleccionará el activo específico del registro maestro creado en la fase de onboarding. Esto se puede hacer buscando por número de serie o nombre del equipo. Vincular la OT a un equipo es fundamental para el historial.
Tipo de Mantenimiento: Se seleccionará "Correctivo" o "Preventivo" según corresponda.
Fecha de la Solicitud: Se registra automáticamente la fecha y hora de creación.28
Para optimizar la captura, Odoo permite la creación automática de solicitudes desde canales externos. Se puede configurar una dirección de correo electrónico (ej. soporte@suempresa.com). Cualquier correo recibido en esta dirección creará automáticamente una solicitud de mantenimiento en estado "Nueva Solicitud", utilizando el asunto del correo como título y el cuerpo como descripción.29 Esto centraliza todas las solicitudes y reduce la carga de entrada manual de datos para el coordinador.

3.2. Aplicando la Matriz de Clasificación Operativa

Necesidad del Negocio: El coordinador debe aplicar el triage a cada OT, asignándole su código de clasificación único M/AREA/N para estandarizar el diagnóstico inicial y facilitar el despacho.
Mapeo Funcional en Odoo: Esta clasificación se implementará de manera elegante y efectiva utilizando el sistema de Etiquetas (Tags) en el formulario de la solicitud de mantenimiento. El uso de etiquetas es una práctica estándar en Odoo para categorizar registros de forma flexible.30
Configuración Previa de Etiquetas: El administrador del sistema creará previamente un conjunto de etiquetas que correspondan a cada valor posible de la matriz de clasificación. Se crearán categorías de etiquetas para mantener el orden (ej. categoría "Naturaleza", categoría "Área", categoría "Complejidad"). Las etiquetas serían, por ejemplo: M1-Correctivo, M2-Preventivo, COC-CAL, REF-COM, N1-Básico, N2-Intermedio, N3-Avanzado.
Proceso de Triage: Para cada nueva OT, el coordinador, basándose en la descripción del cliente y realizando preguntas clave ("¿Qué luces se encienden?", "¿Hace algún ruido extraño?"), seleccionará las tres etiquetas correspondientes del menú desplegable. Siguiendo el ejemplo del "Lavavajillas que no calienta", el coordinador aplicaría las etiquetas: M1-Correctivo, COC-LAV, y N2-Intermedio.
Estas etiquetas son mucho más que simples identificadores visuales; se convierten en la principal herramienta para la gestión y el análisis operativo. El coordinador puede crear filtros personalizados y vistas agrupadas en el tablero Kanban de mantenimiento. Por ejemplo, puede crear una vista guardada para "Todos los trabajos Urgentes (M1) de Refrigeración (REF)" o "Todas las tareas Preventivas (M2) de Nivel Básico (N1) pendientes". Esto proporciona una visibilidad instantánea y dinámica de la carga y tipo de trabajo, permitiendo una gestión proactiva sin necesidad de generar informes complejos.

3.3. Asignación de Técnicos Basada en Competencias y Programación

Necesidad del Negocio: Una vez clasificada la OT, se debe asignar a un técnico que no solo esté disponible, sino que posea las competencias técnicas requeridas (Área y Nivel) para resolver la incidencia eficientemente.
Mapeo Funcional en Odoo: Este será un proceso manual para el coordinador, pero estará fuertemente guiado por los datos del sistema, eliminando la subjetividad.
Identificar Requisitos: El coordinador observa la OT y sus etiquetas (ej. COC-LAV, N2-Intermedio).
Filtrar Técnicos Cualificados: Navega a la vista de lista del módulo de Empleados.
Aplicar Filtros Avanzados: Utiliza la barra de búsqueda para aplicar filtros basados en las habilidades configuradas en la Sección 1.3. La búsqueda sería: "Habilidades contiene COC-LAV" Y "Nivel de Habilidad es N2-Intermedio O N3-Avanzado". El sistema devolverá una lista corta y precisa de todos los técnicos cualificados para ese trabajo específico.
Verificar Disponibilidad: A partir de esta lista filtrada, el coordinador puede revisar la disponibilidad de los técnicos (utilizando el módulo de Calendario de Odoo o una vista de planificación si se instala un módulo comunitario para ello) y su ubicación geográfica para optimizar rutas.
Asignar la OT: Finalmente, regresa a la OT en el módulo de Mantenimiento y selecciona al técnico elegido en el campo Responsable.28
Aunque Odoo Community no dispone de un sistema de despacho automático con optimización de rutas como la aplicación Field Service de la edición Enterprise, esta capacidad de filtrado por competencias es la implementación directa de la lógica de negocio del framework PATCO. El sistema no elige al técnico, pero proporciona al coordinador una lista de candidatos perfectamente cualificados, eliminando el riesgo de asignar un trabajo a personal no capacitado y sentando las bases para un alto índice de resolución en la primera visita.

3.4. Verificación Integrada de Repuestos

Necesidad del Negocio: Antes de enviar a un técnico, es crucial verificar la disponibilidad de los repuestos más probables para la reparación. Esto evita visitas inútiles y gestiona las expectativas del cliente.
Mapeo Funcional en Odoo: Este proceso requiere una integración fluida entre los módulos de Mantenimiento e Inventario.
Vincular Repuestos a la OT: El formulario de maintenance.request por defecto no incluye una lista de materiales. Sin embargo, el módulo de Reparaciones, que se integra con Mantenimiento, sí la tiene.32 La mejor práctica es que el coordinador, desde la OT, cree una "Orden de Reparación" vinculada.
Consulta de Stock en Tiempo Real: En la Orden de Reparación, el coordinador o el técnico asignado pueden añadir las piezas que probablemente se necesitarán (ej. "Resistencia para lavavajillas modelo X"). Al añadir cada producto, el sistema mostrará la cantidad "Prevista" o "A mano" de ese artículo en el inventario.32
Gestión de Múltiples Almacenes: El módulo de Inventario de Odoo permite configurar múltiples ubicaciones de stock. Se puede crear una ubicación principal ("Almacén Central") y ubicaciones secundarias para cada una de las furgonetas de los técnicos ("Furgoneta - Juan Pérez"). El sistema puede mostrar la disponibilidad de la pieza en todas estas ubicaciones.33
Este paso es un motor clave para la comunicación proactiva y la eficiencia. Si el sistema indica que la pieza necesaria no está en stock ni en el almacén central ni en la furgoneta del técnico, esta información se conoce antes del desplazamiento. Esto permite al coordinador contactar inmediatamente al cliente para informarle de una posible demora mientras se gestiona la compra del repuesto. Esta acción transforma un potencial punto de fricción (falta de stock) en una demostración de profesionalismo y transparencia, gestionando las expectativas del cliente y evitando el costo de una visita improductiva.

Sección 4: Fase 4 - El Flujo de Trabajo de Ejecución en Campo y Reporte Digital

Esta sección se centra en la perspectiva del técnico en el terreno. Detalla cómo el sistema Odoo, a través de un dispositivo móvil, le proporciona las herramientas necesarias para ejecutar el trabajo de manera eficiente, documentar sus acciones en tiempo real y, de forma crucial, integrar el informe de servicio detallado generado por el agente de IA externo.

4.1. El Flujo de Trabajo Móvil del Técnico en Odoo

Necesidad del Negocio: Los técnicos necesitan acceso móvil a sus OTs asignadas, información detallada del cliente y del equipo, y una forma sencilla de registrar el progreso de su trabajo, las piezas utilizadas y el tiempo invertido.
Mapeo Funcional en Odoo: Odoo 18 Community Edition cuenta con una interfaz web totalmente responsiva, lo que significa que funciona de manera fluida y nativa en navegadores de tabletas y teléfonos inteligentes sin necesidad de una aplicación móvil dedicada.
Acceso a Tareas: El técnico inicia sesión en Odoo desde su dispositivo y accede al tablero de Mantenimiento. Verá una vista predeterminada o podrá aplicar un filtro para mostrar solo "Mis Órdenes de Trabajo".
Actualización de Estado en Tiempo Real: Al llegar a las instalaciones del cliente, el técnico abre la OT correspondiente y cambia su etapa de "Nuevo" o "Programado" a "En Progreso". Este cambio de estado se refleja instantáneamente en el sistema central, informando al coordinador que el trabajo ha comenzado (su protocolo "En Sitio").
Consulta de Historial: Desde la OT, el técnico tiene acceso directo a la ficha del equipo vinculado. Allí puede consultar todo su historial de mantenimiento: fallas anteriores, reparaciones realizadas, piezas cambiadas. Esto proporciona un contexto valioso para el diagnóstico.
Consumo de Repuestos: Si se ha creado una Orden de Reparación vinculada (como se detalla en 3.4), el técnico puede confirmar las piezas que ha utilizado de su stock de furgoneta. Al marcar una pieza como "Usada", el sistema descuenta automáticamente esa unidad del inventario de su ubicación "Furgoneta -", manteniendo el control de stock en tiempo real.32
Registro de Tiempos: En la pestaña "Partes de Horas" (Timesheets) de la OT, el técnico registra el tiempo dedicado al trabajo. Puede iniciar un temporizador o añadir entradas de tiempo manualmente, describiendo brevemente la actividad realizada.34

4.2. El Punto de Entrega al Agente de IA

Necesidad del Negocio: El proceso operativo dicta que el informe de mantenimiento detallado, con comentarios técnicos y fotos, es generado por un agente de IA externo en formato de Google Doc. Es imperativo que el enlace a este documento externo quede permanentemente asociado al registro de la OT en Odoo para garantizar una trazabilidad completa.
Mapeo Funcional en Odoo: Este requisito se satisface con una personalización menor y de bajo riesgo en el formulario de la solicitud de mantenimiento, utilizando las herramientas de Odoo.
Paso de Configuración (única vez): Un administrador, con el modo desarrollador activado, puede editar la vista del formulario maintenance.request. No es necesario crear un módulo personalizado completo. Se añadirá un nuevo campo al modelo. Este campo será de tipo Char (texto) y se le aplicará el widget url para que se muestre como un enlace clicable. El campo se etiquetará como "Enlace a Informe de Servicio (IA)".37
Flujo de Trabajo del Técnico: Una vez que el técnico ha completado la intervención y el agente de IA ha generado el informe en Google Docs, el técnico obtiene el enlace para compartir de dicho documento. A continuación, simplemente abre la OT en su dispositivo móvil, navega al nuevo campo "Enlace a Informe de Servicio (IA)" y pega la URL.
Este enfoque representa una integración pragmática y potente. Evita la complejidad de intentar replicar un sistema avanzado de generación de informes con checklists dinámicas y gestión de múltiples imágenes dentro de Odoo Community, lo cual podría ser engorroso. En su lugar, se apalanca en una herramienta externa especializada (el agente de IA) para la tarea en la que sobresale (creación de contenido rico), mientras se utiliza Odoo para su propósito principal: ser el sistema centralizado y estructurado de registro. El simple campo de URL actúa como un puente robusto y elegante entre ambos sistemas, creando un flujo de trabajo sin fisuras para el técnico y un registro de auditoría completo para la oficina.

4.3. Cierre Digital del Trabajo y Conformidad del Cliente

Necesidad del Negocio: Es necesario obtener y registrar la conformidad del cliente de que el trabajo se ha realizado a su satisfacción antes de que el técnico abandone las instalaciones.
Mapeo Funcional en Odoo: Si bien la edición Enterprise de Odoo cuenta con una aplicación Firma dedicada para capturar firmas digitales, se puede lograr una confirmación funcional y auditable en la edición Community.
Documentación en el Chatter: Una vez finalizado el trabajo, el técnico muestra al cliente la OT en su dispositivo móvil, explicando las acciones realizadas. A continuación, utiliza la función de "Registrar nota" (chatter) en la parte inferior de la OT para documentar la aprobación. Escribirá una nota como: "Trabajo finalizado. El cliente, Sr. [Nombre del Contacto], revisa el funcionamiento del equipo y da su conformidad verbal el [Fecha] a las [Hora]". Esta nota queda registrada con fecha, hora y usuario.
Cambio de Etapa: Tras registrar la nota, el técnico mueve la OT a la siguiente etapa del flujo, que podría ser "Reparado" o una etapa personalizada como "Pendiente de Cierre Administrativo".
Para una formalidad mayor, existen módulos de terceros en la Odoo App Store que añaden la capacidad de capturar una firma directamente en la pantalla del dispositivo móvil y adjuntarla como imagen a la OT. Sin embargo, el registro en el chatter es una solución nativa, robusta y legalmente válida en muchos contextos para documentar la aceptación del servicio.

Sección 5: Fase 5 - El Flujo de Trabajo de Cierre Administrativo, Facturación y Análisis

Esta sección final describe los procesos de back-office que completan el ciclo de vida del servicio. Cubre la automatización de la facturación y la comunicación con el cliente, así como el uso estratégico de los datos recopilados para medir el rendimiento operativo e impulsar un ciclo de mejora continua.

5.1. Facturación Automatizada y Entrega de Informes

Necesidad del Negocio: Una vez que una OT se marca como finalizada en el campo, el área administrativa debe ser notificada para proceder con la facturación (si aplica) y enviar al cliente el informe final del servicio de manera oportuna y profesional.
Mapeo Funcional en Odoo: Este flujo se orquestará mediante una Acción Automatizada, una potente herramienta nativa de Odoo para crear flujos de trabajo basados en reglas.38
Disparador (Trigger): Se configurará una nueva Acción Automatizada en Ajustes > Técnico > Automatización > Acciones Automatizadas. El disparador de esta acción será "Al actualizar un registro", específicamente cuando el campo Etapa de un registro de maintenance.request se mueva a una etapa final como "Reparado" o "Cerrado".39
Acción 1 - Creación de Factura:
Para los trabajos que no están cubiertos por una "Póliza", la acción puede configurarse para "Crear un nuevo registro".
El nuevo registro será una "Factura de Cliente" (account.move).
Los datos para la factura (cliente, productos de servicio, horas registradas, repuestos utilizados) se pueden obtener dinámicamente de la OT y de la Orden de Reparación vinculada.
La factura se creará en estado "Borrador", permitiendo que el departamento de contabilidad la revise y valide antes de enviarla.
Acción 2 - Entrega del Informe al Cliente:
La misma acción automatizada también puede "Enviar un correo electrónico".40
Se creará una plantilla de correo electrónico personalizada. Esta plantilla incluirá un mensaje de agradecimiento, un enlace a la factura (una vez validada), y, de manera crucial, utilizará un marcador de posición dinámico para insertar el contenido del campo "Enlace a Informe de Servicio (IA)" de la OT.
De este modo, en el momento en que el trabajo se cierra, el cliente recibe automáticamente un correo electrónico profesional con toda la documentación relevante, cerrando el ciclo de comunicación de forma eficiente.

5.2. Estableciendo un Ciclo de Mejora Continua con KPIs de Odoo

Necesidad del Negocio: Para mejorar continuamente, la empresa debe medir sistemáticamente los Indicadores Clave de Rendimiento (KPIs) que definió: CSAT (Puntuación de Satisfacción del Cliente), MTTR (Tiempo Medio de Reparación) y FTFR (Tasa de Reparación en la Primera Visita).
Mapeo Funcional en Odoo:
CSAT (Customer Satisfaction Score):
El Desafío: El módulo de Encuestas de Odoo, que permite crear y enviar encuestas de satisfacción de forma nativa, es una característica de la edición Enterprise.43
Solución Alternativa Pragmática: Se utilizará una herramienta externa gratuita y eficaz como Google Forms. La Acción Automatizada descrita en 5.1, que envía el correo de cierre al cliente, se modificará para incluir un enlace a una encuesta de CSAT creada en Google Forms. El texto del correo incluirá una llamada a la acción clara: "Valoramos su opinión. Por favor, dedique un minuto a calificar nuestro servicio aquí: [enlace a Google Forms]".44 Si bien los resultados se recopilan fuera de Odoo, el proceso de
solicitar la retroalimentación está completamente automatizado e integrado en el flujo de trabajo de cierre, asegurando una alta tasa de respuesta.
MTTR (Mean Time To Repair / Tiempo Medio de Reparación):
Solución Nativa: Este es un KPI que Odoo calcula de forma nativa. El módulo de Mantenimiento registra automáticamente el MTTR para cada pieza de equipo. El cálculo se basa en la diferencia de tiempo entre el campo Fecha de la Solicitud y la fecha en que la OT se mueve a una etapa final "hecha" (done) para todas las solicitudes de tipo correctivo.11 Este valor se puede visualizar directamente en la ficha del equipo y es una medida disponible en los informes de análisis de mantenimiento.46
FTFR (First-Time Fix Rate / Tasa de Reparación en la Primera Visita):
El Desafío: Este no es un KPI estándar en Odoo y debe construirse a través de un proceso de negocio disciplinado y una configuración menor.
Proceso Propuesto para Medición:
Configuración: Se añade un campo personalizado al formulario de maintenance.request llamado "OT Relacionada (Repetición)". Este campo permitirá vincular una OT con otra.
Regla de Negocio: Se establece una regla operativa estricta: si un técnico debe regresar para atender el mismo problema dentro de un período de tiempo definido (ej. 30 días), el coordinador no reabre la OT original. En su lugar, crea una nueva OT y utiliza el campo "OT Relacionada" para vincularla a la solicitud original.
Cálculo del KPI: Con estos datos, se puede crear un informe que calcule el FTFR. La fórmula sería: FTFR=Total de OTs Cerradas(Total de OTs Cerradas−Total de OTs que tienen una ’OT Relacionada’)​×100. Este método proporciona una medida cuantitativa y precisa de uno de los indicadores más críticos de la eficiencia del servicio de campo.

5.3. El Tablero de Mando para la Gerencia

Necesidad del Negocio: La dirección requiere una vista consolidada y de alto nivel de las métricas operativas clave para la toma de decisiones estratégicas, sin tener que sumergirse en informes detallados.
Mapeo Funcional en Odoo: Aunque Odoo Community carece del constructor de tableros de arrastrar y soltar de la edición Enterprise, es posible crear un "centro de informes" muy funcional utilizando las herramientas estándar.
Informes Guardados como Favoritos: Los usuarios pueden crear vistas de informes complejas y guardarlas como "Favoritos" para acceder a ellas con un solo clic desde el menú.46
Vistas Clave para la Gerencia:
Análisis de MTTR: Se puede crear una vista de tabla dinámica (pivot) en el informe de Análisis de Mantenimiento que muestre el MTTR promedio, agrupado por Categoría de Equipo o por Técnico Responsable. Esto ayuda a identificar qué tipos de equipos fallan más o qué técnicos pueden necesitar capacitación adicional.
Análisis de Carga de Trabajo: Un informe que muestre el Conteo de OTs agrupadas por las Etiquetas de clasificación (M, AREA, N). Esto revela instantáneamente dónde se concentra la mayor parte del trabajo (ej. "La mayoría de nuestras OTs son M1-Correctivo para equipos COC-CAL de nivel N2").
Análisis de FTFR: Un informe de lista que filtre todas las OTs que tienen un valor en el campo "OT Relacionada", proporcionando una lista directa de todos los trabajos que requirieron una segunda visita.
Al guardar estas vistas como favoritos y, si se desea, crear elementos de menú personalizados que apunten a ellas, la gerencia puede tener un acceso rápido y eficiente a los datos que necesita para supervisar la salud de la operación y tomar decisiones informadas.47
Obras citadas
res.users & res.partner - Odoo, fecha de acceso: agosto 22, 2025, https://www.odoo.com/forum/help-1/resusers-respartner-219027
What is res.partner ? | Odoo, fecha de acceso: agosto 22, 2025, https://www.odoo.com/forum/help-1/what-is-respartner-61205
Odoo res.partner Concept on Odoo 18 - Streamline Customer and ..., fecha de acceso: agosto 22, 2025, https://www.technaureus.com/blog-detail/odoo-partner-respartner-concept-2
res.partner auto populated address parent to child - Odoo, fecha de acceso: agosto 22, 2025, https://www.odoo.com/forum/help-1/respartner-auto-populated-address-parent-to-child-177533
Create Projects and Tasks from Sales Orders — Odoo 13.0 documentation, fecha de acceso: agosto 22, 2025, https://www.odoo.com/documentation/13.0/applications/services/project/advanced/so_to_task.html
Odoo 10: How to create project tasks from sale orders? - Stack Overflow, fecha de acceso: agosto 22, 2025, https://stackoverflow.com/questions/42412189/odoo-10-how-to-create-project-tasks-from-sale-orders
Employees — Odoo 18.0 documentation, fecha de acceso: agosto 22, 2025, https://www.odoo.com/documentation/18.0/applications/hr/employees.html
New employees — Odoo 18.0 documentation, fecha de acceso: agosto 22, 2025, https://www.odoo.com/documentation/18.0/applications/hr/employees/new_employee.html
Skill Types in Odoo 18 Employees | Odoo 18 Community Book, fecha de acceso: agosto 22, 2025, https://www.cybrosys.com/odoo/odoo-books/v18-ce/employees/skill-types/
Skills Management - Odoo Apps Store, fecha de acceso: agosto 22, 2025, https://apps.odoo.com/apps/modules/11.0/hr_skill
Odoo Maintenance, fecha de acceso: agosto 22, 2025, https://www.odoo.com/app/maintenance
Equipment Management in Odoo 13 - Cybrosys Technologies, fecha de acceso: agosto 22, 2025, https://www.cybrosys.com/blog/equipment-management-odoo-13
Serial numbers — Odoo 18.0 documentation, fecha de acceso: agosto 22, 2025, https://www.odoo.com/documentation/18.0/applications/inventory_and_mrp/inventory/product_management/product_tracking/serial_numbers.html
How to Ensure Accurate Inventory Tracking with Lot and Serial Numbers in Odoo 18, fecha de acceso: agosto 22, 2025, https://www.cybrosys.com/blog/how-to-ensure-accurate-inventory-tracking-with-lot-and-serial-numbers-in-odoo-18
OCA/maintenance: Odoo modules for businesses that ... - GitHub, fecha de acceso: agosto 22, 2025, https://github.com/OCA/maintenance
Product tracking — Odoo 18.0 documentation, fecha de acceso: agosto 22, 2025, https://www.odoo.com/documentation/18.0/applications/inventory_and_mrp/inventory/product_management/product_tracking.html
CRM — Odoo 18.0 documentation, fecha de acceso: agosto 22, 2025, https://www.odoo.com/documentation/18.0/applications/sales/crm.html
Sales — Odoo 18.0 documentation, fecha de acceso: agosto 22, 2025, https://www.odoo.com/documentation/18.0/applications/sales.html
Odoo Sales Software | Powerful CRM & Quotation - Synconics Technologies, fecha de acceso: agosto 22, 2025, https://www.synconics.com/odoo-sales
What are the Differences Between Community & Enterprise in Odoo 18 Members, fecha de acceso: agosto 22, 2025, https://www.cybrosys.com/blog/what-are-the-differences-between-community-enterprise-in-odoo-18-members
Odoo Enterprise vs Community | Odoo Editions Comparison, fecha de acceso: agosto 22, 2025, https://www.odoo.com/page/editions
All Apps - Odoo, fecha de acceso: agosto 22, 2025, https://www.odoo.com/page/all-apps
Subscription | Odoo Apps Store, fecha de acceso: agosto 22, 2025, https://apps.odoo.com/apps/modules/category/Subscription/browse
Subscription Management For Community - Odoo Apps Store, fecha de acceso: agosto 22, 2025, https://apps.odoo.com/apps/modules/15.0/subscription_package
Sales Subscription for community - Odoo Apps Store, fecha de acceso: agosto 22, 2025, https://apps.odoo.com/apps/modules/13.0/community_subscription
Scheduled actions — Odoo 18.0 documentation, fecha de acceso: agosto 22, 2025, https://www.odoo.com/documentation/18.0/applications/sales/subscriptions/scheduled_actions.html
Odoo 18 Development: Automate Tasks with Cron Jobs & Scheduled Actions - YouTube, fecha de acceso: agosto 22, 2025, https://www.youtube.com/watch?v=HQ4XLCw-2tM
Maintenance requests — Odoo 18.0 documentation, fecha de acceso: agosto 22, 2025, https://www.odoo.com/documentation/18.0/applications/inventory_and_mrp/maintenance/maintenance_requests.html
Receiving tickets — Odoo 18.0 documentation, fecha de acceso: agosto 22, 2025, https://www.odoo.com/documentation/18.0/applications/services/helpdesk/overview/receiving_tickets.html
Help Desk request categorizaton : r/Odoo - Reddit, fecha de acceso: agosto 22, 2025, https://www.reddit.com/r/Odoo/comments/1m298xv/help_desk_request_categorizaton/
Ticket TYPE field in Helpdesk is missing in Odoo v18, fecha de acceso: agosto 22, 2025, https://www.odoo.com/forum/help-1/ticket-type-field-in-helpdesk-is-missing-in-odoo-v18-270739
Process repair orders — Odoo 18.0 documentation, fecha de acceso: agosto 22, 2025, https://www.odoo.com/documentation/18.0/applications/inventory_and_mrp/repairs/repair_orders.html
The #1 Open Source Inventory Management | Odoo, fecha de acceso: agosto 22, 2025, https://www.odoo.com/app/inventory
Timesheets — Odoo 18.0 documentation, fecha de acceso: agosto 22, 2025, https://www.odoo.com/documentation/18.0/applications/services/timesheets.html
Helpdesk Ticket Timesheet | The Odoo Community Association | OCA, fecha de acceso: agosto 22, 2025, https://odoo-community.org/shop/helpdesk-ticket-timesheet-5522
Odoo Helpdesk - Track & Bill Time - YouTube, fecha de acceso: agosto 22, 2025, https://www.youtube.com/watch?v=_qLdR4wjrqs
Studio — Odoo 18.0 documentation, fecha de acceso: agosto 22, 2025, https://www.odoo.com/documentation/18.0/applications/studio.html
Automation rules — Odoo 18.0 documentation, fecha de acceso: agosto 22, 2025, https://www.odoo.com/documentation/18.0/applications/studio/automated_actions.html
Close tickets — Odoo 18.0 documentation, fecha de acceso: agosto 22, 2025, https://www.odoo.com/documentation/18.0/applications/services/helpdesk/advanced/close_tickets.html
How to Create & Manage a Helpdesk Ticket From a Lead in Odoo 18, fecha de acceso: agosto 22, 2025, https://www.cybrosys.com/blog/how-to-create-and-manage-a-helpdesk-ticket-from-a-lead-in-odoo-18
How to Create & Manage Stages in Odoo 18 Helpdesk - YouTube, fecha de acceso: agosto 22, 2025, https://www.youtube.com/watch?v=Hq1Y7HN8W3s
Stages — Odoo 18.0 documentation - Helpdesk, fecha de acceso: agosto 22, 2025, https://www.odoo.com/documentation/18.0/applications/services/helpdesk/overview/stages.html
Design Your Surveys - Odoo, fecha de acceso: agosto 22, 2025, https://www.odoo.com/app/surveys
Customer ratings — Odoo 18.0 documentation, fecha de acceso: agosto 22, 2025, https://www.odoo.com/documentation/18.0/applications/services/helpdesk/overview/ratings.html
How to calculate 'Mean Time to Repair' in Odoo18 Maintenance Module? | Odoo, fecha de acceso: agosto 22, 2025, https://www.odoo.com/forum/help-1/how-to-calculate-mean-time-to-repair-in-odoo18-maintenance-module-282507
Reporting — Odoo 16.0 documentation, fecha de acceso: agosto 22, 2025, https://www.odoo.com/documentation/16.0/applications/services/helpdesk/overview/reports.html
KPI Balanced Scorecard | Odoo KPIs - faOtools, fecha de acceso: agosto 22, 2025, https://faotools.com/apps/18.0/kpi-balanced-scorecard-18-0-kpi-scorecard-918
Odoo 18 Custom KPI Dashboard – Real-Time Sales & Inventory Analytics ** Odoo18 Development - YouTube, fecha de acceso: agosto 22, 2025, https://www.youtube.com/watch?v=Qon8a-legzs
Analyze metrics — Odoo 18.0 documentation, fecha de acceso: agosto 22, 2025, https://www.odoo.com/documentation/18.0/applications/marketing/email_marketing/analyze_metrics.html
