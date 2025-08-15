## Estructura de Directorios Recomendada

```
odoo-patco/
├── extra-addons/
│   ├── OCA/                    # Módulos de la Odoo Community Association
│   │   ├── web/               # Módulos web de OCA
│   │   ├── account/           # Módulos contables de OCA
│   │   ├── project/           # Módulos de proyectos de OCA
│   │   └── ...
│   ├── Alpaca/                # Módulos desarrollados internamente
│   │   ├── patco_maintenance/ # Módulo de mantenimiento personalizado
│   │   ├── patco_projects/    # Módulo de proyectos personalizado
│   │   ├── patco_telegram/    # Integración con Telegram
│   │   └── ...
│   └── third_party/           # Módulos de terceros (opcional)
├── addons/                    # Módulos core de Odoo (NO MODIFICAR)
├── config/
│   └── odoo.conf
├── docker-compose.yml
└── ...
```

## Configuración de Addons Path

En el archivo `config/odoo.conf`, el `addons_path` está configurado correctamente:
```ini
addons_path = /opt/odoo/addons,/mnt/extra-addons/
```

Esto le dice a Odoo que busque módulos en:
1. `/opt/odoo/addons` - Módulos core de Odoo
2. `/mnt/extra-addons/` - Módulos personalizados (mapeado desde `./extra-addons`)

## Mejores Prácticas para Desarrollo

### 1. Organización de Módulos

#### Carpeta OCA
- **Propósito**: Módulos de la Odoo Community Association
- **Estructura**: Organizar por categoría funcional
- **Actualización**: Usar git submodules o descargas directas

```bash
# Ejemplo de descarga de módulos OCA
cd extra-addons/OCA
git clone https://github.com/OCA/web.git
git clone https://github.com/OCA/project.git
```

#### Carpeta Alpaca
- **Propósito**: Desarrollos internos de PATCO
- **Nomenclatura**: Prefijo `patco_` para todos los módulos
- **Control de versiones**: Git con branches por funcionalidad

### 2. Estructura de un Módulo Personalizado

```
patco_maintenance/
├── __manifest__.py           # Manifiesto del módulo
├── __init__.py              # Inicialización
├── models/                  # Modelos de datos
│   ├── __init__.py
│   ├── maintenance_request.py
│   └── equipment.py
├── views/                   # Vistas XML
│   ├── maintenance_views.xml
│   └── equipment_views.xml
├── security/                # Permisos y seguridad
│   ├── ir.model.access.csv
│   └── security.xml
├── data/                    # Datos iniciales
│   └── maintenance_data.xml
├── static/                  # Archivos estáticos
│   ├── description/
│   │   ├── icon.png
│   │   └── index.html
│   ├── src/
│   │   ├── css/
│   │   ├── js/
│   │   └── xml/
├── wizard/                  # Asistentes
├── report/                  # Reportes
└── README.md               # Documentación del módulo
```

### 3. Ejemplo de __manifest__.py

```python
{
    'name': 'PATCO - Gestión de Mantenimiento',
    'version': '18.0.1.0.0',
    'category': 'Maintenance',
    'summary': 'Gestión especializada de mantenimiento para equipos hoteleros',
    'description': """
        Módulo personalizado para PACIFIC ALLIANCE TRADING COMPANY SAC
        que extiende las funcionalidades de mantenimiento de Odoo para
        adaptarse a las necesidades específicas del mantenimiento de
        maquinaria hotelera y gastronómica.
    """,
    'author': 'PATCO Development Team',
    'website': 'https://patco.pe',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'maintenance',
        'project',
        'hr',
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/maintenance_data.xml',
        'views/maintenance_views.xml',
        'views/equipment_views.xml',
    ],
    'demo': [
        'demo/maintenance_demo.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'patco_maintenance/static/src/css/maintenance.css',
            'patco_maintenance/static/src/js/maintenance.js',
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': True,
}
```

## Comandos Esenciales

### Reiniciar Servicios
```bash
# Detener servicios
docker-compose down

# Reconstruir y levantar servicios
docker-compose up --build -d

# Ver logs en tiempo real
docker-compose logs -f odoo
```

### Actualizar Lista de Apps
```bash
# Método 1: Desde la interfaz web
# Apps > Update Apps List

# Método 2: Desde línea de comandos
docker-compose exec odoo python3 /opt/odoo/odoo-bin -c /etc/odoo/odoo.conf -d odoo_patco --update-apps-list --stop-after-init

# Método 3: Instalar módulo específico
docker-compose exec odoo python3 /opt/odoo/odoo-bin -c /etc/odoo/odoo.conf -d odoo_patco -i patco_maintenance --stop-after-init
```

### Desarrollo y Debug
```bash
# Modo desarrollo con auto-reload
docker-compose exec odoo python3 /opt/odoo/odoo-bin -c /etc/odoo/odoo.conf -d odoo_patco --dev=reload,qweb,werkzeug,xml

# Actualizar módulo específico
docker-compose exec odoo python3 /opt/odoo/odoo-bin -c /etc/odoo/odoo.conf -d odoo_patco -u patco_maintenance --stop-after-init
```

## Diferencias entre Desarrollo (Windows) y Producción (Linux)

### Desarrollo en Windows 11

#### Ventajas:
- Docker Desktop con interfaz gráfica
- Integración con VS Code y herramientas de desarrollo
- Facilidad para debugging

#### Consideraciones:
- Rendimiento ligeramente inferior debido a la virtualización
- Paths con barras invertidas (\) vs barras normales (/)
- Posibles problemas de permisos con volúmenes

#### Configuración recomendada:
```yaml
# docker-compose.override.yml para desarrollo
version: '3.8'
services:
  odoo:
    command: [
      "python3", "/opt/odoo/odoo-bin", 
      "-c", "/etc/odoo/odoo.conf", 
      "--dev=reload,qweb,werkzeug,xml"
    ]
    ports:
      - "8069:8069"
      - "8072:8072"  # Puerto adicional para debugging
```

### Producción en Linux Ubuntu

#### Ventajas:
- Mejor rendimiento nativo
- Mayor estabilidad
- Menor consumo de recursos

#### Configuración recomendada:
```yaml
# docker-compose.prod.yml
version: '3.8'
services:
  odoo:
    restart: always
    environment:
      - ODOO_RC=/etc/odoo/odoo.conf
    deploy:
      resources:
        limits:
          memory: 2G
        reservations:
          memory: 1G
```

#### Script de despliegue:
```bash
#!/bin/bash
# deploy.sh
set -e

echo "Desplegando Odoo PATCO en producción..."

# Backup de base de datos
docker-compose exec db pg_dump -U odoo odoo_patco > backup_$(date +%Y%m%d_%H%M%S).sql

# Actualizar código
git pull origin main

# Reconstruir servicios
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up --build -d

# Verificar estado
docker-compose ps

echo "Despliegue completado exitosamente"
```

## Solución de Problemas Comunes

### 1. Módulos no aparecen en Apps
```bash
# Verificar mapeo de volúmenes
docker-compose exec odoo ls -la /mnt/extra-addons/

# Verificar permisos
docker-compose exec odoo find /mnt/extra-addons/ -name "__manifest__.py"

# Forzar actualización
docker-compose restart odoo
```

### 2. Errores de importación
```bash
# Verificar logs
docker-compose logs odoo | grep -i error

# Verificar sintaxis Python
docker-compose exec odoo python3 -m py_compile /mnt/extra-addons/Alpaca/patco_maintenance/__init__.py
```

### 3. Problemas de base de datos
```bash
# Reinicializar base de datos (CUIDADO: Borra todos los datos)
docker-compose down
docker volume rm odoo-patco-db-data
docker-compose up -d
```

## Checklist de Verificación

### Antes de desarrollar:
- [ ] `extra-addons/` existe y contiene las carpetas `OCA/` y `Alpaca/`
- [ ] `docker-compose.yml` mapea `./extra-addons:/mnt/extra-addons`
- [ ] `config/odoo.conf` incluye `/mnt/extra-addons/` en `addons_path`
- [ ] Servicios Docker están ejecutándose correctamente

### Antes de desplegar:
- [ ] Todos los módulos tienen `__manifest__.py` válido
- [ ] No hay errores de sintaxis en el código Python
- [ ] Las dependencias están correctamente declaradas
- [ ] Los archivos de seguridad (`ir.model.access.csv`) están completos
- [ ] Se ha probado la instalación en entorno de desarrollo
- [ ] Se ha realizado backup de la base de datos de producción

## Recursos Adicionales

- [Documentación oficial de Odoo](https://www.odoo.com/documentation/18.0/)
- [OCA Guidelines](https://github.com/OCA/odoo-community.org/blob/master/website/Contribution/CONTRIBUTING.rst)
- [Odoo Development Cookbook](https://www.packtpub.com/product/odoo-development-cookbook/)
- [Docker Compose Best Practices](https://docs.docker.com/compose/production/)