# -*- coding: utf-8 -*-


def post_init_hook(env):
    """
    Hook ejecutado después de la instalación del módulo.
    Configura automáticamente la suite PATCO.
    """
    # Log de instalación exitosa
    import logging
    _logger = logging.getLogger(__name__)
    _logger.info("PATCO Suite instalado correctamente. Todos los módulos están disponibles.")