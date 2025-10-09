# -*- coding: utf-8 -*-
import logging
import re
from odoo import api, models, fields, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class MaintenanceEquipmentCategory(models.Model):
    """
    Extensión del modelo maintenance.equipment.category para manejar
    conversión robusta de colores hexadecimales a enteros.
    """
    _inherit = 'maintenance.equipment.category'

    # Paleta de colores estándar de Odoo (índices 0-11)
    # Estos colores son consistentes en todas las versiones de Odoo
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
        '#FFFFFF': 0,   # Blanco -> Negro (por defecto)
    }

    @api.model
    def _hex_to_rgb(self, hex_color):
        """
        Convierte un color hexadecimal a valores RGB.
        
        Args:
            hex_color (str): Color en formato hexadecimal (#RRGGBB)
            
        Returns:
            tuple: (r, g, b) valores entre 0-255
        """
        hex_color = hex_color.lstrip('#')
        if len(hex_color) != 6:
            raise ValueError(f"Color hexadecimal inválido: #{hex_color}")
        
        try:
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            return (r, g, b)
        except ValueError as e:
            raise ValueError(f"Error al convertir color hexadecimal #{hex_color}: {e}")

    @api.model
    def _calculate_color_distance(self, color1_rgb, color2_rgb):
        """
        Calcula la distancia euclidiana entre dos colores RGB.
        
        Args:
            color1_rgb (tuple): (r, g, b) del primer color
            color2_rgb (tuple): (r, g, b) del segundo color
            
        Returns:
            float: Distancia entre los colores
        """
        return sum((c1 - c2) ** 2 for c1, c2 in zip(color1_rgb, color2_rgb)) ** 0.5

    @api.model
    def _find_closest_odoo_color(self, hex_color):
        """
        Encuentra el color más cercano en la paleta de Odoo.
        
        Args:
            hex_color (str): Color en formato hexadecimal
            
        Returns:
            int: Índice del color más cercano en la paleta de Odoo
        """
        # Normalizar el color de entrada
        hex_color = hex_color.upper().strip()
        
        # Si el color está directamente en la paleta, devolverlo
        if hex_color in self.ODOO_COLOR_PALETTE:
            return self.ODOO_COLOR_PALETTE[hex_color]
        
        try:
            target_rgb = self._hex_to_rgb(hex_color)
        except ValueError as e:
            _logger.warning(f"Color hexadecimal inválido {hex_color}: {e}. Usando color por defecto.")
            return 0  # Negro por defecto
        
        # Encontrar el color más cercano
        min_distance = float('inf')
        closest_color_index = 0
        
        for palette_hex, color_index in self.ODOO_COLOR_PALETTE.items():
            try:
                palette_rgb = self._hex_to_rgb(palette_hex)
                distance = self._calculate_color_distance(target_rgb, palette_rgb)
                
                if distance < min_distance:
                    min_distance = distance
                    closest_color_index = color_index
                    
            except ValueError:
                continue  # Saltar colores inválidos en la paleta
        
        _logger.info(f"Color {hex_color} mapeado al índice {closest_color_index} (distancia: {min_distance:.2f})")
        return closest_color_index

    @api.model
    def _validate_hex_color(self, color_value):
        """
        Valida si un valor es un color hexadecimal válido.
        
        Args:
            color_value (str): Valor a validar
            
        Returns:
            bool: True si es un color hexadecimal válido
        """
        if not isinstance(color_value, str):
            return False
        
        # Patrón para color hexadecimal: #RRGGBB
        hex_pattern = r'^#[0-9A-Fa-f]{6}$'
        return bool(re.match(hex_pattern, color_value))

    @api.model
    def _convert_color_value(self, color_value):
        """
        Convierte un valor de color a entero, manejando tanto enteros como hexadecimales.
        
        Args:
            color_value: Valor del color (int, str, o None)
            
        Returns:
            int: Índice de color válido para Odoo (0-11)
        """
        # Si ya es un entero válido, devolverlo
        if isinstance(color_value, int):
            # Asegurar que esté en el rango válido (0-11)
            return max(0, min(11, color_value))
        
        # Si es None o vacío, devolver color por defecto
        if not color_value:
            return 0
        
        # Si es string, intentar conversión
        if isinstance(color_value, str):
            color_value = color_value.strip()
            
            # Si es un color hexadecimal
            if self._validate_hex_color(color_value):
                return self._find_closest_odoo_color(color_value)
            
            # Si es un string que representa un entero
            try:
                int_value = int(color_value)
                return max(0, min(11, int_value))
            except ValueError:
                _logger.warning(f"Valor de color no reconocido: {color_value}. Usando color por defecto.")
                return 0
        
        # Para cualquier otro tipo, usar color por defecto
        _logger.warning(f"Tipo de color no soportado: {type(color_value)}. Usando color por defecto.")
        return 0

    @api.model_create_multi
    def create(self, vals_list):
        """
        Override del método create para manejar conversión de colores.
        """
        for vals in vals_list:
            if 'color' in vals:
                original_color = vals['color']
                converted_color = self._convert_color_value(original_color)
                
                if original_color != converted_color:
                    _logger.info(f"Color convertido de {original_color} a {converted_color}")
                
                vals['color'] = converted_color
        
        return super().create(vals_list)

    def write(self, vals):
        """
        Override del método write para manejar conversión de colores.
        """
        if 'color' in vals:
            original_color = vals['color']
            converted_color = self._convert_color_value(original_color)
            
            if original_color != converted_color:
                _logger.info(f"Color convertido de {original_color} a {converted_color}")
            
            vals['color'] = converted_color
        
        return super().write(vals)

    @api.constrains('color')
    def _check_color_value(self):
        """
        Constraint para validar que el color esté en el rango válido.
        """
        for record in self:
            if record.color is not None and not (0 <= record.color <= 11):
                raise ValidationError(
                    _("El valor del color debe estar entre 0 y 11. Valor actual: %s") % record.color
                )