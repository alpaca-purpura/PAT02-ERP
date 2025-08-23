## 1. Filosofía Principal: El Código es la Única Fuente de Verdad

-   **Prohibido Configuraciones Manuales:** Cualquier elemento que pueda ser creado o modificado desde la interfaz de Odoo y que sea parte de la lógica de la aplicación, **DEBE** estar definido en un archivo de código (XML, CSV, PY). Se prohíbe explícitamente cualquier configuración directa en la interfaz de Odoo en los entornos de `staging` y `producción`.
-   **Separación de Datos:**
    -   El directorio `data/` se usa **exclusivamente** para datos iniciales y obligatorios para el funcionamiento del módulo (ej: secuencias, plantillas de correo base, configuraciones por defecto).
    -   El directorio `demo/` se usa **exclusivamente** para datos de demostración o de prueba que facilitan la validación del módulo. Estos datos no deben cargarse en producción.

## 2. Estructura del Módulo: La Base de Todo

-   **Estructura de Directorios Estándar:** Al crear un nuevo módulo, el agente debe generar y mantener la siguiente estructura de directorios completa, incluso si algunos directorios permanecen vacíos.
    ```
    mi_modulo/
    ├── __init__.py
    ├── __manifest__.py
    ├── controllers/
    │   ├── __init__.py
    │   └── main.py
    ├── data/
    │   └── mi_modelo_data.xml
    ├── demo/
    │   └── mi_modelo_demo.xml
    ├── i18n/
    │   └── es_PE.po
    ├── models/
    │   ├── __init__.py
    │   └── mi_modelo.py
    ├── security/
    │   ├── ir.model.access.csv
    │   └── security_rules.xml
    ├── static/
    │   └── src/
    │       ├── js/
    │       ├── css/
    │       └── xml/
    ├── views/
    │   ├── mi_modelo_views.xml
    │   └── menus.xml
    └── wizards/
        ├── __init__.py
        └── mi_wizard.py
    ```
-   **`__manifest__.py` Completo:** El manifiesto debe estar siempre actualizado, declarando explícitamente todas las `depends` para asegurar la correcta carga de los módulos.
-   **Inicialización Correcta:** Cada directorio que contenga código Python (`models`, `controllers`, `wizards`) debe tener un archivo `__init__.py` que importe los archivos `.py` de ese directorio.

## 3. Modelos (Python y ORM): El Corazón Lógico

-   **Un Modelo por Archivo:** Cada modelo principal debe estar en su propio archivo Python (e.g., `res_partner.py` para extender `res.partner`).
-   **Nombres Técnicos:** Los nombres de los campos deben ser en inglés y seguir la convención `snake_case`. Sufijos: `_id` para `Many2one`, `_ids` para `One2many` y `Many2many`.
-   **API Decorators:** Todos los métodos deben usar el decorador de API apropiado: `@api.model`, `@api.model_create_multi`, `@api.constrains`, `@api.onchange`, `@api.depends`.
-   **ORM sobre SQL Directo:** Se debe usar siempre el ORM de Odoo. Si una consulta SQL es inevitable por rendimiento, debe usarse `self.env.cr.execute()` con parámetros de tupla para prevenir inyección SQL y debe incluir un comentario explicando la justificación.
-   **Evitar `sudo()`:** Utilizar `sudo()` solo cuando sea estrictamente necesario y con el alcance más limitado posible (ej: `self.sudo().action_confirm()` es incorrecto; `record.sudo().write(...)` es mejor). Comentar siempre por qué se escalan privilegios.
-   **Extender, no Modificar:** Extender siempre modelos/métodos en lugar de modificar directamente el core de Odoo. Nunca editar archivos en `odoo/addons`.

## 4. Vistas y Datos (XML): El Código sobre la Interfaz

-   **Todo en XML:**
    -   **Vistas (`ir.ui.view`):** Todas las vistas y sus herencias deben estar en archivos XML. Prohibido usar Odoo Studio o "Editar Vista" en entornos de desarrollo que irán a producción.
    -   **Acciones (`ir.actions.act_window`, `ir.actions.server`):** Definirlas siempre en XML.
    -   **Menús (`<menuitem>`):** Siempre en un archivo XML dedicado, usualmente `views/menus.xml`.
    -   **Parámetros del Sistema (`ir.config_parameter`):** Usar para configuraciones dinámicas. No hardcodear valores como correos, contraseñas, tokens o rutas.
-   **IDs Externos Únicos:** Definir siempre un `id` explícito para cada registro en XML. La convención es `nombre_modulo.id_del_registro`.
-   **Herencia con XPath:** Para modificar vistas existentes, utilizar siempre `<xpath expr="..." position="...">` con la expresión más específica posible.

## 5. Seguridad

-   **`ir.model.access.csv` Obligatorio:** Nunca dejar un modelo sin sus reglas de acceso definidas en este archivo. Cada línea debe tener un ID único (e.g., `access_mi_modelo_user`).
-   **Reglas de Registro (`Record Rules`):** Para seguridad a nivel de fila, definir `ir.rule` en un archivo XML de seguridad (`security/security_rules.xml`).

## 6. Calidad de Código y Herramientas

-   **Estilo de Código:** Seguir estrictamente **PEP8** y las convenciones de Odoo. Se recomienda configurar herramientas como `black` (formateador) y `flake8` con `pylint-odoo` (linter).
-   **Logging:** Usar siempre `_logger` para registrar información, advertencias y errores. No usar `print()`.
-   **Documentación:** Documentar la lógica de negocio compleja en el código y usar `docstrings` para describir lo que hacen los métodos.
-   **Tests:** Para lógica de negocio compleja, crear tests unitarios en el directorio `tests/` para asegurar la estabilidad a largo plazo.

## 7. Modularidad y Dependencias

-   **Módulos Atómicos:** Cada `feature` debe estar en un módulo separado. No crear “mega módulos”.
-   **Nomenclatura de Módulos:** Usar prefijos para los módulos personalizados para evitar conflictos con módulos de la comunidad o del core (e.g., `custom_sales`, `custom_hr_payroll`).
-   **Dependencias Externas:** Toda librería externa de Python debe ser declarada en un archivo `requirements.txt` en la raíz del proyecto.

## 8. Entornos, Versionamiento y Despliegues

-   **Entornos Separados:** Mantener una estricta separación de entornos:
    -   `dev`: Para desarrollo y pruebas locales.
    -   `staging`: Copia de producción para validar despliegues.
    -   `prod`: Entorno real del cliente. Nunca desarrollar directamente en producción.
-   **Versionamiento (Git):** Usar un flujo de ramas claro:
    -   `main`: Código estable que está en producción.
    -   `feature/*`: Para cada nueva funcionalidad.
    -   `hotfix/*`: Para arreglos urgentes en producción.
-   **Proceso de Despliegue:**
    1.  **Prueba de Instalación:** Antes de liberar, probar una instalación limpia con `-i <modulo>`.
    2.  **Prueba de Actualización:** En `staging`, probar la actualización con `-u <modulo>`.
    3.  **Backup Obligatorio:** Realizar un **backup completo** de la base de datos y del filestore antes de cada despliegue a producción.
    4.  Desplegar en producción actualizando los módulos correspondientes.

## 9. Migraciones de Datos

-   **Hooks para Transformaciones:** Para transformaciones de datos complejas entre versiones (ej: renombrar un campo, mover datos), usar `post_init_hook` o `pre_init_hook` en el `__manifest__.py`.
-   **Scripts Versionados:** Nunca ejecutar scripts SQL directamente en producción sin que estén versionados y probados.