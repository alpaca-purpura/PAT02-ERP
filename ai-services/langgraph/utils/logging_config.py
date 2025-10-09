#!/usr/bin/env python3
"""
Configuración de Logging para LangGraph Server

Configura logging estructurado usando structlog para el servidor LangGraph.

Autor: PATCO Development Team
Versión: 1.0.0
Fecha: Enero 2025
"""

import logging
import sys
from typing import Any, Dict

import structlog
from structlog.stdlib import LoggerFactory


def setup_logging(log_level: str = "INFO") -> None:
    """
    Configura logging estructurado para la aplicación.
    
    Args:
        log_level: Nivel de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    
    # Configurar logging estándar
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, log_level.upper())
    )
    
    # Configurar structlog
    structlog.configure(
        processors=[
            # Agregar timestamp
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="ISO"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            # Formatear como JSON para producción
            structlog.processors.JSONRenderer() if log_level != "DEBUG" 
            else structlog.dev.ConsoleRenderer(colors=True)
        ],
        context_class=dict,
        logger_factory=LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )


def get_logger(name: str) -> structlog.stdlib.BoundLogger:
    """
    Obtiene un logger estructurado.
    
    Args:
        name: Nombre del logger
        
    Returns:
        Logger estructurado configurado
    """
    return structlog.get_logger(name)


class LoggingMixin:
    """Mixin para agregar logging estructurado a clases."""
    
    @property
    def logger(self) -> structlog.stdlib.BoundLogger:
        """Obtiene logger para la clase."""
        if not hasattr(self, '_logger'):
            self._logger = get_logger(self.__class__.__name__)
        return self._logger
    
    def log_method_call(self, method_name: str, **kwargs) -> None:
        """
        Log de llamada a método.
        
        Args:
            method_name: Nombre del método
            **kwargs: Argumentos adicionales para el log
        """
        self.logger.debug(
            f"🔧 Llamando método {method_name}",
            method=method_name,
            class_name=self.__class__.__name__,
            **kwargs
        )
    
    def log_method_result(self, method_name: str, result: Any = None, **kwargs) -> None:
        """
        Log de resultado de método.
        
        Args:
            method_name: Nombre del método
            result: Resultado del método
            **kwargs: Argumentos adicionales para el log
        """
        self.logger.debug(
            f"✅ Método {method_name} completado",
            method=method_name,
            class_name=self.__class__.__name__,
            has_result=result is not None,
            **kwargs
        )
    
    def log_error(self, method_name: str, error: Exception, **kwargs) -> None:
        """
        Log de error en método.
        
        Args:
            method_name: Nombre del método
            error: Excepción ocurrida
            **kwargs: Argumentos adicionales para el log
        """
        self.logger.error(
            f"❌ Error en método {method_name}",
            method=method_name,
            class_name=self.__class__.__name__,
            error_type=type(error).__name__,
            error_message=str(error),
            **kwargs
        )