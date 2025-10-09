# Documentación del Modelo res.partner - Odoo 18

## Tabla de Contenidos
1. [Información General](#información-general)
2. [Campos del Core de Odoo 18](#campos-del-core-de-odoo-18)
3. [Campos Computados](#campos-computados)
4. [Métodos Principales](#métodos-principales)
5. [Lógica de Negocio](#lógica-de-negocio)
6. [Campos Agregados por Módulos OCA](#campos-agregados-por-módulos-oca)

---

## Información General

El modelo `res.partner` es uno de los modelos más importantes en Odoo, representando contactos, clientes, proveedores y empresas. En Odoo 18, este modelo hereda de múltiples mixins para proporcionar funcionalidades avanzadas.

**Herencias:**
- `FormatAddressMixin`: Formateo de direcciones
- `FormatVATLabelMixin`: Formateo de etiquetas VAT
- `avatar.mixin`: Gestión de avatares
- `mail.activity.mixin`: Actividades de correo
- `mail.thread.blacklist`: Lista negra de correos

**Archivo principal:** `odoo/addons/base/models/res_partner.py`

---

## Campos del Core de Odoo 18

### Campos de Identificación
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `name` | Char | Nombre del contacto/empresa |
| `complete_name` | Char (computed) | Nombre completo incluyendo jerarquía |
| `display_name` | Char (computed) | Nombre para mostrar con contexto |
| `ref` | Char | Referencia interna del partner |
| `barcode` | Char | Código de barras único |

### Campos de Relaciones
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `parent_id` | Many2one | Partner padre (empresa) |
| `child_ids` | One2many | Contactos hijos |
| `commercial_partner_id` | Many2one (computed) | Entidad comercial |
| `commercial_company_name` | Char (computed) | Nombre de la empresa comercial |
| `company_name` | Char | Nombre de empresa (para crear padre) |

### Campos de Tipo y Clasificación
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `is_company` | Boolean | Es una empresa |
| `is_public` | Boolean (computed) | Es un usuario público |
| `company_type` | Selection | Tipo: 'person' o 'company' |
| `type` | Selection | Tipo de dirección: 'contact', 'invoice', 'delivery', 'other' |
| `title` | Many2one | Título (Sr., Sra., etc.) |
| `function` | Char | Cargo/función |
| `industry_id` | Many2one | Industria |
| `category_id` | Many2many | Etiquetas/categorías |

### Campos de Dirección
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `street` | Char | Calle |
| `street2` | Char | Calle 2 |
| `zip` | Char | Código postal |
| `city` | Char | Ciudad |
| `state_id` | Many2one | Estado/provincia |
| `country_id` | Many2one | País |
| `partner_latitude` | Float | Latitud |
| `partner_longitude` | Float | Longitud |
| `contact_address` | Char (computed) | Dirección completa |

### Campos de Contacto
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `email` | Char | Correo electrónico |
| `email_formatted` | Char (computed) | Email formateado |
| `phone` | Char | Teléfono |
| `mobile` | Char | Móvil |
| `website` | Char | Sitio web |

### Campos de Localización
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `lang` | Selection | Idioma |
| `tz` | Selection | Zona horaria |

### Campos Fiscales y Legales
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `vat` | Char | Número de identificación fiscal |
| `vat_label` | Char (computed) | Etiqueta VAT localizada |
| `same_vat_partner_id` | Many2one (computed) | Partner con mismo VAT |
| `company_registry` | Char | Registro mercantil |
| `company_registry_label` | Char (computed) | Etiqueta de registro |

### Campos Financieros
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `bank_ids` | One2many | Cuentas bancarias |
| `property_product_pricelist` | Many2one | Lista de precios |

### Campos de Usuario y Permisos
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `user_id` | Many2one | Vendedor responsable |
| `user_ids` | One2many | Usuarios relacionados |
| `partner_share` | Boolean (computed) | Es un partner compartido |

### Campos de Empresa
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `company_id` | Many2one | Empresa |
| `employee` | Boolean | Es empleado |

### Campos Visuales
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `color` | Integer | Color para kanban |
| `avatar_128`, `avatar_256`, `avatar_512`, `avatar_1024`, `avatar_1920` | Binary | Avatares en diferentes tamaños |
| `image_128`, `image_256`, `image_512`, `image_1024`, `image_1920` | Binary | Imágenes en diferentes tamaños |

### Campos de Notas
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `comment` | Text | Notas internas |

### Campos Técnicos
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `active` | Boolean | Registro activo |
| `starred_message_ids` | Many2many | Mensajes destacados |
| `message_bounce` | Integer | Rebotes de email |

---

## Campos Computados

### Principales Campos Computados
- **`complete_name`**: Construye el nombre completo incluyendo la jerarquía de padres
- **`display_name`**: Nombre contextual que puede incluir dirección, email, VAT según el contexto
- **`commercial_partner_id`**: Identifica la entidad comercial principal
- **`commercial_company_name`**: Nombre de la empresa comercial
- **`contact_address`**: Dirección formateada completa
- **`email_formatted`**: Email en formato "Nombre <email@domain.com>"
- **`is_public`**: Determina si el partner tiene usuarios públicos
- **`partner_share`**: Indica si es un partner externo (no empleado)
- **`same_vat_partner_id`**: Encuentra partners con el mismo VAT
- **`vat_label`**: Etiqueta localizada para el campo VAT

---

## Métodos Principales

### Métodos de Creación y Escritura
- **`create(vals_list)`**: Creación con sincronización de campos
- **`write(vals)`**: Escritura con validaciones y sincronización
- **`name_create(name)`**: Creación rápida desde nombre/email
- **`find_or_create(email)`**: Buscar o crear por email

### Métodos de Sincronización
- **`_fields_sync(values)`**: Sincroniza campos comerciales y de dirección
- **`_commercial_sync_from_company()`**: Sincroniza desde entidad comercial
- **`_commercial_sync_to_children()`**: Sincroniza a contactos hijos
- **`_children_sync(values)`**: Sincroniza cambios a hijos
- **`update_address(vals)`**: Actualiza campos de dirección

### Métodos de Dirección
- **`address_get(adr_pref)`**: Obtiene direcciones por tipo
- **`_display_address(without_company)`**: Formatea dirección para mostrar
- **`_get_address_format()`**: Obtiene formato de dirección por país

### Métodos de Validación
- **`_check_barcode_unicity()`**: Valida unicidad del código de barras
- **`_check_import_consistency(vals_list)`**: Valida consistencia en importación

### Métodos OnChange
- **`onchange_parent_id()`**: Actualiza campos al cambiar padre
- **`onchange_country_id()`**: Actualiza estado al cambiar país
- **`onchange_state_id()`**: Valida estado según país
- **`_onchange_company_type()`**: Actualiza is_company según tipo

### Métodos Utilitarios
- **`create_company()`**: Crea empresa padre desde contacto
- **`open_commercial_entity()`**: Abre vista de entidad comercial
- **`_get_gravatar_image(email)`**: Obtiene imagen de Gravatar

---

## Lógica de Negocio

### Sincronización de Campos Comerciales
Los campos comerciales (`vat`, `company_registry`, `industry_id`) se sincronizan automáticamente:
- Desde la entidad comercial hacia contactos
- Entre contactos de la misma entidad comercial

### Sincronización de Direcciones
Los campos de dirección se sincronizan:
- Desde el padre hacia contactos tipo 'contact'
- Cuando se cambia el padre o el tipo

### Validaciones Importantes
1. **Usuarios activos**: No se pueden archivar partners con usuarios activos
2. **Código de barras único**: Cada partner debe tener un código único
3. **Consistencia de empresa**: La empresa debe ser compatible con usuarios relacionados
4. **VAT duplicado**: Se detectan partners con el mismo VAT

### Herencia de Campos
- **Campos comerciales**: Se heredan de la entidad comercial
- **Campos de dirección**: Los contactos heredan del padre si no tienen valores propios
- **Idioma**: Se propaga desde el padre si no se especifica

---

## Campos Agregados por Módulos Nativos de Odoo

### Módulo: account
**Archivo:** `addons/account/models/partner.py`

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `fiscal_country_codes` | Char (computed) | Códigos de países fiscales |
| `partner_vat_placeholder` | Char (computed) | Placeholder para VAT |
| `partner_company_registry_placeholder` | Char (computed) | Placeholder para registro mercantil |
| `duplicate_bank_partner_ids` | Many2many (related) | Partners con cuentas bancarias duplicadas |
| `credit` | Monetary (computed) | Total por cobrar del cliente |
| `credit_to_invoice` | Monetary (computed) | Crédito pendiente de facturar |
| `credit_limit` | Float | Límite de crédito específico del partner |
| `use_partner_credit_limit` | Boolean (computed) | Usar límite de crédito del partner |
| `show_credit_limit` | Boolean (computed) | Mostrar límite de crédito |
| `days_sales_outstanding` | Float (computed) | Días de ventas pendientes (DSO) |
| `debit` | Monetary (computed) | Total por pagar al proveedor |
| `debit_limit` | Monetary | Límite de deuda |
| `total_invoiced` | Monetary (computed) | Total facturado |
| `currency_id` | Many2one (computed) | Moneda de la empresa |
| `journal_item_count` | Integer (computed) | Contador de asientos contables |
| `property_account_payable_id` | Many2one | Cuenta por pagar |
| `property_account_receivable_id` | Many2one | Cuenta por cobrar |
| `property_account_position_id` | Many2one | Posición fiscal |
| `property_payment_term_id` | Many2one | Términos de pago del cliente |
| `property_supplier_payment_term_id` | Many2one | Términos de pago del proveedor |
| `ref_company_ids` | One2many | Empresas que referencian al partner |
| `supplier_invoice_count` | Integer (computed) | Contador de facturas de proveedor |
| `invoice_ids` | One2many | Facturas |
| `contract_ids` | One2many | Contratos analíticos |
| `bank_account_count` | Integer (computed) | Contador de cuentas bancarias |
| `trust` | Selection | Grado de confianza crediticia |
| `ignore_abnormal_invoice_date` | Boolean | Ignorar fecha anormal de factura |
| `ignore_abnormal_invoice_amount` | Boolean | Ignorar monto anormal de factura |
| `invoice_warn` | Selection | Advertencias de facturación |
| `invoice_warn_msg` | Text | Mensaje de advertencia de facturación |
| `invoice_sending_method` | Selection | Método de envío de facturas |
| `invoice_edi_format` | Selection (computed) | Formato de factura electrónica |
| `invoice_edi_format_store` | Char | Almacén del formato EDI |
| `display_invoice_edi_format` | Boolean | Mostrar formato EDI |
| `invoice_template_pdf_report_id` | Many2one | Plantilla de reporte PDF |
| `display_invoice_template_pdf_report_id` | Boolean | Mostrar plantilla PDF |
| `supplier_rank` | Integer | Ranking como proveedor | Es 1 si es Proveedor | Es 2 si es Fabricante (Samsung, etc.)
| `customer_rank` | Integer | Ranking como cliente | Es 1 si es Cliente
| `autopost_bills` | Selection | Auto-contabilizar facturas |
| `duplicated_bank_account_partners_count` | Integer (computed) | Contador de partners con cuentas duplicadas |
| `is_coa_installed` | Boolean | Plan contable instalado (DEPRECATED) |
| `property_outbound_payment_method_line_id` | Many2one | Método de pago saliente preferido |
| `property_inbound_payment_method_line_id` | Many2one | Método de pago entrante preferido |

### Módulo: sale
**Archivo:** `addons/sale/models/res_partner.py`

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `sale_order_count` | Integer (computed) | Contador de órdenes de venta |
| `sale_order_ids` | One2many | Órdenes de venta |
| `sale_warn` | Selection | Advertencias de ventas |
| `sale_warn_msg` | Text | Mensaje de advertencia de ventas |

### Módulo: purchase
**Archivo:** `addons/purchase/models/res_partner.py`

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `property_purchase_currency_id` | Many2one | Moneda del proveedor |
| `purchase_order_count` | Integer (computed) | Contador de órdenes de compra |
| `purchase_warn` | Selection | Advertencias de compras |
| `purchase_warn_msg` | Text | Mensaje de advertencia de compras |
| `receipt_reminder_email` | Boolean | Recordatorio de recepción por email |
| `reminder_date_before_receipt` | Integer | Días antes de la recepción |

### Módulo: crm
**Archivo:** `addons/crm/models/res_partner.py`

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `opportunity_ids` | One2many | Oportunidades |
| `opportunity_count` | Integer (computed) | Contador de oportunidades |

### Módulo: stock
**Archivo:** `addons/stock/models/res_partner.py`

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `property_stock_customer` | Many2one | Ubicación del cliente |
| `property_stock_supplier` | Many2one | Ubicación del proveedor |
| `picking_warn` | Selection | Advertencias de picking |
| `picking_warn_msg` | Text | Mensaje de advertencia de picking |

### Módulo: project
**Archivo:** `addons/project/models/res_partner.py`

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `project_ids` | One2many | Proyectos |
| `task_ids` | One2many | Tareas |
| `task_count` | Integer (computed) | Contador de tareas |

### Módulo: mail
**Archivo:** `addons/mail/models/res_partner.py`

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `contact_address_inline` | Char (computed) | Dirección completa en línea (para tracking) |
| `starred_message_ids` | Many2many | Mensajes destacados |

**Nota:** El módulo mail también agrega tracking a campos existentes como `name`, `email`, `phone`, `parent_id`, `user_id`, `vat`.

### Módulo: website
**Archivo:** `addons/website/models/res_partner.py`

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `visitor_ids` | One2many | Visitantes del sitio web |

**Herencias adicionales:** `website.published.multi.mixin`

### Módulo: fleet
**Archivo:** `addons/fleet/models/res_partner.py`

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `plan_to_change_car` | Boolean | Planea cambiar de auto |
| `plan_to_change_bike` | Boolean | Planea cambiar de moto |

### Módulo: portal
**Archivo:** `addons/portal/models/res_partner.py`

**Métodos agregados:**
- `_can_edit_name()`: Determina si se puede editar el nombre
- `can_edit_vat()`: Determina si se puede editar el VAT

### Módulo: base_vat
**Archivo:** `addons/base_vat/models/res_partner.py`

Agrega validaciones y métodos para el campo VAT existente, incluyendo validaciones por país.

### Módulo: sms
**Archivo:** `addons/sms/models/res_partner.py`

**Herencias adicionales:** `mail.thread.phone`

### Módulo: bus
**Archivo:** `addons/bus/models/res_partner.py`

**Herencias adicionales:** `bus.listener.mixin`

### Módulo: point_of_sale
**Archivo:** `addons/point_of_sale/models/res_partner.py`

**Herencias adicionales:** `pos.load.mixin`

### Otros Módulos con Extensiones Menores

- **calendar**: Agrega funcionalidades de calendario
- **event**: Agrega campos relacionados con eventos
- **loyalty**: Agrega campos de programas de lealtad
- **survey**: Agrega campos relacionados con encuestas
- **delivery**: Agrega campos de métodos de entrega
- **payment**: Agrega campos de métodos de pago
- **mass_mailing**: Agrega campos de marketing masivo
- **website_sale**: Agrega campos de comercio electrónico
- **contacts**: Mejoras en la gestión de contactos
- **hr**: Agrega campos relacionados con recursos humanos
- **product**: Agrega relaciones con productos

### Módulos de Localización

Múltiples módulos de localización (`l10n_*`) agregan campos específicos por país:
- **l10n_pe**: Campos específicos para Perú
- **l10n_ar**: Campos específicos para Argentina  
- **l10n_mx**: Campos específicos para México
- **l10n_co**: Campos específicos para Colombia
- **l10n_cl**: Campos específicos para Chile
- Y muchos otros países...

---

## Campos Agregados por Módulos OCA

### Módulo: partner_contact_role
**Archivo:** `extra-addons/OCA/partner-contact/partner_contact_role/models/res_partner.py`

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `role_ids` | Many2many | Roles del contacto (res.partner.role) |

### Módulo: partner_contact_gender
**Archivo:** `extra-addons/OCA/partner-contact/partner_contact_gender/models/res_partner.py`

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `gender` | Selection | Género: 'male', 'female', 'other' |

### Módulo: helpdesk_portal_restriction
**Archivo:** `extra-addons/OCA/helpdesk/helpdesk_portal_restriction/models/res_partner.py`

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `helpdesk_team_ids` | Many2many | Equipos de helpdesk disponibles |
| `helpdesk_category_ids` | Many2many | Categorías de helpdesk disponibles |

### Módulo: partner_fax
**Archivo:** `extra-addons/OCA/partner-contact/partner_fax/`

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `fax` | Char | Número de fax |

### Módulo: partner_multi_relation
**Archivo:** `extra-addons/OCA/partner-contact/partner_multi_relation/`

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `relation_count` | Integer | Contador de relaciones |
| `relation_all_ids` | One2many | Todas las relaciones del partner |

### Módulo: base_location_nuts
**Archivo:** `extra-addons/OCA/partner-contact/base_location_nuts/models/res_partner.py`

Extiende funcionalidades de localización NUTS (Nomenclature of Territorial Units for Statistics).

### Módulo: partner_company_type
**Archivo:** `extra-addons/OCA/partner-contact/partner_company_type/`

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `partner_company_type_id` | Many2one | Tipo de empresa específico |

### Módulo: sale_partner_company_group
**Archivo:** `extra-addons/OCA/partner-contact/sale_partner_company_group/`

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `company_group_id` | Many2one | Grupo de empresas |

### Módulo: partner_ref_unique
**Archivo:** `extra-addons/OCA/partner-contact/partner_ref_unique/`

Agrega validación de unicidad al campo `ref` según configuración de empresa.

### Módulo: partner_pricelist_search
**Archivo:** `extra-addons/OCA/partner-contact/partner_pricelist_search/`

Mejora la búsqueda por lista de precios en partners.

---

## Notas Importantes

### Campos de Dirección Estándar
Los campos de dirección definidos en `ADDRESS_FIELDS` son:
- `street`, `street2`, `zip`, `city`, `state_id`, `country_id`

### Campos Comerciales Estándar
Los campos comerciales que se sincronizan son:
- `vat`, `company_registry`, `industry_id`

### Contextos Especiales
- `show_address`: Incluye dirección en display_name
- `show_email`: Incluye email en display_name
- `show_vat`: Incluye VAT en display_name
- `partner_show_db_id`: Incluye ID en display_name
- `address_inline`: Muestra dirección en una línea

### Consideraciones de Rendimiento
- Los campos computados pueden ser costosos con muchos registros
- La sincronización automática puede generar escrituras en cascada
- Las búsquedas por lista de precios pueden ser lentas con muchos partners

---

*Documentación generada para Odoo 18 Community Edition*
*Última actualización: Enero 2025*