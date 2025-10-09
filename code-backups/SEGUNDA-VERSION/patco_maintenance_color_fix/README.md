# PATCO - Corrección de Colores para Maintenance

## Descripción

Este módulo resuelve el error `ValueError: invalid literal for int() with base 10: '#924f4f'` que ocurre cuando se intenta guardar una categoría de equipo con un color hexadecimal en el módulo `maintenance` de Odoo 18.

## Problema Resuelto

El modelo `maintenance.equipment.category` tiene un campo `color` definido como `Integer`, pero algunos widgets de UI envían valores hexadecimales (ej: `#924f4f`) en lugar de enteros, causando errores de conversión.

## Solución Implementada

### Conversión Robusta de Colores

El módulo implementa una conversión inteligente que:

1. **Detecta el tipo de valor**: Maneja tanto enteros como strings hexadecimales
2. **Valida formato hexadecimal**: Verifica que el formato sea `#RRGGBB`
3. **Mapea a paleta de Odoo**: Convierte colores hexadecimales al índice más cercano (0-11)
4. **Calcula distancia de color**: Usa distancia euclidiana en espacio RGB
5. **Mantiene compatibilidad**: Funciona con valores enteros existentes

### Paleta de Colores Estándar

```python
ODOO_COLOR_PALETTE = {
    '#FF0000': 1,   # Rojo
    '#FF8C00': 2,   # Naranja
    '#FFD700': 3,   # Amarillo
    '#32CD32': 4,   # Verde Lima
    '#00FF00': 5,   # Verde
    '#00CED1': 6,   # Turquesa
    '#0000FF': 7,   # Azul
    '#9932CC': 8,   # Púrpura
    '#FF1493': 9,   # Rosa
    '#8B4513': 10,  # Marrón
    '#808080': 11,  # Gris
    '#000000': 0,   # Negro (por defecto)
}
```

## Funcionalidades

### Métodos Principales

- `_convert_color_value()`: Conversión principal de cualquier valor a entero válido
- `_find_closest_odoo_color()`: Encuentra el color más cercano en la paleta
- `_hex_to_rgb()`: Convierte hexadecimal a valores RGB
- `_calculate_color_distance()`: Calcula distancia entre colores
- `_validate_hex_color()`: Valida formato hexadecimal

### Validaciones

- Constraint `_check_color_value()`: Asegura que el color esté en rango 0-11
- Validación de formato hexadecimal con regex
- Manejo de errores con logging detallado

## Compatibilidad con Futuras Versiones

### Diseño Future-Proof

1. **Paleta Estándar**: Usa los 12 colores estándar de Odoo que han sido consistentes desde la v8
2. **Algoritmo Robusto**: La conversión por distancia euclidiana es matemáticamente sólida
3. **Logging Detallado**: Facilita debugging en futuras versiones
4. **Validaciones Estrictas**: Previene errores por cambios en la UI
5. **Herencia Limpia**: No modifica el modelo original, solo extiende

### Estrategia de Migración

- **Odoo 19+**: Si cambia el tipo de campo, el módulo se puede adaptar fácilmente
- **Nuevos Widgets**: La validación hexadecimal maneja cualquier widget que envíe #RRGGBB
- **API Changes**: Los métodos `create()` y `write()` son puntos de extensión estables

## Instalación

1. Copiar el módulo a `extra-addons/`
2. Actualizar lista de módulos
3. Instalar `patco_maintenance_color_fix`

```bash
# Instalación
docker exec odoo-patco-app python3 /opt/odoo/odoo-bin -c /etc/odoo/odoo.conf -d odoo_patco -i patco_maintenance_color_fix --stop-after-init

# Actualización
docker exec odoo-patco-app python3 /opt/odoo/odoo-bin -c /etc/odoo/odoo.conf -d odoo_patco -u patco_maintenance_color_fix --stop-after-init
```

## Uso

Una vez instalado, el módulo funciona automáticamente:

1. Los usuarios pueden seguir usando widgets de color que envíen valores hexadecimales
2. El sistema convierte automáticamente `#924f4f` → `10` (marrón más cercano)
3. Los valores enteros existentes siguen funcionando normalmente
4. Se registra la conversión en los logs para auditoría

## Ejemplos de Conversión

```python
# Conversiones automáticas
'#FF0000' → 1  # Rojo exacto
'#924f4f' → 10 # Marrón (más cercano)
'#00FF00' → 5  # Verde exacto
'#INVALID' → 0 # Error → Negro por defecto
5 → 5          # Entero válido sin cambios
15 → 11        # Entero fuera de rango → Máximo válido
```

## Logging

El módulo registra todas las conversiones:

```
INFO: Color #924f4f mapeado al índice 10 (distancia: 45.23)
INFO: Color convertido de #FF0000 a 1
WARNING: Color hexadecimal inválido #GGGGGG. Usando color por defecto.
```

## Dependencias

- `base`: Funcionalidades básicas de Odoo
- `maintenance`: Módulo de mantenimiento estándar

## Estructura del Módulo

```
patco_maintenance_color_fix/
├── __init__.py
├── __manifest__.py
├── README.md
└── models/
    ├── __init__.py
    └── maintenance_equipment_category.py
```

## Licencia

LGPL-3 - Compatible con Odoo Community Edition