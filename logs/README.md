# Logs de Odoo - Sistema PATCO

Este directorio contiene los archivos de log de Odoo para el sistema PATCO.

## Configuración de Logging

Los logs están configurados con nivel DEBUG para:
- Módulos PATCO: `patco_core`, `patco_customer_equipment`, `patco_hr_skills`, `patco_suite`
- Módulos OCA: `fieldservice`, `maintenance`, `helpdesk`, `agreement`, y relacionados

## Archivos de Log

- `odoo.log`: Log principal de Odoo con información detallada de todos los módulos
- Los logs se rotan automáticamente cuando alcanzan cierto tamaño

## Uso Durante Pruebas

Para monitorear errores durante las pruebas:

```bash
# Ver logs en tiempo real
tail -f logs/odoo.log

# Filtrar errores específicos
grep -i "error\|exception\|traceback" logs/odoo.log

# Filtrar por módulo específico
grep "patco_" logs/odoo.log
```

## Notas

- Los logs se generan automáticamente cuando Odoo está ejecutándose
- El directorio está mapeado desde el contenedor Docker `/var/log/odoo`
- Los logs incluyen timestamps, niveles y información de módulos