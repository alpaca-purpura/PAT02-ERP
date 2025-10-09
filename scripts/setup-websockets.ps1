# ===== SCRIPT DE CONFIGURACIÓN INICIAL WEBSOCKETS =====
# Autor: PATCO Suite
# Descripción: Configura el entorno para prevenir problemas de websockets
# Uso: .\scripts\setup-websockets.ps1

Write-Host "🚀 PATCO Suite - Configuración Inicial WebSockets" -ForegroundColor Green
Write-Host "=================================================" -ForegroundColor Green

# Verificar que los contenedores estén corriendo
Write-Host "📋 Verificando contenedores..." -ForegroundColor Yellow
$containers = docker ps --format "{{.Names}}" | Where-Object { $_ -match "odoo-patco" }

if (-not $containers) {
    Write-Host "❌ Error: Los contenedores no están corriendo." -ForegroundColor Red
    Write-Host "   Ejecuta primero: docker compose up -d" -ForegroundColor Red
    exit 1
}

# Esperar a que Odoo se inicie completamente
Write-Host "⏳ Esperando a que Odoo se inicie completamente..." -ForegroundColor Yellow
Start-Sleep -Seconds 45

# Verificar que la base de datos esté lista
Write-Host "🗄️  Verificando base de datos..." -ForegroundColor Yellow
$dbCheck = docker exec odoo-patco-db psql -U odoo -d odoo_patco -c "SELECT 1;" 2>$null

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Error: La base de datos no está lista." -ForegroundColor Red
    exit 1
}

Write-Host "✅ Base de datos lista" -ForegroundColor Green

# Configuración preventiva
Write-Host "🔧 Aplicando configuración preventiva..." -ForegroundColor Yellow

# 1. Asegurar que OdooBot esté activo
docker exec odoo-patco-db psql -U odoo -d odoo_patco -c "UPDATE res_users SET active = true WHERE id = 1;" | Out-Null
Write-Host "   ✅ OdooBot configurado como activo" -ForegroundColor Green

# 2. Limpiar assets potencialmente problemáticos
docker exec odoo-patco-db psql -U odoo -d odoo_patco -c "DELETE FROM ir_attachment WHERE name LIKE '%websocket_worker_bundle%' AND res_model IS NULL;" | Out-Null
Write-Host "   ✅ Assets problemáticos limpiados" -ForegroundColor Green

# 3. Verificar configuración de workers
Write-Host "🔍 Verificando configuración de workers..." -ForegroundColor Yellow
$workerCheck = docker exec odoo-patco-app bash -c "grep -E 'workers|longpolling_port|gevent_port' /etc/odoo/odoo.conf"

if ($workerCheck -match "workers.*=.*2" -and $workerCheck -match "longpolling_port.*=.*8072") {
    Write-Host "   ✅ Configuración de workers correcta" -ForegroundColor Green
} else {
    Write-Host "   ⚠️  Advertencia: Revisar configuración de workers en odoo.conf" -ForegroundColor Yellow
}

# 4. Verificar Traefik
Write-Host "🌐 Verificando Traefik..." -ForegroundColor Yellow
$traefik = docker ps --format "{{.Names}}" | Where-Object { $_ -match "traefik" }

if ($traefik) {
    Write-Host "   ✅ Traefik corriendo: $traefik" -ForegroundColor Green
} else {
    Write-Host "   ⚠️  Advertencia: Traefik no detectado" -ForegroundColor Yellow
}

Write-Host "" -ForegroundColor White
Write-Host "🎉 ¡Configuración inicial completada!" -ForegroundColor Green
Write-Host "📋 El entorno está configurado para prevenir problemas de websockets" -ForegroundColor Cyan
Write-Host "" -ForegroundColor White
Write-Host "💡 Si experimentas problemas de websockets, ejecuta:" -ForegroundColor Yellow
Write-Host "   .\scripts\fix-websockets.ps1" -ForegroundColor White