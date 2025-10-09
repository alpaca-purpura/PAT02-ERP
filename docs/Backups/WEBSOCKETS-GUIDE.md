# 🌐 Guía Completa de WebSockets - PATCO Suite Odoo 18

## 📋 Resumen Ejecutivo

Esta guía documenta la **solución definitiva** para problemas de websockets en Odoo 18 Community con Traefik, incluyendo scripts automatizados para prevenir y corregir problemas.

## 🎯 Problema Original

**Síntomas:**
- ❌ Mensaje "Se perdió la conexión en tiempo real..."
- 🔄 Necesidad de recargar página para ver respuestas de OdooBot
- 📝 Mensajes no aparecen automáticamente en chat
- 🚫 Errores `KeyError: 'socket'` y `RuntimeError: Couldn't bind the websocket`

## 🔍 Causa Raíz Identificada

### 1. **Problema de Routing (Principal)**
- Las conexiones `/websocket` iban al worker HTTP (puerto 8069)
- Necesitaban ir al worker longpolling (puerto 8072)
- **Solución:** Traefik con routing específico para websockets

### 2. **OdooBot Desactivado**
- Usuario OdooBot (ID: 1) estaba `active = false`
- **Solución:** `UPDATE res_users SET active = true WHERE id = 1;`

### 3. **Assets Corruptos**
- Archivo `websocket_worker_bundle` corrupto o faltante
- **Solución:** Eliminar assets corruptos y regenerar

## ✅ Solución Implementada

### 🌐 **Traefik Proxy Configuration**

```yaml
traefik:
  image: traefik:v3.0
  command:
    - --providers.docker=true
    - --entrypoints.web.address=:80
    - --entrypoints.websecure.address=:443
  ports:
    - "80:80"
    - "443:443"
    - "8080:8080"  # Dashboard
```

### 🔄 **Odoo WebSocket Routing**

```yaml
labels:
  # Router principal para Odoo
  - "traefik.http.routers.odoo-dev.rule=Host(`localhost`)"
  - "traefik.http.routers.odoo-dev.service=odoo-web-dev"
  
  # Router específico para websockets
  - "traefik.http.routers.odoo-websocket-dev.rule=Host(`localhost`) && PathPrefix(`/websocket`)"
  - "traefik.http.routers.odoo-websocket-dev.service=odoo-websocket-dev"
  
  # Servicios separados
  - "traefik.http.services.odoo-web-dev.loadbalancer.server.port=8069"
  - "traefik.http.services.odoo-websocket-dev.loadbalancer.server.port=8072"
```

### ⚙️ **Configuración Odoo (odoo.conf)**

```ini
[options]
workers = 2
longpolling_port = 8072
proxy_mode = True
xmlrpc_interface = 0.0.0.0
netrpc_interface = 0.0.0.0
```

## 🚀 Scripts Automatizados

### **Para Instalación Limpia:**
```powershell
# Windows
docker compose down -v
docker compose up -d
.\scripts\setup-websockets.ps1
```

```bash
# Linux
docker compose down -v
docker compose up -d
./scripts/fix-websockets.sh
```

### **Para Corrección de Problemas:**
```powershell
# Windows
.\scripts\fix-websockets.ps1
```

```bash
# Linux
./scripts/fix-websockets.sh
```

## 🔧 Flujo de Corrección Manual

Si prefieres ejecutar los comandos manualmente:

### 1. **Activar OdooBot**
```sql
docker exec odoo-patco-db psql -U odoo -d odoo_patco -c "UPDATE res_users SET active = true WHERE id = 1;"
```

### 2. **Limpiar Assets Corruptos**
```sql
docker exec odoo-patco-db psql -U odoo -d odoo_patco -c "DELETE FROM ir_attachment WHERE name LIKE '%websocket_worker_bundle%' OR name LIKE '%bus%';"
```

### 3. **Limpiar Archivos Físicos**
```bash
docker exec odoo-patco-app rm -rf /home/odoo/.local/share/Odoo/filestore/odoo_patco/48/
```

### 4. **Reiniciar y Regenerar**
```bash
docker restart odoo-patco-app
# Esperar 30 segundos
```

## 📊 Verificación de Estado

### **Verificar Evented Service:**
```bash
docker exec odoo-patco-app tail -n 20 /var/log/odoo/odoo.log | grep "Evented Service"
```
**Salida esperada:** `Evented Service (longpolling) running on 0.0.0.0:8072`

### **Verificar OdooBot:**
```sql
docker exec odoo-patco-db psql -U odoo -d odoo_patco -c "SELECT u.id, p.name, u.active FROM res_users u JOIN res_partner p ON u.partner_id = p.id WHERE u.id = 1;"
```
**Salida esperada:** `1 | OdooBot | t`

### **Verificar Traefik:**
- Dashboard: http://localhost:8080
- Debe mostrar servicios `odoo-web-dev` y `odoo-websocket-dev`

## 🌍 Migración a Producción

### **Cambios Necesarios en `docker-compose.prod.yml`:**

```yaml
labels:
  # Router principal
  - "traefik.http.routers.odoo.rule=Host(`tu-dominio.com`)"
  - "traefik.http.routers.odoo.entrypoints=websecure"
  - "traefik.http.routers.odoo.tls.certresolver=letsencrypt"
  - "traefik.http.routers.odoo.service=odoo-web"
  
  # Router websockets
  - "traefik.http.routers.odoo-websocket.rule=Host(`tu-dominio.com`) && PathPrefix(`/websocket`)"
  - "traefik.http.routers.odoo-websocket.entrypoints=websecure"
  - "traefik.http.routers.odoo-websocket.tls.certresolver=letsencrypt"
  - "traefik.http.routers.odoo-websocket.service=odoo-websocket"
  
  # Servicios
  - "traefik.http.services.odoo-web.loadbalancer.server.port=8069"
  - "traefik.http.services.odoo-websocket.loadbalancer.server.port=8072"
```

## 🛠️ Troubleshooting

### **Problema: Websockets no funcionan después de reinicio**
**Solución:** Ejecutar `.\scripts\fix-websockets.ps1`

### **Problema: OdooBot no responde**
**Verificar:** 
```sql
SELECT active FROM res_users WHERE id = 1;
```
**Corregir:** 
```sql
UPDATE res_users SET active = true WHERE id = 1;
```

### **Problema: Error FileNotFoundError en logs**
**Solución:** Limpiar assets y reiniciar:
```bash
docker exec odoo-patco-db psql -U odoo -d odoo_patco -c "DELETE FROM ir_attachment WHERE name LIKE '%websocket_worker_bundle%';"
docker restart odoo-patco-app
```

### **Problema: Traefik no redirige websockets**
**Verificar:** Dashboard en http://localhost:8080
**Buscar:** Servicios `odoo-websocket-dev` en la lista

## 📈 Beneficios de la Solución

### ✅ **Funcionalidad Completa**
- Chat en tiempo real sin recargar página
- OdooBot responde automáticamente
- Notificaciones push funcionando
- Actualizaciones de estado en vivo

### 🔧 **Mantenimiento Simplificado**
- Scripts automatizados para corrección
- Documentación completa
- Configuración versionada en Git
- Fácil migración entre entornos

### 🚀 **Escalabilidad**
- Configuración lista para producción
- Compatible con SSL/TLS
- Optimizado para múltiples workers
- Monitoreo con Traefik dashboard

## 📝 Notas Importantes

1. **Orden de ejecución:** Siempre ejecutar scripts después de `docker compose up -d`
2. **Tiempo de espera:** Los scripts incluyen esperas apropiadas para inicialización
3. **Idempotencia:** Todos los scripts se pueden ejecutar múltiples veces
4. **Compatibilidad:** Solución probada con Odoo 18 Community + Traefik v3.0
5. **Logs:** Los scripts limpian logs automáticamente para facilitar debugging

## 🎉 Resultado Final

**✅ WebSockets completamente funcionales**
**✅ Chat en tiempo real**
**✅ OdooBot respondiendo automáticamente**
**✅ Sin errores en logs**
**✅ Configuración documentada y automatizada**

---

*Esta guía documenta la solución definitiva implementada en septiembre 2025 para PATCO Suite Odoo 18.*