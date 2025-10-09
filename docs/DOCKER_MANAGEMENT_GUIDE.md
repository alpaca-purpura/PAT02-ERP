# 🐳 Guía de Gestión Docker - Proyecto PATCO

## 📋 Resumen del Problema y Solución

### ❌ Problema Identificado
Cuando ejecutas `docker compose down`, algunos contenedores no se detienen porque:

1. **Servicios con perfiles específicos**: Los servicios con `profiles` (como `ai-setup`, `office-services`) no se incluyen en el comando básico `docker compose down`
2. **Contenedores huérfanos**: Contenedores que se ejecutaron con perfiles específicos quedan "huérfanos" y no se gestionan con comandos básicos
3. **Red en uso**: La red `odoo-patco-network` permanece activa mientras haya contenedores conectados a ella
4. **⚠️ NUEVO PROBLEMA**: Error "Resource is still in use" al intentar eliminar la red

### ✅ Solución Implementada
Para detener TODOS los servicios correctamente, debes usar comandos específicos según el perfil.

### 🔧 Solución para "Resource is still in use"
**Causa**: Contenedores individuales pueden quedar conectados a la red sin aparecer en `docker ps`, especialmente servicios IA que se ejecutan con perfiles específicos.

**Solución**: Usar `docker network inspect` para identificar contenedores conectados y eliminarlos manualmente antes de eliminar la red.

## Cuando quieras resetear completamente el entorno, usa esta secuencia:
```bash
# 1. Detener todos los perfiles
docker compose --profile ai-setup --profile office-services down -v

# 2. Si la red sigue en uso, inspeccionarla
docker network inspect odoo-patco-network

# 3. Eliminar contenedores conectados manualmente
docker stop [nombre-contenedor]
docker rm [nombre-contenedor]

# 4. Eliminar la red
docker network rm odoo-patco-network

# 5. Reiniciar desde cero
docker compose up -d
```

## 🚀 Comandos de Gestión por Perfiles

### 1. **Servicios Básicos** (Odoo + PostgreSQL)
```bash
# Iniciar servicios básicos
docker compose up -d

# Detener servicios básicos
docker compose down

# Detener y eliminar volúmenes
docker compose down -v
```

### 2. **Servicios IA de Configuración** (Perfil: ai-setup)
```bash
# Iniciar servicios de configuración IA
docker compose --profile ai-setup up -d

# Detener servicios de configuración IA
docker compose --profile ai-setup down

# Detener y eliminar volúmenes
docker compose --profile ai-setup down -v
```

### 3. **Servicios de Oficina** (Perfil: office-services)
```bash
# Iniciar OnlyOffice Document Server
docker compose --profile office-services up -d

# Detener OnlyOffice Document Server
docker compose --profile office-services down

# Detener y eliminar volúmenes
docker compose --profile office-services down -v
```

### 4. **TODOS los Servicios** (Comando Universal)
```bash
# Iniciar TODOS los servicios
docker compose --profile ai-setup --profile office-services up -d

# Detener TODOS los servicios
docker compose --profile ai-setup --profile office-services down

# Detener TODOS y eliminar volúmenes
docker compose --profile ai-setup --profile office-services down -v
```

---

## 🔧 Comandos de Limpieza Completa

### Método 1: Limpieza por Perfiles
```bash
# Detener todos los perfiles
docker compose --profile ai-setup --profile office-services down -v

# Verificar que no queden contenedores
docker ps -a

# Limpiar contenedores huérfanos
docker container prune -f
```

### Método 2: Limpieza Manual (Método Usado)
```bash
# 1. Identificar contenedores activos
docker ps -a

# 2. Detener contenedores específicos
docker stop patco-document-indexer patco-mcp-server patco-onlyoffice-documentserver patco-onlyoffice-rabbitmq

# 3. Eliminar contenedores
docker rm patco-document-indexer patco-mcp-server patco-onlyoffice-documentserver patco-onlyoffice-rabbitmq

# 4. Eliminar red
docker network rm odoo-patco-network

# 5. Limpiar recursos no utilizados
docker system prune -f
```

### Método 2.1: Solución para Red "Resource is still in use"
```bash
# ⚠️ PROBLEMA: La red odoo-patco-network no se elimina con "Resource is still in use"
# ✅ SOLUCIÓN: Identificar y eliminar contenedores conectados manualmente

# 1. Inspeccionar qué contenedores están usando la red
docker network inspect odoo-patco-network

# 2. Identificar contenedores en la sección "Containers" del output
# Ejemplo: "patco-document-indexer" aparece conectado

# 3. Detener el contenedor específico
docker stop patco-document-indexer

# 4. Eliminar el contenedor
docker rm patco-document-indexer

# 5. Ahora eliminar la red
docker network rm odoo-patco-network

# 6. Verificar que la red fue eliminada
docker network ls | grep odoo-patco
```

### Método 3: Limpieza Nuclear (Último Recurso)
```bash
# ⚠️ CUIDADO: Esto elimina TODOS los contenedores y redes
docker stop $(docker ps -aq)
docker rm $(docker ps -aq)
docker network prune -f
docker volume prune -f
docker system prune -af
```

---

## 📊 Servicios del Proyecto PATCO

### Servicios Básicos (Sin perfil)
- `db` → `odoo-patco-db` (PostgreSQL 15)
- `odoo` → `odoo-patco-app` (Odoo Community 18)

### Servicios IA - Configuración (Perfil: ai-setup)
- `pgvector-setup` → `patco-pgvector-setup`
- `ai-services-validator` → `patco-ai-validator`

### Servicios IA - Producción (Sin perfil específico)
- `document-indexer` → `patco-document-indexer`
- `mcp-server` → `patco-mcp-server`
- `langgraph-server` → `patco-langgraph-server`

### Servicios de Oficina (Perfil: office-services)
- `onlyoffice-documentserver` → `patco-onlyoffice-documentserver`
- `onlyoffice-rabbitmq` → `patco-onlyoffice-rabbitmq`

---

## 🌐 Gestión de Redes

### Red Principal
- **Nombre**: `odoo-patco-network`
- **Tipo**: Bridge
- **Propósito**: Comunicación entre todos los servicios PATCO

### Verificar Estado de Red
```bash
# Listar redes
docker network ls

# Inspeccionar red específica
docker network inspect odoo-patco-network

# Ver qué contenedores están conectados
docker network inspect odoo-patco-network | grep -A 10 "Containers"
```

---

## 📦 Gestión de Volúmenes

### Volúmenes del Proyecto
```bash
# Listar volúmenes PATCO
docker volume ls | grep patco

# Volúmenes principales:
# - odoo-patco-web-data (datos web Odoo)
# - odoo-patco-db-data (base de datos PostgreSQL)
# - patco-onlyoffice-* (datos OnlyOffice)
```

### Limpieza de Volúmenes
```bash
# Eliminar volúmenes específicos
docker volume rm odoo-patco-web-data odoo-patco-db-data

# Eliminar todos los volúmenes no utilizados
docker volume prune -f
```

---

## 🚨 Comandos de Emergencia

### Verificar Estado General
```bash
# Ver todos los contenedores
docker ps -a

# Ver uso de recursos
docker stats

# Ver logs de un servicio específico
docker compose logs odoo
docker compose logs db
```

### Reinicio Completo del Proyecto
```bash
# 1. Detener todo
docker compose --profile ai-setup --profile office-services down -v

# 2. Limpiar contenedores huérfanos
docker container prune -f

# 3. Limpiar redes no utilizadas
docker network prune -f

# 4. Iniciar servicios básicos
docker compose up -d

# 5. Iniciar servicios adicionales si es necesario
docker compose --profile office-services up -d
```

---

## 📝 Notas para Producción

### Diferencias Clave
1. **Archivo de configuración**: Usar `docker-compose.prod.yml` en producción
2. **Proxy reverso**: Traefik configurado para HTTPS automático
3. **Variables de entorno**: Archivo `.env` con credenciales seguras
4. **Volúmenes**: Rutas absolutas en el servidor de producción
5. **Redes**: Configuración de red externa para Traefik

### Comando de Producción
```bash
# Producción con Traefik
docker compose -f docker-compose.prod.yml up -d

# Detener producción
docker compose -f docker-compose.prod.yml down
```

---

## ✅ Checklist de Verificación

### Antes de Desplegar
- [ ] Todos los servicios básicos funcionan: `docker compose up -d`
- [ ] Los logs no muestran errores: `docker compose logs`
- [ ] La red está correctamente configurada: `docker network inspect odoo-patco-network`
- [ ] Los volúmenes persisten datos: `docker volume ls | grep patco`

### Después de Cambios
- [ ] Detener servicios correctamente con perfiles
- [ ] Verificar que no queden contenedores huérfanos: `docker ps -a`
- [ ] Limpiar recursos no utilizados: `docker system prune -f`
- [ ] Probar reinicio completo del stack

---

**🎯 Comando Recomendado para Desarrollo Diario:**
```bash
# Detener todo correctamente
docker compose --profile ai-setup --profile office-services down

# Iniciar servicios básicos
docker compose up -d

# Iniciar servicios adicionales según necesidad
docker compose --profile office-services up -d
```