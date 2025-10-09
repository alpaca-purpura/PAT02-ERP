#!/usr/bin/env python3
"""
Servidor LangGraph para PATCO Suite

Servidor FastAPI que implementa orquestación conversacional usando LangGraph
para el agente IA de PATCO Suite.

Autor: PATCO Development Team
Versión: 1.0.0
Fecha: Enero 2025
"""

import asyncio
import logging
import time
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Dict, Any

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import structlog

from config import settings
from schemas import (
    ProcessMessageRequest, ProcessMessageResponse,
    ConversationHistoryResponse, HealthCheckResponse,
    ConversationState, ConversationMessage
)
from graphs.conversation_graph import ConversationGraph
from utils.mcp_client import MCPClient
from utils.logging_config import setup_logging

# Configurar logging estructurado
setup_logging()
logger = structlog.get_logger(__name__)

# Variables globales
conversation_graph: ConversationGraph = None
mcp_client: MCPClient = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestión del ciclo de vida de la aplicación."""
    
    # Startup
    logger.info("🚀 Iniciando servidor LangGraph...")
    
    try:
        # Inicializar cliente MCP
        global mcp_client
        mcp_client = MCPClient(settings.get_mcp_server_url())
        await mcp_client.connect()
        logger.info("✅ Cliente MCP conectado")
        
        # Inicializar grafo de conversación
        global conversation_graph
        conversation_graph = ConversationGraph(
            database_url=settings.get_database_url(),
            mcp_client=mcp_client
        )
        await conversation_graph.initialize()
        logger.info("✅ Grafo de conversación inicializado")
        
        logger.info("🎯 Servidor LangGraph listo para recibir requests")
        
        yield
        
    except Exception as e:
        logger.error("❌ Error durante startup", error=str(e))
        raise
    
    # Shutdown
    logger.info("🛑 Cerrando servidor LangGraph...")
    
    try:
        if mcp_client:
            await mcp_client.disconnect()
            logger.info("✅ Cliente MCP desconectado")
        
        if conversation_graph:
            await conversation_graph.cleanup()
            logger.info("✅ Grafo de conversación limpiado")
            
    except Exception as e:
        logger.error("❌ Error durante shutdown", error=str(e))


# Crear aplicación FastAPI
app = FastAPI(
    title="PATCO LangGraph Server",
    description="Servidor de orquestación conversacional para agente IA PATCO",
    version="1.0.0",
    lifespan=lifespan
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins(),
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Configurar TrustedHost
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]  # En producción, especificar hosts específicos
)


@app.middleware("http")
async def logging_middleware(request, call_next):
    """Middleware para logging de requests."""
    
    start_time = time.time()
    
    # Log del request
    logger.info(
        "📥 Request recibido",
        method=request.method,
        url=str(request.url),
        client_ip=request.client.host if request.client else "unknown"
    )
    
    # Procesar request
    response = await call_next(request)
    
    # Log de la respuesta
    process_time = time.time() - start_time
    logger.info(
        "📤 Response enviado",
        method=request.method,
        url=str(request.url),
        status_code=response.status_code,
        process_time=f"{process_time:.3f}s"
    )
    
    return response


@app.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """Endpoint de health check."""
    
    dependencies = {}
    
    try:
        # Verificar conexión MCP
        if mcp_client and await mcp_client.is_connected():
            dependencies["mcp_server"] = "connected"
        else:
            dependencies["mcp_server"] = "disconnected"
        
        # Verificar grafo de conversación
        if conversation_graph and conversation_graph.is_ready():
            dependencies["conversation_graph"] = "ready"
        else:
            dependencies["conversation_graph"] = "not_ready"
        
        return HealthCheckResponse(
            status="healthy",
            service="langgraph-server",
            dependencies=dependencies
        )
        
    except Exception as e:
        logger.error("❌ Error en health check", error=str(e))
        raise HTTPException(status_code=503, detail="Service unhealthy")


@app.post("/conversation/{conversation_id}/message", response_model=ProcessMessageResponse)
async def process_conversation_message(
    conversation_id: str,
    request: ProcessMessageRequest,
    background_tasks: BackgroundTasks
):
    """Procesa un mensaje en una conversación específica."""
    
    start_time = time.time()
    
    try:
        logger.info(
            "💬 Procesando mensaje",
            conversation_id=conversation_id,
            message_role=request.message.role,
            message_length=len(request.message.content)
        )
        
        # Validar que el grafo esté listo
        if not conversation_graph or not conversation_graph.is_ready():
            raise HTTPException(
                status_code=503, 
                detail="Conversation graph not ready"
            )
        
        # Configurar contexto de la conversación
        config = {"configurable": {"thread_id": conversation_id}}
        
        # Preparar estado inicial
        initial_state = ConversationState(
            messages=[request.message],
            context=request.context or ConversationContext()
        )
        
        # Ejecutar grafo de conversación
        result = await conversation_graph.process_message(
            initial_state.dict(),
            config=config
        )
        
        # Calcular tiempo de procesamiento
        processing_time = time.time() - start_time
        
        # Preparar respuesta
        response = ProcessMessageResponse(
            conversation_id=conversation_id,
            response=result.get("response"),
            actions=result.get("actions", []),
            conversation_state=result.get("conversation_state", "unknown"),
            processing_time=processing_time
        )
        
        logger.info(
            "✅ Mensaje procesado exitosamente",
            conversation_id=conversation_id,
            processing_time=f"{processing_time:.3f}s",
            response_length=len(response.response) if response.response else 0
        )
        
        return response
        
    except Exception as e:
        logger.error(
            "❌ Error procesando mensaje",
            conversation_id=conversation_id,
            error=str(e)
        )
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/conversation/{conversation_id}/history", response_model=ConversationHistoryResponse)
async def get_conversation_history(conversation_id: str):
    """Obtiene el historial de una conversación."""
    
    try:
        logger.info("📚 Obteniendo historial", conversation_id=conversation_id)
        
        if not conversation_graph or not conversation_graph.is_ready():
            raise HTTPException(
                status_code=503,
                detail="Conversation graph not ready"
            )
        
        # Configurar contexto
        config = {"configurable": {"thread_id": conversation_id}}
        
        # Obtener historial del checkpointer
        history = await conversation_graph.get_conversation_history(config)
        
        return ConversationHistoryResponse(
            conversation_id=conversation_id,
            messages=history.get("messages", []),
            state=history.get("conversation_state", "unknown"),
            context=history.get("context", {})
        )
        
    except Exception as e:
        logger.error(
            "❌ Error obteniendo historial",
            conversation_id=conversation_id,
            error=str(e)
        )
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/conversation/{conversation_id}/reset")
async def reset_conversation(conversation_id: str):
    """Reinicia una conversación específica."""
    
    try:
        logger.info("🔄 Reiniciando conversación", conversation_id=conversation_id)
        
        if not conversation_graph or not conversation_graph.is_ready():
            raise HTTPException(
                status_code=503,
                detail="Conversation graph not ready"
            )
        
        # Configurar contexto
        config = {"configurable": {"thread_id": conversation_id}}
        
        # Reiniciar conversación
        await conversation_graph.reset_conversation(config)
        
        return {"message": "Conversation reset successfully", "conversation_id": conversation_id}
        
    except Exception as e:
        logger.error(
            "❌ Error reiniciando conversación",
            conversation_id=conversation_id,
            error=str(e)
        )
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/conversations/active")
async def get_active_conversations():
    """Obtiene lista de conversaciones activas."""
    
    try:
        logger.info("📋 Obteniendo conversaciones activas")
        
        if not conversation_graph or not conversation_graph.is_ready():
            raise HTTPException(
                status_code=503,
                detail="Conversation graph not ready"
            )
        
        active_conversations = await conversation_graph.get_active_conversations()
        
        return {
            "active_conversations": active_conversations,
            "count": len(active_conversations)
        }
        
    except Exception as e:
        logger.error("❌ Error obteniendo conversaciones activas", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/metrics")
async def get_metrics():
    """Obtiene métricas del servidor."""
    
    try:
        metrics = {
            "service": "langgraph-server",
            "version": "1.0.0",
            "uptime": time.time(),  # Se calculará el uptime real
            "status": "running"
        }
        
        if conversation_graph:
            graph_metrics = await conversation_graph.get_metrics()
            metrics.update(graph_metrics)
        
        return metrics
        
    except Exception as e:
        logger.error("❌ Error obteniendo métricas", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def root():
    """Endpoint raíz con información del servicio."""
    
    return {
        "service": "PATCO LangGraph Server",
        "version": "1.0.0",
        "description": "Servidor de orquestación conversacional para agente IA",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "process_message": "/conversation/{conversation_id}/message",
            "get_history": "/conversation/{conversation_id}/history",
            "reset_conversation": "/conversation/{conversation_id}/reset",
            "active_conversations": "/conversations/active",
            "metrics": "/metrics"
        }
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host=settings.LANGGRAPH_HOST,
        port=settings.LANGGRAPH_PORT,
        reload=settings.LANGGRAPH_DEBUG,
        log_level=settings.LANGGRAPH_LOG_LEVEL.lower()
    )