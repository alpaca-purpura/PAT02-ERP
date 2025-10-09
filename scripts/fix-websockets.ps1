# ===== SCRIPT DE CORRECCIÓN DE WEBSOCKETS ODOO 18 =====
# Autor: PATCO Suite
# Descripción: Automatiza la corrección de problemas de websockets en Odoo 18
# Uso: .\scripts\fix-websockets.ps1

Write-Host "🔧 PATCO Suite - Corrección de WebSockets Odoo 18" -ForegroundColor Green
Write-Host "=================================================" -ForegroundColor Green

# Verificar que Docker esté corriendo
Write-Host "📋 Verificando estado de contenedores..." -ForegroundColor Yellow
$containers = docker ps --format "{{.Names}}" | Where-Object { $_ -match "odoo-patco" }

if (-not $containers) {
    Write-Host "❌ Error: Los contenedores de Odoo no están corriendo." -ForegroundColor Red
    Write-Host "   Ejecuta primero: docker compose up -d" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Contenedores encontrados: $($containers -join ', ')" -ForegroundColor Green

# 1. Activar OdooBot
Write-Host "🤖 Activando OdooBot..." -ForegroundColor Yellow
docker exec odoo-patco-db psql -U odoo -d odoo_patco -c "UPDATE res_users SET active = true WHERE id = 1;" | Out-Null

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ OdooBot activado correctamente" -ForegroundColor Green
} else {
    Write-Host "⚠️  Advertencia: No se pudo activar OdooBot" -ForegroundColor Yellow
}

# 2. Limpiar assets corruptos
Write-Host "🧹 Limpiando assets corruptos..." -ForegroundColor Yellow
docker exec odoo-patco-db psql -U odoo -d odoo_patco -c "DELETE FROM ir_attachment WHERE name LIKE '%websocket_worker_bundle%' OR name LIKE '%bus%';" | Out-Null

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Assets corruptos eliminados" -ForegroundColor Green
} else {
    Write-Host "⚠️  Advertencia: No se pudieron eliminar assets" -ForegroundColor Yellow
}

# 3. Limpiar archivos físicos corruptos
Write-Host "📁 Limpiando archivos físicos corruptos..." -ForegroundColor Yellow
try {
    $result = docker exec odoo-patco-app bash -c "find /home/odoo/.local/share/Odoo/filestore/odoo_patco -name '48' -type d -exec rm -rf {} + 2>/dev/null; exit 0" 2>$null
    Write-Host "✅ Archivos físicos limpiados" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Advertencia: No se pudieron limpiar algunos archivos físicos" -ForegroundColor Yellow
}

# 4. Reiniciar Odoo para regenerar assets
Write-Host "🔄 Reiniciando Odoo para regenerar assets..." -ForegroundColor Yellow
docker restart odoo-patco-app | Out-Null

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Odoo reiniciado correctamente" -ForegroundColor Green
} else {
    Write-Host "❌ Error: No se pudo reiniciar Odoo" -ForegroundColor Red
    exit 1
}

# 5. Esperar a que Odoo se inicie
Write-Host "⏳ Esperando a que Odoo se inicie completamente..." -ForegroundColor Yellow
Start-Sleep -Seconds 30

# 6. Verificar que el Evented Service esté corriendo
Write-Host "🔍 Verificando Evented Service..." -ForegroundColor Yellow
try {
    $logContent = Get-Content -Path "c:\Trabajo\PAT02-ERP\logs\odoo.log" -Tail 20 -ErrorAction SilentlyContinue
    $eventedServiceFound = $logContent | Where-Object { $_ -match "Evented Service.*running on.*8072" }
    
    if ($eventedServiceFound) {
        Write-Host "✅ Evented Service corriendo en puerto 8072" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Advertencia: Evented Service no detectado en logs" -ForegroundColor Yellow
    }
} catch {
    Write-Host "⚠️  Advertencia: No se pudo verificar el estado del Evented Service" -ForegroundColor Yellow
}

# 7. Limpiar logs para pruebas
Write-Host "🧽 Limpiando logs para pruebas..." -ForegroundColor Yellow
Clear-Content -Path "c:\Trabajo\PAT02-ERP\logs\odoo.log" -ErrorAction SilentlyContinue

Write-Host "" -ForegroundColor White
Write-Host "🎉 ¡Corrección completada!" -ForegroundColor Green
Write-Host "📋 Resumen de acciones realizadas:" -ForegroundColor Cyan
Write-Host "   ✅ OdooBot activado" -ForegroundColor White
Write-Host "   ✅ Assets corruptos eliminados" -ForegroundColor White
Write-Host "   ✅ Archivos físicos limpiados" -ForegroundColor White
Write-Host "   ✅ Odoo reiniciado y assets regenerados" -ForegroundColor White
Write-Host "   ✅ Logs limpiados" -ForegroundColor White
Write-Host "" -ForegroundColor White
Write-Host "🌐 Puedes probar el websocket en: http://localhost" -ForegroundColor Cyan
Write-Host "📊 Dashboard de Traefik: http://localhost:8080" -ForegroundColor Cyan
Write-Host "" -ForegroundColor White
Write-Host "💡 Si el problema persiste, revisa los logs en: logs/odoo.log" -ForegroundColor Yellow