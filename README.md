# Odoo PATCO - Sistema ERP


## Descripción

Sistema ERP basado en Odoo Community 18 para **PACIFIC ALLIANCE TRADING COMPANY SAC**, empresa peruana dedicada al servicio de mantenimiento de maquinaria para la industria hotelera y gastronómica.

## Características

- **Odoo Community 18**: Sistema ERP completo
- **PostgreSQL 15**: Base de datos robusta y confiable
- **Docker Compose**: Despliegue simple y estandarizado
- **Configuración centralizada**: Todas las contraseñas en archivo `.env`
- **Volúmenes persistentes**: Datos seguros y respaldados

## Estructura del Proyecto

```
odoo-patco/
├── docker-compose.yml     # Configuración de servicios
├── .env                   # Variables de entorno (NO subir a git)
├── .env.example          # Plantilla de configuración
├── config/
│   └── odoo.conf         # Configuración de Odoo
├── addons/               # Módulos personalizados
└── README.md            # Este archivo
```

## Requisitos Previos

- Docker Desktop instalado
- Docker Compose v3.8 o superior
- Puerto 8069 disponible

## Instalación y Configuración


### Desplegar los Servicios

Clonar el repositorio. Ir a la carpeta raiz, donde se encuentra el archivo docker-compose.yml

```bash
# Iniciar los servicios en segundo plano
docker-compose up -d

# Verificar que los servicios estén ejecutándose
docker-compose ps

# Ver los logs en tiempo real
docker-compose logs -f
```

### Acceder a Odoo

- **URL**: http://localhost:8069

## Configuración Inicial
Todo ha sido programado por lo que el proceso manual es mínimo y es el siguiente:
1. Ejecutar desde docker compose.
2. Ingresar con usuario administrador, y a Facturacion/Ajustes y cambiar la localización fiscal a Perú, Guardar.
3. Instalar patco_auto_install

## Comandos Útiles

### Gestión de Servicios

```bash
# Iniciar servicios
docker-compose up -d

# Detener servicios
docker-compose down

# Reiniciar servicios
docker-compose restart

# Ver estado de servicios
docker-compose ps

# Ver logs
docker-compose logs -f
```

### Gestión de Datos

```bash
# Backup de la base de datos
docker-compose exec db pg_dump -U odoo odoo_patco > backup_$(date +%Y%m%d_%H%M%S).sql

# Restaurar base de datos
docker-compose exec -T db psql -U odoo odoo_patco < backup_file.sql

# Acceder a la base de datos
docker-compose exec db psql -U odoo -d odoo_patco
```


## Módulos del Sistema

El sistema incluirá los siguientes módulos personalizados:

- **Gestión de Proyectos**: Servicios de mantenimiento
- **Gestión de Clientes**: Empresas hoteleras y gastronómicas
- **Gestión de Activos**: Maquinaria y equipos
- **Gestión de Facturación**: Ventas y cobranza
- **Agente IA**: Asistente para técnicos vía Telegram

## Seguridad

### Recomendaciones

1. **Cambiar contraseñas por defecto** antes del despliegue
3. **Usar contraseñas seguras** (mínimo 12 caracteres)
4. **Configurar firewall** para limitar acceso al puerto 8069
5. **Realizar backups regulares** de la base de datos

### Archivo .gitignore

Asegúrate de que el archivo `.gitignore` incluya:

```
.env
*.log
__pycache__/
*.pyc
```

## Solución de Problemas

### Problemas Comunes

1. **Puerto 8069 ocupado**:
   ```bash
   # Cambiar puerto en docker-compose.yml
   ports:
     - "8070:8069"  # Usar puerto 8070
   ```

2. **Error de conexión a base de datos**:
   ```bash
   # Verificar que PostgreSQL esté ejecutándose
   docker-compose logs db
   
   # Reiniciar servicios
   docker-compose down && docker-compose up -d
   ```

3. **Problemas de permisos**:
   ```bash
   # En Linux/Mac, ajustar permisos
   sudo chown -R 101:101 ./config
   sudo chown -R 101:101 ./addons
   ```

4. **Problema de assets corruptos (CSS)
   ```bash
      # En Linux/Mac, ajustar permisos
   # 1. Limpiar assets corruptos
   docker-compose exec db psql -U odoo -d odoo_patco -c "DELETE FROM ir_attachment WHERE res_model = 'ir.ui.view' AND (name ILIKE '%.assets_%.css' OR name ILIKE '%.assets_%.js');"

   # 2. Reiniciar Odoo
   docker-compose restart odoo
   ```
5. actualizaciones de los modulos, si hay cambios
   ```bash
   # Actualizar módulos
   docker-compose exec odoo odoo-bin -u all -d odoo-patco
   ```

### Logs y Diagnóstico

```bash
# Ver logs detallados
docker-compose logs --tail=100 -f

# Acceder al contenedor de Odoo
docker-compose exec odoo bash

# Verificar configuración
docker-compose exec odoo cat /etc/odoo/odoo.conf
```

**Nota**: Este es un sistema en desarrollo. Para producción, considerar configuraciones adicionales de seguridad, SSL/TLS, y monitoreo.