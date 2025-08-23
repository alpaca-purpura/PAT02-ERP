# PATCO Core

## Descripción

Módulo base con configuraciones y dependencias comunes de PATCO. Este módulo proporciona la funcionalidad básica para la clasificación operacional de servicios en tickets de helpdesk y órdenes de servicio de campo.

## Características

### Modelos de Clasificación
- **Naturaleza del Servicio** (`patco.service.nature`): Define los tipos de naturaleza de los servicios
- **Área del Servicio** (`patco.service.area`): Define las áreas operacionales de los servicios
- **Complejidad del Servicio** (`patco.service.complexity`): Define los niveles de complejidad de los servicios

### Funcionalidades
- Clasificación automática de códigos basada en naturaleza, área y complejidad
- Validación de completitud de clasificación antes de pasar a etapas en progreso
- Integración con módulos de Helpdesk Management y Field Service
- Campos personalizados en tickets de helpdesk y órdenes FSM

## Dependencias

### Módulos Odoo Standard
- `base`: Funcionalidades básicas de Odoo
- `sale_management`: Gestión de ventas

### Módulos OCA
- `fieldservice`: Gestión de servicios de campo
- `helpdesk_mgmt`: Gestión de helpdesk
- `web_responsive`: Interfaz responsiva

## Instalación

1. Asegúrate de tener instalados todos los módulos de dependencia
2. Copia el módulo en tu directorio de addons
3. Actualiza la lista de módulos en Odoo
4. Instala el módulo `patco_core`

## Configuración

### Datos Iniciales
El módulo incluye datos iniciales para:
- Naturalezas de servicio predefinidas
- Áreas de servicio predefinidas
- Complejidades de servicio predefinidas

### Menús de Configuración
Accede a la configuración a través de:
- **Configuración > Naturaleza del Servicio**
- **Configuración > Área del Servicio**
- **Configuración > Complejidad del Servicio**

## Uso

### En Tickets de Helpdesk
1. Abre un ticket de helpdesk
2. Ve a la pestaña "Clasificación Operacional"
3. Selecciona la naturaleza, área y complejidad
4. El código de clasificación se generará automáticamente

### En Órdenes de Servicio de Campo
1. Abre una orden FSM
2. En la pestaña "Info", encuentra la sección "Clasificación Operacional"
3. Selecciona la naturaleza, área y complejidad
4. El código de clasificación se generará automáticamente

## Validaciones

- Los campos de naturaleza, área y complejidad son obligatorios antes de mover un ticket o orden a una etapa "en progreso"
- Los códigos de naturaleza, área y complejidad deben ser únicos
- Los nombres de naturaleza, área y complejidad deben ser únicos

## Estructura de Archivos

```
patco_core/
├── __init__.py
├── __manifest__.py
├── README.md
├── data/
│   ├── patco_core_data.xml
│   ├── patco_service_nature_data.xml
│   ├── patco_service_area_data.xml
│   └── patco_service_complexity_data.xml
├── i18n/
│   └── es_PE.po
├── models/
│   ├── __init__.py
│   ├── patco_service_nature.py
│   ├── patco_service_area.py
│   ├── patco_service_complexity.py
│   └── service_order_classification.py
├── security/
│   ├── ir.model.access.csv
│   └── patco_security.xml
├── static/
│   ├── description/
│   └── src/
└── views/
    ├── patco_service_nature_views.xml
    ├── patco_service_area_views.xml
    ├── patco_service_complexity_views.xml
    ├── service_order_views.xml
    └── patco_menus.xml
```

## Compatibilidad

- **Versión de Odoo**: 18.0
- **Licencia**: LGPL-3
- **Estado**: Estable

## Soporte

Para soporte técnico, contacta al equipo de desarrollo de PATCO.

## Changelog

### v18.0.1.0.0
- Versión inicial para Odoo 18.0
- Modelos de clasificación operacional
- Integración con helpdesk_mgmt y fieldservice
- Validaciones de completitud
- Datos iniciales y traducciones en español peruano