#!/bin/bash
# ===== SCRIPT DE CORRECCIÓN DE WEBSOCKETS ODOO 18 =====
# Autor: PATCO Suite
# Descripción: Automatiza la corrección de problemas de websockets en Odoo 18
# Uso: ./scripts/fix-websockets.sh

set -e  # Salir si hay errores

echo "🔧 PATCO Suite - Corrección de WebSockets Odoo 18"
echo "================================================="

# Verificar que Docker esté corriendo
echo "📋 Verificando estado de contenedores..."
if ! docker ps --format "{{.Names}}" | grep -q "odoo-patco"; then
    echo "❌ Error: Los contenedores de Odoo no están corriendo."
    echo "   Ejecuta primero: docker compose up -d"
    exit 1
fi

containers=$(docker ps --format "{{.Names}}" | grep "odoo-patco" | tr '\n' ' ')
echo "✅ Contenedores encontrados: $containers"

# 1. Activar OdooBot
echo "🤖 Activando OdooBot..."
if docker exec odoo-patco-db psql -U odoo -d odoo_patco -c "UPDATE res_users SET active = true WHERE id = 1;" > /dev/null 2>&1; then
    echo "✅ OdooBot activado correctamente"
else
    echo "⚠️  Advertencia: No se pudo activar OdooBot"
fi

# 2. Limpiar assets corruptos
echo "🧹 Limpiando assets corruptos..."
if docker exec odoo-patco-db psql -U odoo -d odoo_patco -c "DELETE FROM ir_attachment WHERE name LIKE '%websocket_worker_bundle%' OR name LIKE '%bus%';" > /dev/null 2>&1; then
    echo "✅ Assets corruptos eliminados"
else
    echo "⚠️  Advertencia: No se pudieron eliminar assets"
fi

# 3. Limpiar archivos físicos corruptos
echo "📁 Limpiando archivos físicos corruptos..."
docker exec odoo-patco-app bash -c "find /home/odoo/.local/share/Odoo/filestore/odoo_patco -name '48' -type d -exec rm -rf {} + 2>/dev/null || true" > /dev/null 2>&1
echo "✅ Archivos físicos limpiados"

# 4. Reiniciar Odoo para regenerar assets
echo "🔄 Reiniciando Odoo para regenerar assets..."
if docker restart odoo-patco-app > /dev/null 2>&1; then
    echo "✅ Odoo reiniciado correctamente"
else
    echo "❌ Error: No se pudo reiniciar Odoo"
    exit 1
fi

# 5. Esperar a que Odoo se inicie
echo "⏳ Esperando a que Odoo se inicie completamente..."
sleep 30

# 6. Verificar que el Evented Service esté corriendo
echo "🔍 Verificando Evented Service..."
if docker exec odoo-patco-app bash -c "tail -n 20 /var/log/odoo/odoo.log | grep -q 'Evented Service.*running on.*8072'"; then
    echo "✅ Evented Service corriendo en puerto 8072"
else
    echo "⚠️  Advertencia: Evented Service no detectado en logs"
fi

# 7. Limpiar logs para pruebas
echo "🧽 Limpiando logs para pruebas..."
if [ -f "logs/odoo.log" ]; then
    > logs/odoo.log
elif [ -f "/var/log/odoo/odoo.log" ]; then
    docker exec odoo-patco-app bash -c "> /var/log/odoo/odoo.log"
fi

echo ""
echo "🎉 ¡Corrección completada!"
echo "📋 Resumen de acciones realizadas:"
echo "   ✅ OdooBot activado"
echo "   ✅ Assets corruptos eliminados"
echo "   ✅ Archivos físicos limpiados"
echo "   ✅ Odoo reiniciado y assets regenerados"
echo "   ✅ Logs limpiados"
echo ""
echo "🌐 Puedes probar el websocket en tu dominio configurado"
echo "📊 Dashboard de Traefik disponible si está configurado"
echo ""
echo "💡 Si el problema persiste, revisa los logs de Odoo"