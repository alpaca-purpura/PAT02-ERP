# Plan de Implementación Detallado - Agente IA con RAG para PATCO Suite

**Versión:** 1.0  
**Fecha:** Enero 2025  
**Duración Estimada:** 8-10 semanas  
**Metodología:** Desarrollo incremental con validación continua  

## 🎯 Objetivos del Plan

### Objetivo Principal
Implementar el sistema de Agente IA con RAG de manera incremental, asegurando que cada fase sea completamente funcional antes de proceder a la siguiente, minimizando riesgos y maximizando la validación temprana.

### Principios de Implementación
1. **Fases Pequeñas y Medibles**: Cada fase debe completarse en 1-2 semanas máximo
2. **Validación Continua**: Pruebas exhaustivas al final de cada fase
3. **Rollback Seguro**: Capacidad de revertir cambios sin afectar el sistema productivo
4. **Documentación Actualizada**: README.md actualizado en cada fase
5. **Ejecución Autónoma**: Todas las tareas ejecutables por el asistente IA

## 📋 Resumen de Fases

| Fase | Nombre | Duración | Dependencias | Entregables Clave |
|------|--------|----------|--------------|-------------------|
| **0** | Preparación del Entorno | 3-5 días | Ninguna | Infraestructura base lista |
| **1** | Módulo Base patco_ai_agent | 1 semana | Fase 0 | Módulo instalable con modelos básicos |
| **2** | Extensión PostgreSQL + PGVector | 3-5 días | Fase 1 | Base de datos con capacidades vectoriales |
| **3** | Indexador de Documentos | 1 semana | Fase 2 | Sistema de indexación automática |
| **4** | Servidor MCP Básico | 1 semana | Fase 1 | Conectividad Odoo-IA funcional |
| **5** | LangGraph Core | 1.5 semanas | Fase 4 | Orquestador conversacional básico |
| **6** | Integración FSM Básica | 1 semana | Fase 5 | Conversaciones vinculadas a órdenes FSM |
| **7** | RAG y Búsqueda Semántica | 1 semana | Fase 3,5 | Búsqueda inteligente en base de conocimiento |
| **8** | Generación de Reportes | 1 semana | Fase 6,7 | Reportes automáticos desde conversaciones |
| **9** | Interfaz de Usuario | 1 semana | Fase 6 | Widget de chat integrado en Odoo |
| **10** | Optimización y Producción | 1 semana | Todas | Sistema listo para producción |

## 🚀 Fase 0: Preparación del Entorno (3-5 días)

### Objetivos
- Configurar infraestructura Docker extendida
- Preparar variables de entorno y configuraciones
- Validar conectividad entre servicios

### Tareas Específicas

#### Tarea 0.1: Configuración Docker Extendida
```bash
# Crear estructura de directorios
mkdir -p ai-services/{langgraph,mcp,indexer}
mkdir -p ai-services/langgraph/{graphs,nodes,utils}
mkdir -p ai-services/mcp/{tools,schemas}
mkdir -p ai-services/indexer/{processors,embeddings}

# Crear archivos de configuración base
touch docker-compose.ai.yml
touch .env.ai
```

#### Tarea 0.2: Variables de Entorno
```bash
# .env.ai
GEMINI_API_KEY=your_gemini_api_key_here
ODOO_AI_USER=ai_agent_user
ODOO_AI_PASSWORD=secure_password_here
LANGGRAPH_SERVER_PORT=8001
MCP_SERVER_PORT=8002
VECTOR_INDEXER_SCHEDULE=0 2 * * *  # Diario a las 2 AM
```

#### Tarea 0.3: Docker Compose AI
```yaml
# docker-compose.ai.yml - Versión inicial mínima
version: '3.8'

services:
  pgvector-setup:
    image: postgres:15
    depends_on:
      - db
    command: >
      bash -c "
        echo 'Esperando PostgreSQL...' &&
        sleep 30 &&
        PGPASSWORD=P4tc0_2 psql -h db -U odoo -d odoo_patco -c 'CREATE EXTENSION IF NOT EXISTS vector;' &&
        echo 'Extensión pgvector instalada correctamente'
      "
    networks:
      - odoo-network
    restart: "no"

networks:
  odoo-network:
    external: true
    name: odoo-patco-network
```

#### Criterios de Aceptación Fase 0
- [ ] Estructura de directorios creada correctamente
- [ ] Variables de entorno configuradas
- [ ] PGVector instalado en PostgreSQL existente
- [ ] Conectividad entre servicios validada
- [ ] Logs limpios sin errores de configuración

---

## 🏗️ Fase 1: Módulo Base patco_ai_agent (1 semana)

### Objetivos
- Crear módulo Odoo funcional e instalable
- Implementar modelos de datos básicos
- Configurar permisos y seguridad inicial

### Tareas Específicas

#### Tarea 1.1: Estructura del Módulo
```python
# extra-addons/patco_ai_agent/__manifest__.py
{
    'name': 'PATCO AI Agent with RAG',
    'version': '18.0.1.0.0',
    'category': 'Artificial Intelligence',
    'summary': 'AI Agent with RAG capabilities for PATCO Suite',
    'description': """
        Agente IA conversacional integrado con capacidades RAG para guiar
        técnicos de campo durante servicios, con generación automática de reportes.
    """,
    'author': 'PATCO',
    'website': 'https://patco.com.pe',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'mail',
        'discuss',
        'patco_suite',  # Dependencia de toda la suite PATCO
    ],
    'external_dependencies': {
        'python': [
            'requests',
            'numpy',
            'psycopg2-binary'
        ]
    },
    'data': [
        'security/ir.model.access.csv',
        'security/security_groups.xml',
        'data/ai_agent_data.xml',
        'views/ai_conversation_views.xml',
        'views/ai_knowledge_base_views.xml',
        'views/discuss_channel_views.xml',
        'views/menu_views.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
```

#### Tarea 1.2: Modelos de Datos Básicos
```python
# models/ai_conversation.py
from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class AIConversation(models.Model):
    _name = 'ai.conversation'
    _description = 'Conversación con Agente IA'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'
    
    name = fields.Char('Nombre', compute='_compute_name', store=True)
    fsm_order_id = fields.Many2one('fsm.order', 'Orden FSM', required=True)
    technician_id = fields.Many2one('hr.employee', 'Técnico', required=True)
    channel_id = fields.Many2one('discuss.channel', 'Canal de Conversación')
    
    state = fields.Selection([
        ('initiated', 'Iniciado'),
        ('equipment_selected', 'Equipo Seleccionado'),
        ('checklist_entry', 'Checklist de Entrada'),
        ('work_in_progress', 'Trabajo en Progreso'),
        ('checklist_exit', 'Checklist de Salida'),
        ('report_generated', 'Reporte Generado'),
        ('completed', 'Completado'),
        ('archived', 'Archivado')
    ], default='initiated', tracking=True)
    
    current_equipment_id = fields.Many2one('maintenance.equipment', 'Equipo Actual')
    context_data = fields.Json('Datos de Contexto', default=dict)
    conversation_summary = fields.Text('Resumen de Conversación')
    
    # Métricas básicas
    message_count = fields.Integer('Número de Mensajes', default=0)
    start_time = fields.Datetime('Hora de Inicio', default=fields.Datetime.now)
    end_time = fields.Datetime('Hora de Finalización')
    duration = fields.Float('Duración (horas)', compute='_compute_duration', store=True)
    
    # Resultados
    report_url = fields.Char('URL del Reporte')
    report_generated = fields.Boolean('Reporte Generado', default=False)
    
    @api.depends('fsm_order_id', 'technician_id')
    def _compute_name(self):
        for record in self:
            if record.fsm_order_id and record.technician_id:
                record.name = f"IA-{record.fsm_order_id.name}-{record.technician_id.name}"
            else:
                record.name = "Nueva Conversación IA"
    
    @api.depends('start_time', 'end_time')
    def _compute_duration(self):
        for record in self:
            if record.start_time and record.end_time:
                delta = record.end_time - record.start_time
                record.duration = delta.total_seconds() / 3600.0
            else:
                record.duration = 0.0
    
    def action_start_conversation(self):
        """Inicia la conversación con el agente IA"""
        self.ensure_one()
        
        # Crear canal de discuss si no existe
        if not self.channel_id:
            channel = self.env['discuss.channel'].create({
                'name': f"🤖 Asistente IA - {self.fsm_order_id.name}",
                'channel_type': 'chat',
                'channel_partner_ids': [(4, self.technician_id.user_id.partner_id.id)]
            })
            self.channel_id = channel.id
        
        # Enviar mensaje inicial
        self._send_initial_message()
        
        # Actualizar estado
        self.state = 'equipment_selected'
        
        _logger.info(f"Conversación IA iniciada: {self.name}")
    
    def _send_initial_message(self):
        """Envía mensaje inicial del agente IA"""
        message = f"""
        ¡Hola {self.technician_id.name}! 👋
        
        Soy tu asistente IA para la orden de servicio **{self.fsm_order_id.name}**.
        
        📋 **Detalles del servicio:**
        - Cliente: {self.fsm_order_id.partner_id.name}
        - Ubicación: {self.fsm_order_id.location_id.name if self.fsm_order_id.location_id else 'No especificada'}
        - Equipos asignados: {len(self.fsm_order_id.equipment_ids)} equipos
        
        Te ayudaré durante todo el proceso. ¿Has llegado al sitio y estás listo para comenzar?
        """
        
        # Crear partner para el agente IA si no existe
        ai_partner = self.env.ref('patco_ai_agent.ai_agent_partner', raise_if_not_found=False)
        if not ai_partner:
            ai_partner = self.env['res.partner'].create({
                'name': '🤖 Asistente IA PATCO',
                'is_company': False,
                'email': 'ai-agent@patco.com.pe',
                'phone': '+51-1-234-5678'
            })
        
        self.channel_id.message_post(
            body=message,
            author_id=ai_partner.id,
            message_type='comment'
        )
```

#### Tarea 1.3: Extensión de ir.attachment para RAG
```python
# models/ir_attachment.py
from odoo import models, fields, api
import hashlib
import json

class IrAttachment(models.Model):
    _inherit = 'ir.attachment'
    
    # Campos para RAG
    x_embedding = fields.Binary('Vector Embedding')
    x_embedding_model = fields.Char('Modelo de Embedding', default='gemini-embedding-001')
    x_chunk_index = fields.Integer('Índice de Chunk', default=0)
    x_parent_document_id = fields.Many2one('ir.attachment', 'Documento Padre')
    x_content_hash = fields.Char('Hash de Contenido', compute='_compute_content_hash', store=True)
    x_indexed_date = fields.Datetime('Fecha de Indexación')
    x_equipment_category_ids = fields.Many2many(
        'maintenance.equipment.category', 
        'attachment_equipment_category_rel',
        'attachment_id', 'category_id',
        string='Categorías de Equipo Relacionadas'
    )
    x_service_nature_ids = fields.Many2many(
        'patco.service.nature',
        'attachment_service_nature_rel',
        'attachment_id', 'nature_id',
        string='Naturalezas de Servicio Relacionadas'
    )
    x_document_type = fields.Selection([
        ('manual', 'Manual Técnico'),
        ('procedure', 'Procedimiento'),
        ('checklist', 'Lista de Verificación'),
        ('report', 'Reporte de Servicio'),
        ('image', 'Imagen Técnica'),
        ('video', 'Video Instructivo'),
        ('other', 'Otro')
    ], string='Tipo de Documento', default='other')
    
    x_is_indexed = fields.Boolean('Indexado para RAG', default=False)
    x_indexing_error = fields.Text('Error de Indexación')
    
    @api.depends('datas')
    def _compute_content_hash(self):
        for record in self:
            if record.datas:
                content = record.datas
                record.x_content_hash = hashlib.sha256(content).hexdigest()
            else:
                record.x_content_hash = False
    
    def action_index_for_rag(self):
        """Marca el documento para indexación RAG"""
        self.ensure_one()
        
        # Validar que el documento sea indexable
        if not self.datas:
            self.x_indexing_error = "No hay contenido para indexar"
            return False
        
        # Marcar para indexación
        self.write({
            'x_is_indexed': False,  # Se marcará como True cuando se complete la indexación
            'x_indexing_error': False,
            'x_indexed_date': False
        })
        
        # Aquí se podría disparar un job de indexación
        # Por ahora solo marcamos el documento
        
        return True
    
    def search_similar(self, query: str, limit: int = 10):
        """Búsqueda por similitud semántica - Implementación básica"""
        # Por ahora retorna búsqueda textual básica
        # Se implementará búsqueda vectorial en fases posteriores
        
        domain = [
            ('x_is_indexed', '=', True),
            '|', '|',
            ('name', 'ilike', query),
            ('description', 'ilike', query),
            ('index_content', 'ilike', query)
        ]
        
        return self.search(domain, limit=limit)
```

#### Tarea 1.4: Vistas Básicas
```xml
<!-- views/ai_conversation_views.xml -->
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    
    <!-- Vista de formulario para conversaciones IA -->
    <record id="view_ai_conversation_form" model="ir.ui.view">
        <field name="name">ai.conversation.form</field>
        <field name="model">ai.conversation</field>
        <field name="arch" type="xml">
            <form string="Conversación IA">
                <header>
                    <button name="action_start_conversation" 
                            string="Iniciar Conversación" 
                            type="object" 
                            class="btn-primary"
                            attrs="{'invisible': [('state', '!=', 'initiated')]}"/>
                    <field name="state" widget="statusbar" statusbar_visible="initiated,equipment_selected,work_in_progress,completed"/>
                </header>
                <sheet>
                    <div class="oe_title">
                        <h1>
                            <field name="name" readonly="1"/>
                        </h1>
                    </div>
                    <group>
                        <group>
                            <field name="fsm_order_id"/>
                            <field name="technician_id"/>
                            <field name="current_equipment_id"/>
                        </group>
                        <group>
                            <field name="channel_id"/>
                            <field name="message_count"/>
                            <field name="duration" widget="float_time"/>
                        </group>
                    </group>
                    <notebook>
                        <page string="Contexto">
                            <field name="context_data" widget="ace" options="{'mode': 'json'}"/>
                        </page>
                        <page string="Resumen">
                            <field name="conversation_summary" placeholder="Resumen automático de la conversación..."/>
                        </page>
                        <page string="Reporte">
                            <group>
                                <field name="report_generated"/>
                                <field name="report_url" widget="url" attrs="{'invisible': [('report_url', '=', False)]}"/>
                            </group>
                        </page>
                    </notebook>
                </sheet>
                <div class="oe_chatter">
                    <field name="message_ids"/>
                    <field name="activity_ids"/>
                </div>
            </form>
        </field>
    </record>
    
    <!-- Vista de lista para conversaciones IA -->
    <record id="view_ai_conversation_tree" model="ir.ui.view">
        <field name="name">ai.conversation.tree</field>
        <field name="model">ai.conversation</field>
        <field name="arch" type="xml">
            <tree string="Conversaciones IA">
                <field name="name"/>
                <field name="fsm_order_id"/>
                <field name="technician_id"/>
                <field name="state" decoration-info="state=='initiated'" decoration-warning="state=='work_in_progress'" decoration-success="state=='completed'"/>
                <field name="message_count"/>
                <field name="duration" widget="float_time"/>
                <field name="create_date"/>
            </tree>
        </field>
    </record>
    
    <!-- Acción para conversaciones IA -->
    <record id="action_ai_conversation" model="ir.actions.act_window">
        <field name="name">Conversaciones IA</field>
        <field name="res_model">ai.conversation</field>
        <field name="view_mode">tree,form</field>
        <field name="help" type="html">
            <p class="o_view_nocontent_smiling_face">
                ¡Crea tu primera conversación con el Asistente IA!
            </p>
            <p>
                Las conversaciones IA guían a los técnicos durante los servicios de campo,
                proporcionando acceso a la base de conocimiento y generando reportes automáticamente.
            </p>
        </field>
    </record>

</odoo>
```

#### Tarea 1.5: Seguridad y Permisos
```csv
# security/ir.model.access.csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_ai_conversation_user,ai.conversation.user,model_ai_conversation,base.group_user,1,1,1,0
access_ai_conversation_manager,ai.conversation.manager,model_ai_conversation,patco_base.group_patco_administrator,1,1,1,1
access_ai_knowledge_base_user,ai.knowledge.base.user,model_ai_knowledge_base,base.group_user,1,0,0,0
access_ai_knowledge_base_manager,ai.knowledge.base.manager,model_ai_knowledge_base,patco_base.group_patco_administrator,1,1,1,1
```

#### Criterios de Aceptación Fase 1
- [ ] Módulo patco_ai_agent instalable sin errores
- [ ] Modelos ai.conversation e ir.attachment extendido funcionando
- [ ] Vistas básicas accesibles desde menú
- [ ] Permisos configurados correctamente
- [ ] Conversación básica creatable manualmente
- [ ] Tests unitarios básicos pasando

---

## 🗄️ Fase 2: Extensión PostgreSQL + PGVector (3-5 días)

### Objetivos
- Configurar PGVector en PostgreSQL existente
- Crear tablas para embeddings vectoriales
- Validar operaciones vectoriales básicas

### Tareas Específicas

#### Tarea 2.1: Instalación PGVector Automatizada
```dockerfile
# ai-services/pgvector-setup/Dockerfile
FROM postgres:15

RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    postgresql-server-dev-15 \
    && rm -rf /var/lib/apt/lists/*

RUN git clone --branch v0.5.1 https://github.com/pgvector/pgvector.git \
    && cd pgvector \
    && make \
    && make install

COPY setup-pgvector.sql /docker-entrypoint-initdb.d/
```

```sql
-- ai-services/pgvector-setup/setup-pgvector.sql
-- Crear extensión pgvector
CREATE EXTENSION IF NOT EXISTS vector;

-- Crear tabla para embeddings de documentos
CREATE TABLE IF NOT EXISTS ai_document_embeddings (
    id SERIAL PRIMARY KEY,
    attachment_id INTEGER NOT NULL,
    chunk_index INTEGER DEFAULT 0,
    content TEXT NOT NULL,
    embedding vector(768),  -- Dimensión para Gemini embeddings
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices para búsqueda eficiente
CREATE INDEX IF NOT EXISTS ai_document_embeddings_attachment_idx 
ON ai_document_embeddings(attachment_id);

CREATE INDEX IF NOT EXISTS ai_document_embeddings_embedding_idx 
ON ai_document_embeddings USING hnsw (embedding vector_cosine_ops);

-- Función para búsqueda de similitud
CREATE OR REPLACE FUNCTION search_similar_documents(
    query_embedding vector(768),
    similarity_threshold float DEFAULT 0.7,
    max_results integer DEFAULT 10
)
RETURNS TABLE(
    attachment_id integer,
    chunk_index integer,
    content text,
    similarity float,
    metadata jsonb
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        e.attachment_id,
        e.chunk_index,
        e.content,
        1 - (e.embedding <=> query_embedding) as similarity,
        e.metadata
    FROM ai_document_embeddings e
    WHERE 1 - (e.embedding <=> query_embedding) > similarity_threshold
    ORDER BY e.embedding <=> query_embedding
    LIMIT max_results;
END;
$$ LANGUAGE plpgsql;
```

#### Tarea 2.2: Actualización Docker Compose
```yaml
# Actualizar docker-compose.ai.yml
version: '3.8'

services:
  pgvector-setup:
    build:
      context: ./ai-services/pgvector-setup
      dockerfile: Dockerfile
    depends_on:
      db:
        condition: service_healthy
    environment:
      - PGHOST=db
      - PGPORT=5432
      - PGUSER=odoo
      - PGPASSWORD=P4tc0_2
      - PGDATABASE=odoo_patco
    command: >
      bash -c "
        echo 'Configurando PGVector...' &&
        sleep 10 &&
        psql -c 'CREATE EXTENSION IF NOT EXISTS vector;' &&
        psql -f /docker-entrypoint-initdb.d/setup-pgvector.sql &&
        echo 'PGVector configurado correctamente'
      "
    networks:
      - odoo-network
    restart: "no"

networks:
  odoo-network:
    external: true
    name: odoo-patco-network
```

#### Tarea 2.3: Validación de Funcionalidad
```python
# ai-services/pgvector-setup/test_pgvector.py
import psycopg2
import numpy as np
from psycopg2.extras import register_adapter, Json
import json

def test_pgvector_functionality():
    """Prueba funcionalidad básica de PGVector"""
    
    # Conexión a la base de datos
    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        database="odoo_patco",
        user="odoo",
        password="P4tc0_2"
    )
    
    cur = conn.cursor()
    
    try:
        # Verificar que la extensión está instalada
        cur.execute("SELECT extname FROM pg_extension WHERE extname = 'vector';")
        result = cur.fetchone()
        assert result is not None, "Extensión vector no encontrada"
        print("✓ Extensión pgvector instalada correctamente")
        
        # Probar inserción de vector
        test_embedding = np.random.rand(768).tolist()
        cur.execute("""
            INSERT INTO ai_document_embeddings 
            (attachment_id, content, embedding, metadata) 
            VALUES (%s, %s, %s, %s)
        """, (
            999,  # ID de prueba
            "Documento de prueba para validar PGVector",
            test_embedding,
            json.dumps({"test": True, "category": "validation"})
        ))
        
        # Probar búsqueda de similitud
        query_embedding = np.random.rand(768).tolist()
        cur.execute("""
            SELECT attachment_id, content, 
                   1 - (embedding <=> %s::vector) as similarity
            FROM ai_document_embeddings 
            WHERE attachment_id = 999
            ORDER BY embedding <=> %s::vector
            LIMIT 1
        """, (query_embedding, query_embedding))
        
        result = cur.fetchone()
        assert result is not None, "No se pudo recuperar el documento de prueba"
        print(f"✓ Búsqueda vectorial funcionando - Similitud: {result[2]:.4f}")
        
        # Limpiar datos de prueba
        cur.execute("DELETE FROM ai_document_embeddings WHERE attachment_id = 999")
        
        conn.commit()
        print("✓ Todas las pruebas de PGVector pasaron correctamente")
        
    except Exception as e:
        print(f"✗ Error en pruebas de PGVector: {e}")
        conn.rollback()
        raise
    
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    test_pgvector_functionality()
```

#### Criterios de Aceptación Fase 2
- [ ] Extensión PGVector instalada en PostgreSQL
- [ ] Tablas de embeddings creadas correctamente
- [ ] Índices HNSW funcionando
- [ ] Funciones de búsqueda de similitud operativas
- [ ] Tests de validación pasando
- [ ] Documentación de esquema actualizada

---

## 📚 Fase 3: Indexador de Documentos (1 semana)

### Objetivos
- Crear servicio de indexación automática de documentos
- Implementar procesadores para diferentes tipos de archivos
- Generar embeddings con Gemini API

### Tareas Específicas

#### Tarea 3.1: Servicio Base de Indexación
```python
# ai-services/indexer/indexer.py
import asyncio
import logging
from pathlib import Path
import psycopg2
from psycopg2.extras import Json
import requests
import json
import hashlib
from typing import List, Dict, Any
import os
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DocumentIndexer:
    def __init__(self):
        self.db_url = os.getenv("DATABASE_URL")
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.odoo_url = os.getenv("ODOO_URL", "http://odoo:8069")
        self.batch_size = 50
        
    async def connect_db(self):
        """Conecta a PostgreSQL"""
        self.conn = psycopg2.connect(self.db_url)
        self.cursor = self.conn.cursor()
        
    async def get_pending_documents(self) -> List[Dict]:
        """Obtiene documentos pendientes de indexación desde Odoo"""
        
        # Query para obtener attachments no indexados
        query = """
        SELECT 
            id, name, datas, mimetype, res_model, res_id,
            x_document_type, x_content_hash
        FROM ir_attachment 
        WHERE 
            x_is_indexed = FALSE 
            AND datas IS NOT NULL
            AND mimetype IN ('application/pdf', 'text/plain', 'image/jpeg', 'image/png')
        LIMIT %s
        """
        
        self.cursor.execute(query, (self.batch_size,))
        columns = [desc[0] for desc in self.cursor.description]
        
        documents = []
        for row in self.cursor.fetchall():
            doc = dict(zip(columns, row))
            documents.append(doc)
            
        logger.info(f"Encontrados {len(documents)} documentos pendientes de indexación")
        return documents
    
    async def process_document(self, document: Dict) -> List[Dict]:
        """Procesa un documento y genera chunks con embeddings"""
        
        try:
            # Determinar procesador según tipo MIME
            processor = self._get_processor(document['mimetype'])
            
            # Extraer texto del documento
            text_chunks = await processor.extract_text(document)
            
            # Generar embeddings para cada chunk
            embeddings_data = []
            for i, chunk in enumerate(text_chunks):
                embedding = await self._generate_embedding(chunk['content'])
                
                embeddings_data.append({
                    'attachment_id': document['id'],
                    'chunk_index': i,
                    'content': chunk['content'],
                    'embedding': embedding,
                    'metadata': {
                        'document_name': document['name'],
                        'document_type': document['x_document_type'],
                        'mimetype': document['mimetype'],
                        'chunk_length': len(chunk['content']),
                        'page_number': chunk.get('page_number'),
                        'processed_at': datetime.now().isoformat()
                    }
                })
            
            return embeddings_data
            
        except Exception as e:
            logger.error(f"Error procesando documento {document['id']}: {e}")
            return []
    
    async def _generate_embedding(self, text: str) -> List[float]:
        """Genera embedding usando Gemini API"""
        
        url = "https://generativelanguage.googleapis.com/v1beta/models/embedding-001:embedContent"
        
        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": self.gemini_api_key
        }
        
        data = {
            "model": "models/embedding-001",
            "content": {
                "parts": [{"text": text}]
            }
        }
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            embedding = result['embedding']['values']
            
            # Validar dimensión del embedding
            if len(embedding) != 768:
                raise ValueError(f"Embedding dimension mismatch: {len(embedding)} != 768")
            
            return embedding
            
        except Exception as e:
            logger.error(f"Error generando embedding: {e}")
            raise
    
    def _get_processor(self, mimetype: str):
        """Retorna el procesador apropiado según tipo MIME"""
        
        if mimetype == 'application/pdf':
            from processors.pdf_processor import PDFProcessor
            return PDFProcessor()
        elif mimetype == 'text/plain':
            from processors.text_processor import TextProcessor
            return TextProcessor()
        elif mimetype in ['image/jpeg', 'image/png']:
            from processors.image_processor import ImageProcessor
            return ImageProcessor()
        else:
            raise ValueError(f"Tipo MIME no soportado: {mimetype}")
    
    async def save_embeddings(self, embeddings_data: List[Dict]):
        """Guarda embeddings en PostgreSQL"""
        
        if not embeddings_data:
            return
        
        # Preparar datos para inserción batch
        insert_query = """
        INSERT INTO ai_document_embeddings 
        (attachment_id, chunk_index, content, embedding, metadata)
        VALUES %s
        """
        
        values = []
        for data in embeddings_data:
            values.append((
                data['attachment_id'],
                data['chunk_index'],
                data['content'],
                data['embedding'],
                Json(data['metadata'])
            ))
        
        # Inserción batch usando execute_values
        from psycopg2.extras import execute_values
        execute_values(
            self.cursor,
            insert_query,
            values,
            template=None,
            page_size=100
        )
        
        # Marcar documento como indexado en Odoo
        attachment_ids = list(set(data['attachment_id'] for data in embeddings_data))
        update_query = """
        UPDATE ir_attachment 
        SET x_is_indexed = TRUE, x_indexed_date = %s
        WHERE id = ANY(%s)
        """
        
        self.cursor.execute(update_query, (datetime.now(), attachment_ids))
        self.conn.commit()
        
        logger.info(f"Guardados {len(embeddings_data)} embeddings para {len(attachment_ids)} documentos")
    
    async def run_indexing_cycle(self):
        """Ejecuta un ciclo completo de indexación"""
        
        try:
            await self.connect_db()
            
            # Obtener documentos pendientes
            documents = await self.get_pending_documents()
            
            if not documents:
                logger.info("No hay documentos pendientes de indexación")
                return
            
            # Procesar cada documento
            total_embeddings = 0
            for document in documents:
                logger.info(f"Procesando documento: {document['name']} (ID: {document['id']})")
                
                embeddings_data = await self.process_document(document)
                
                if embeddings_data:
                    await self.save_embeddings(embeddings_data)
                    total_embeddings += len(embeddings_data)
                else:
                    # Marcar como error de indexación
                    self.cursor.execute("""
                        UPDATE ir_attachment 
                        SET x_indexing_error = 'Error durante procesamiento'
                        WHERE id = %s
                    """, (document['id'],))
                    self.conn.commit()
            
            logger.info(f"Ciclo de indexación completado: {total_embeddings} embeddings generados")
            
        except Exception as e:
            logger.error(f"Error en ciclo de indexación: {e}")
            if hasattr(self, 'conn'):
                self.conn.rollback()
        
        finally:
            if hasattr(self, 'cursor'):
                self.cursor.close()
            if hasattr(self, 'conn'):
                self.conn.close()

async def main():
    """Función principal del indexador"""
    
    indexer = DocumentIndexer()
    
    # Modo watch: ejecutar continuamente
    if "--watch" in sys.argv:
        logger.info("Iniciando indexador en modo watch...")
        
        while True:
            await indexer.run_indexing_cycle()
            await asyncio.sleep(300)  # 5 minutos entre ciclos
    
    # Modo single: ejecutar una vez
    else:
        logger.info("Ejecutando ciclo único de indexación...")
        await indexer.run_indexing_cycle()

if __name__ == "__main__":
    import sys
    asyncio.run(main())
```

#### Tarea 3.2: Procesadores de Documentos
```python
# ai-services/indexer/processors/text_processor.py
import base64
from typing import List, Dict

class TextProcessor:
    def __init__(self):
        self.chunk_size = 1000  # Caracteres por chunk
        self.overlap = 200      # Solapamiento entre chunks
    
    async def extract_text(self, document: Dict) -> List[Dict]:
        """Extrae texto de documento de texto plano"""
        
        # Decodificar contenido base64
        content_bytes = base64.b64decode(document['datas'])
        text = content_bytes.decode('utf-8', errors='ignore')
        
        # Dividir en chunks
        chunks = self._split_text(text)
        
        return [
            {
                'content': chunk,
                'page_number': None
            }
            for chunk in chunks
        ]
    
    def _split_text(self, text: str) -> List[str]:
        """Divide texto en chunks con solapamiento"""
        
        if len(text) <= self.chunk_size:
            return [text]
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + self.chunk_size
            
            # Si no es el último chunk, buscar un punto de corte natural
            if end < len(text):
                # Buscar el último espacio o salto de línea antes del límite
                for i in range(end, start + self.chunk_size - 100, -1):
                    if text[i] in [' ', '\n', '.', '!', '?']:
                        end = i + 1
                        break
            
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            # Calcular siguiente posición con solapamiento
            start = end - self.overlap
            if start >= len(text):
                break
        
        return chunks
```

```python
# ai-services/indexer/processors/pdf_processor.py
import base64
import PyPDF2
import io
from typing import List, Dict

class PDFProcessor:
    def __init__(self):
        self.chunk_size = 1000
        self.overlap = 200
    
    async def extract_text(self, document: Dict) -> List[Dict]:
        """Extrae texto de documento PDF"""
        
        try:
            # Decodificar PDF desde base64
            pdf_bytes = base64.b64decode(document['datas'])
            pdf_file = io.BytesIO(pdf_bytes)
            
            # Leer PDF
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            chunks = []
            for page_num, page in enumerate(pdf_reader.pages):
                page_text = page.extract_text()
                
                if page_text.strip():
                    # Dividir página en chunks
                    page_chunks = self._split_text(page_text)
                    
                    for chunk in page_chunks:
                        chunks.append({
                            'content': chunk,
                            'page_number': page_num + 1
                        })
            
            return chunks
            
        except Exception as e:
            raise Exception(f"Error procesando PDF: {e}")
    
    def _split_text(self, text: str) -> List[str]:
        """Divide texto en chunks (mismo método que TextProcessor)"""
        # Implementación idéntica a TextProcessor
        pass
```

#### Tarea 3.3: Dockerfile y Configuración
```dockerfile
# ai-services/indexer/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . .

# Comando por defecto
CMD ["python", "indexer.py"]
```

```txt
# ai-services/indexer/requirements.txt
asyncio
psycopg2-binary
requests
PyPDF2
Pillow
python-magic
numpy
```

#### Criterios de Aceptación Fase 3
- [ ] Servicio de indexación ejecutándose correctamente
- [ ] Procesadores para PDF y texto funcionando
- [ ] Embeddings generándose con Gemini API
- [ ] Documentos marcándose como indexados en Odoo
- [ ] Logs estructurados y monitoreo básico
- [ ] Manejo de errores robusto

---

## 🔌 Fase 4: Servidor MCP Básico (1 semana)

### Objetivos
- Implementar servidor MCP para conectividad Odoo-IA
- Crear herramientas básicas para FSM y equipos
- Validar comunicación bidireccional

### Tareas Específicas

#### Tarea 4.1: Servidor MCP Base
```python
# ai-services/mcp/server.py
import asyncio
import json
import logging
from typing import Any, Dict, List
from mcp import Server, types
from mcp.server.models import InitializationOptions
import aiohttp
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OdooMCPServer:
    def __init__(self):
        self.server = Server("patco-mcp-server")
        self.odoo_url = os.getenv("ODOO_URL", "http://odoo:8069")
        self.odoo_db = os.getenv("ODOO_DB", "odoo_patco")
        self.odoo_username = os.getenv("ODOO_USERNAME")
        self.odoo_password = os.getenv("ODOO_PASSWORD")
        self.session = None
        
        # Registrar handlers
        self._register_handlers()
    
    def _register_handlers(self):
        """Registra todos los handlers del servidor MCP"""
        
        @self.server.list_tools()
        async def handle_list_tools() -> List[types.Tool]:
            """Lista todas las herramientas disponibles"""
            return [
                types.Tool(
                    name="get_fsm_order",
                    description="Obtiene información completa de una orden FSM",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "order_id": {
                                "type": "integer",
                                "description": "ID de la orden FSM"
                            }
                        },
                        "required": ["order_id"]
                    }
                ),
                types.Tool(
                    name="update_fsm_order",
                    description="Actualiza campos de una orden FSM",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "order_id": {
                                "type": "integer",
                                "description": "ID de la orden FSM"
                            },
                            "values": {
                                "type": "object",
                                "description": "Campos a actualizar"
                            }
                        },
                        "required": ["order_id", "values"]
                    }
                ),
                types.Tool(
                    name="get_equipment_info",
                    description="Obtiene información detallada de un equipo",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "equipment_id": {
                                "type": "integer",
                                "description": "ID del equipo"
                            }
                        },
                        "required": ["equipment_id"]
                    }
                ),
                types.Tool(
                    name="search_knowledge_base",
                    description="Busca información en la base de conocimiento",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Consulta de búsqueda"
                            },
                            "equipment_category_id": {
                                "type": "integer",
                                "description": "ID de categoría de equipo (opcional)"
                            },
                            "limit": {
                                "type": "integer",
                                "description": "Número máximo de resultados",
                                "default": 5
                            }
                        },
                        "required": ["query"]
                    }
                ),
                types.Tool(
                    name="create_ai_conversation",
                    description="Crea una nueva conversación IA para una orden FSM",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "fsm_order_id": {
                                "type": "integer",
                                "description": "ID de la orden FSM"
                            },
                            "technician_id": {
                                "type": "integer",
                                "description": "ID del técnico"
                            }
                        },
                        "required": ["fsm_order_id", "technician_id"]
                    }
                )
            ]
        
        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[types.TextContent]:
            """Ejecuta herramienta específica"""
            
            try:
                # Asegurar autenticación
                await self._ensure_authenticated()
                
                if name == "get_fsm_order":
                    result = await self._get_fsm_order(arguments["order_id"])
                
                elif name == "update_fsm_order":
                    result = await self._update_fsm_order(
                        arguments["order_id"], 
                        arguments["values"]
                    )
                
                elif name == "get_equipment_info":
                    result = await self._get_equipment_info(arguments["equipment_id"])
                
                elif name == "search_knowledge_base":
                    result = await self._search_knowledge_base(
                        arguments["query"],
                        arguments.get("equipment_category_id"),
                        arguments.get("limit", 5)
                    )
                
                elif name == "create_ai_conversation":
                    result = await self._create_ai_conversation(
                        arguments["fsm_order_id"],
                        arguments["technician_id"]
                    )
                
                else:
                    raise ValueError(f"Herramienta desconocida: {name}")
                
                return [types.TextContent(
                    type="text",
                    text=json.dumps(result, indent=2, ensure_ascii=False)
                )]
                
            except Exception as e:
                logger.error(f"Error ejecutando herramienta {name}: {e}")
                return [types.TextContent(
                    type="text",
                    text=f"Error: {str(e)}"
                )]
    
    async def _ensure_authenticated(self):
        """Asegura que tenemos una sesión autenticada con Odoo"""
        
        if self.session is None:
            self.session = aiohttp.ClientSession()
        
        # Intentar autenticación
        auth_url = f"{self.odoo_url}/web/session/authenticate"
        auth_data = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "db": self.odoo_db,
                "login": self.odoo_username,
                "password": self.odoo_password
            },
            "id": 1
        }
        
        async with self.session.post(auth_url, json=auth_data) as response:
            result = await response.json()
            
            if result.get("error"):
                raise Exception(f"Error de autenticación: {result['error']}")
            
            if not result.get("result", {}).get("uid"):
                raise Exception("Autenticación fallida")
        
        logger.info("Autenticación con Odoo exitosa")
    
    async def _odoo_call(self, model: str, method: str, args: List = None, kwargs: Dict = None):
        """Realiza llamada RPC a Odoo"""
        
        if args is None:
            args = []
        if kwargs is None:
            kwargs = {}
        
        call_url = f"{self.odoo_url}/web/dataset/call_kw"
        call_data = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "model": model,
                "method": method,
                "args": args,
                "kwargs": kwargs
            },
            "id": 1
        }
        
        async with self.session.post(call_url, json=call_data) as response:
            result = await response.json()
            
            if result.get("error"):
                raise Exception(f"Error en llamada Odoo: {result['error']}")
            
            return result.get("result")
    
    async def _get_fsm_order(self, order_id: int) -> Dict:
        """Obtiene información completa de orden FSM"""
        
        # Campos a obtener
        fields = [
            'name', 'partner_id', 'location_id', 'person_id', 'stage_id',
            'equipment_ids', 'x_service_nature_id', 'x_service_area_id',
            'x_service_complexity_id', 'x_required_skill_ids', 'description',
            'date_start', 'date_end', 'x_timer_status', 'x_total_timesheet_time'
        ]
        
        order_data = await self._odoo_call(
            'fsm.order', 
            'read', 
            [[order_id]], 
            {'fields': fields}
        )
        
        if not order_data:
            raise Exception(f"Orden FSM {order_id} no encontrada")
        
        order = order_data[0]
        
        # Obtener información adicional de equipos
        if order['equipment_ids']:
            equipment_data = await self._odoo_call(
                'maintenance.equipment',
                'read',
                [order['equipment_ids']],
                {'fields': ['name', 'category_id', 'x_patco_code', 'x_technical_specs']}
            )
            order['equipment_details'] = equipment_data
        
        return order
    
    async def _update_fsm_order(self, order_id: int, values: Dict) -> Dict:
        """Actualiza orden FSM"""
        
        result = await self._odoo_call(
            'fsm.order',
            'write',
            [[order_id], values]
        )
        
        return {
            "success": result,
            "order_id": order_id,
            "updated_fields": list(values.keys())
        }
    
    async def _get_equipment_info(self, equipment_id: int) -> Dict:
        """Obtiene información detallada de equipo"""
        
        fields = [
            'name', 'category_id', 'x_patco_code', 'x_technical_specs',
            'x_operating_conditions', 'x_installation_date', 'x_warranty_expiry',
            'partner_id', 'x_service_location_id'
        ]
        
        equipment_data = await self._odoo_call(
            'maintenance.equipment',
            'read',
            [[equipment_id]],
            {'fields': fields}
        )
        
        if not equipment_data:
            raise Exception(f"Equipo {equipment_id} no encontrado")
        
        equipment = equipment_data[0]
        
        # Obtener checklists de la categoría
        if equipment['category_id']:
            category_data = await self._odoo_call(
                'maintenance.equipment.category',
                'read',
                [[equipment['category_id'][0]]],
                {'fields': ['x_checklist_entry_template', 'x_checklist_exit_template']}
            )
            
            if category_data:
                equipment['checklists'] = category_data[0]
        
        return equipment
    
    async def _search_knowledge_base(self, query: str, equipment_category_id: int = None, limit: int = 5) -> Dict:
        """Busca en la base de conocimiento usando RAG"""
        
        # Por ahora implementación básica - se mejorará con RAG real
        domain = [
            ('x_is_indexed', '=', True),
            '|', '|',
            ('name', 'ilike', query),
            ('description', 'ilike', query),
            ('index_content', 'ilike', query)
        ]
        
        if equipment_category_id:
            domain.append(('x_equipment_category_ids', 'in', [equipment_category_id]))
        
        results = await self._odoo_call(
            'ir.attachment',
            'search_read',
            [domain],
            {
                'fields': ['name', 'description', 'x_document_type', 'mimetype'],
                'limit': limit
            }
        )
        
        return {
            "query": query,
            "results_count": len(results),
            "results": results
        }
    
    async def _create_ai_conversation(self, fsm_order_id: int, technician_id: int) -> Dict:
        """Crea nueva conversación IA"""
        
        conversation_data = {
            'fsm_order_id': fsm_order_id,
            'technician_id': technician_id,
            'state': 'initiated'
        }
        
        conversation_id = await self._odoo_call(
            'ai.conversation',
            'create',
            [conversation_data]
        )
        
        # Iniciar conversación
        await self._odoo_call(
            'ai.conversation',
            'action_start_conversation',
            [[conversation_id]]
        )
        
        return {
            "conversation_id": conversation_id,
            "fsm_order_id": fsm_order_id,
            "technician_id": technician_id,
            "status": "created_and_started"
        }
    
    async def run(self):
        """Ejecuta el servidor MCP"""
        
        try:
            # Configurar transporte stdio
            from mcp.server.stdio import stdio_server
            
            async with stdio_server() as (read_stream, write_stream):
                logger.info("Servidor MCP iniciado")
                
                await self.server.run(
                    read_stream,
                    write_stream,
                    InitializationOptions(
                        server_name="patco-mcp-server",
                        server_version="1.0.0"
                    )
                )
        
        except Exception as e:
            logger.error(f"Error ejecutando servidor MCP: {e}")
            raise
        
        finally:
            if self.session:
                await self.session.close()

async def main():
    """Función principal"""
    server = OdooMCPServer()
    await server.run()

if __name__ == "__main__":
    asyncio.run(main())
```

#### Criterios de Aceptación Fase 4
- [ ] Servidor MCP ejecutándose correctamente
- [ ] Herramientas básicas funcionando (get_fsm_order, update_fsm_order)
- [ ] Autenticación con Odoo operativa
- [ ] Comunicación bidireccional validada
- [ ] Manejo de errores robusto
- [ ] Logs estructurados

---

## 🤖 Fase 5: LangGraph Core (1.5 semanas)

### Objetivos
- Implementar orquestador conversacional con LangGraph
- Crear grafo de estados para flujo de servicio técnico
- Integrar con servidor MCP

### Tareas Específicas

#### Tarea 5.1: Servidor LangGraph Base
```python
# ai-services/langgraph/main.py
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
import asyncio
import logging
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.postgres import AsyncPostgresSaver
from datetime import datetime
import os
import json

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Modelos Pydantic
class ConversationMessage(BaseModel):
    role: str
    content: str
    timestamp: Optional[datetime] = None
    metadata: Optional[Dict[str, Any]] = None

class ConversationState(BaseModel):
    messages: List[ConversationMessage] = []
    fsm_order_id: Optional[int] = None
    technician_id: Optional[int] = None
    current_equipment_id: Optional[int] = None
    context: Dict[str, Any] = {}
    current_intent: Optional[str] = None
    entities: Dict[str, Any] = {}
    response: Optional[str] = None
    actions: List[Dict[str, Any]] = []
    conversation_state: str = "initiated"

class ProcessMessageRequest(BaseModel):
    conversation_id: str
    message: ConversationMessage
    context: Optional[Dict[str, Any]] = None

# Aplicación FastAPI
app = FastAPI(
    title="PATCO AI Agent - LangGraph Server",
    description="Servidor de orquestación conversacional para agente IA PATCO",
    version="1.0.0"
)

# Configuración global
DB_URI = os.getenv("DATABASE_URL")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Checkpointer para persistencia
checkpointer = None

@app.on_event("startup")
async def startup_event():
    """Inicialización del servidor"""
    global checkpointer
    
    try:
        # Configurar checkpointer con PostgreSQL
        checkpointer = AsyncPostgresSaver.from_conn_string(DB_URI)
        await checkpointer.setup()
        
        logger.info("Servidor LangGraph iniciado correctamente")
        
    except Exception as e:
        logger.error(f"Error en startup: {e}")
        raise

# Importar nodos del grafo
from nodes.message_processor import process_message
from nodes.context_retriever import retrieve_context
from nodes.rag_search import perform_rag_search
from nodes.action_planner import plan_actions
from nodes.response_generator import generate_response
from nodes.action_executor import execute_actions

# Función de enrutamiento
def route_by_intent(state: ConversationState) -> str:
    """Enruta según la intención detectada"""
    
    intent = state.current_intent
    
    if intent == "question":
        return "rag_search"
    elif intent == "action":
        return "action_planner"
    elif intent == "status_update":
        return "context_retriever"
    else:
        return "response_generator"

# Construcción del grafo
def build_conversation_graph():
    """Construye el grafo de conversación"""
    
    workflow = StateGraph(ConversationState)
    
    # Agregar nodos
    workflow.add_node("message_processor", process_message)
    workflow.add_node("context_retriever", retrieve_context)
    workflow.add_node("rag_search", perform_rag_search)
    workflow.add_node("action_planner", plan_actions)
    workflow.add_node("response_generator", generate_response)
    workflow.add_node("action_executor", execute_actions)
    
    # Definir edges
    workflow.add_edge(START, "message_processor")
    
    # Edges condicionales
    workflow.add_conditional_edges(
        "message_processor",
        route_by_intent,
        {
            "question": "rag_search",
            "action": "action_planner", 
            "status_update": "context_retriever",
            "default": "response_generator"
        }
    )
    
    workflow.add_edge("context_retriever", "response_generator")
    workflow.add_edge("rag_search", "response_generator")
    workflow.add_edge("action_planner", "action_executor")
    workflow.add_edge("action_executor", "response_generator")
    workflow.add_edge("response_generator", END)
    
    # Compilar grafo
    return workflow.compile(checkpointer=checkpointer)

# Instancia global del grafo
conversation_graph = None

@app.on_event("startup")
async def build_graph():
    """Construye el grafo al iniciar"""
    global conversation_graph
    conversation_graph = build_conversation_graph()
    logger.info("Grafo de conversación construido")

@app.post("/conversation/{conversation_id}/message")
async def process_conversation_message(
    conversation_id: str,
    request: ProcessMessageRequest
):
    """Procesa mensaje en conversación específica"""
    
    try:
        config = {"configurable": {"thread_id": conversation_id}}
        
        # Preparar estado inicial
        initial_state = ConversationState(
            messages=[request.message],
            context=request.context or {}
        )
        
        # Ejecutar grafo
        result = await conversation_graph.ainvoke(
            initial_state.dict(),
            config=config
        )
        
        return {
            "conversation_id": conversation_id,
            "response": result.get("response"),
            "actions": result.get("actions", []),
            "conversation_state": result.get("conversation_state"),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error procesando mensaje: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/conversation/{conversation_id}/history")
async def get_conversation_history(conversation_id: str):
    """Obtiene historial de conversación"""
    
    try:
        config = {"configurable": {"thread_id": conversation_id}}
        
        # Obtener estado actual del checkpointer
        checkpoint = await checkpointer.aget(config)
        
        if not checkpoint:
            return {"conversation_id": conversation_id, "messages": []}
        
        return {
            "conversation_id": conversation_id,
            "messages": checkpoint.get("messages", []),
            "state": checkpoint.get("conversation_state", "unknown")
        }
        
    except Exception as e:
        logger.error(f"Error obteniendo historial: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Endpoint de salud"""
    return {
        "status": "healthy",
        "service": "langgraph-server",
        "timestamp": datetime.now().isoformat()
    }

#### Tarea 5.2: Nodos del Grafo LangGraph
```python
# ai-services/langgraph/nodes/message_processor.py
import logging
from typing import Dict, Any
import google.generativeai as genai
import os

logger = logging.getLogger(__name__)

# Configurar Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

async def process_message(state: Dict[str, Any]) -> Dict[str, Any]:
    """Procesa mensaje del técnico y determina intención"""
    
    try:
        messages = state.get("messages", [])
        if not messages:
            return state
        
        last_message = messages[-1]
        message_content = last_message.get("content", "")
        
        # Prompt para análisis de intención
        intent_prompt = f"""
        Analiza el siguiente mensaje de un técnico de campo y determina la intención principal:
        
        Mensaje: "{message_content}"
        
        Intenciones posibles:
        - question: El técnico hace una pregunta técnica o solicita información
        - action: El técnico quiere realizar una acción (actualizar estado, registrar datos, etc.)
        - status_update: El técnico reporta el estado actual o progreso
        - greeting: Saludo o mensaje inicial
        - other: Otro tipo de mensaje
        
        Responde solo con la intención (una palabra).
        """
        
        # Llamar a Gemini para análisis de intención
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(intent_prompt)
        intent = response.text.strip().lower()
        
        # Extraer entidades básicas
        entities = await extract_entities(message_content, state.get("context", {}))
        
        # Actualizar estado
        state["current_intent"] = intent
        state["entities"] = entities
        
        logger.info(f"Mensaje procesado - Intención: {intent}")
        
        return state
        
    except Exception as e:
        logger.error(f"Error procesando mensaje: {e}")
        state["current_intent"] = "other"
        state["entities"] = {}
        return state

async def extract_entities(message: str, context: Dict) -> Dict[str, Any]:
    """Extrae entidades del mensaje"""
    
    entities = {}
    
    # Extracciones básicas con regex/keywords
    import re
    
    # Buscar números (mediciones, IDs, etc.)
    numbers = re.findall(r'\d+\.?\d*', message)
    if numbers:
        entities["numbers"] = numbers
    
    # Buscar menciones de equipos
    equipment_keywords = ["equipo", "horno", "refrigerador", "aire", "cocina", "lavadora"]
    for keyword in equipment_keywords:
        if keyword.lower() in message.lower():
            entities["equipment_mentioned"] = keyword
            break
    
    # Buscar estados/acciones
    action_keywords = {
        "iniciar": "start",
        "comenzar": "start", 
        "terminar": "finish",
        "completar": "complete",
        "problema": "issue",
        "error": "error",
        "funciona": "working",
        "reparado": "fixed"
    }
    
    for keyword, action in action_keywords.items():
        if keyword.lower() in message.lower():
            entities["action"] = action
            break
    
    return entities
```

```python
# ai-services/langgraph/nodes/rag_search.py
import logging
import psycopg2
import json
import os
from typing import Dict, Any, List
import google.generativeai as genai

logger = logging.getLogger(__name__)

async def perform_rag_search(state: Dict[str, Any]) -> Dict[str, Any]:
    """Realiza búsqueda RAG en base de conocimiento"""
    
    try:
        messages = state.get("messages", [])
        if not messages:
            return state
        
        query = messages[-1].get("content", "")
        context = state.get("context", {})
        
        # Generar embedding de la consulta
        query_embedding = await generate_query_embedding(query)
        
        # Buscar documentos similares
        similar_docs = await search_similar_documents(
            query_embedding, 
            context.get("equipment_category_id"),
            limit=5
        )
        
        # Generar respuesta usando RAG
        rag_response = await generate_rag_response(query, similar_docs)
        
        # Actualizar estado
        state["rag_results"] = similar_docs
        state["response"] = rag_response
        
        logger.info(f"RAG search completado - {len(similar_docs)} documentos encontrados")
        
        return state
        
    except Exception as e:
        logger.error(f"Error en RAG search: {e}")
        state["response"] = "Lo siento, no pude encontrar información relevante en este momento."
        return state

async def generate_query_embedding(query: str) -> List[float]:
    """Genera embedding para la consulta"""
    
    try:
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        
        result = genai.embed_content(
            model="models/embedding-001",
            content=query,
            task_type="retrieval_query"
        )
        
        return result['embedding']
        
    except Exception as e:
        logger.error(f"Error generando embedding: {e}")
        raise

async def search_similar_documents(
    query_embedding: List[float], 
    equipment_category_id: int = None,
    limit: int = 5
) -> List[Dict]:
    """Busca documentos similares en PostgreSQL"""
    
    try:
        conn = psycopg2.connect(os.getenv("DATABASE_URL"))
        cursor = conn.cursor()
        
        # Query base con similitud coseno
        base_query = """
        SELECT 
            e.attachment_id,
            e.content,
            e.metadata,
            1 - (e.embedding <=> %s::vector) as similarity
        FROM ai_document_embeddings e
        WHERE 1 - (e.embedding <=> %s::vector) > 0.7
        """
        
        params = [query_embedding, query_embedding]
        
        # Filtrar por categoría si se especifica
        if equipment_category_id:
            base_query += " AND e.metadata->>'equipment_category_id' = %s"
            params.append(str(equipment_category_id))
        
        base_query += " ORDER BY e.embedding <=> %s::vector LIMIT %s"
        params.extend([query_embedding, limit])
        
        cursor.execute(base_query, params)
        results = cursor.fetchall()
        
        documents = []
        for row in results:
            documents.append({
                "attachment_id": row[0],
                "content": row[1],
                "metadata": row[2],
                "similarity": float(row[3])
            })
        
        cursor.close()
        conn.close()
        
        return documents
        
    except Exception as e:
        logger.error(f"Error buscando documentos: {e}")
        return []

async def generate_rag_response(query: str, documents: List[Dict]) -> str:
    """Genera respuesta usando documentos encontrados"""
    
    if not documents:
        return "No encontré información específica sobre tu consulta. ¿Podrías ser más específico?"
    
    # Construir contexto desde documentos
    context_parts = []
    for doc in documents[:3]:  # Usar top 3 documentos
        context_parts.append(f"Documento: {doc['content'][:500]}...")
    
    context = "\n\n".join(context_parts)
    
    # Prompt para generar respuesta
    response_prompt = f"""
    Eres un asistente técnico especializado. Basándote en la siguiente información técnica, 
    responde la pregunta del técnico de manera clara y práctica.
    
    Pregunta del técnico: {query}
    
    Información técnica disponible:
    {context}
    
    Instrucciones:
    - Responde de manera concisa y práctica
    - Si la información no es suficiente, dilo claramente
    - Incluye pasos específicos cuando sea apropiado
    - Usa un tono profesional pero amigable
    
    Respuesta:
    """
    
    try:
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        model = genai.GenerativeModel('gemini-pro')
        
        response = model.generate_content(response_prompt)
        return response.text
        
    except Exception as e:
        logger.error(f"Error generando respuesta RAG: {e}")
        return "Encontré información relevante pero tuve problemas procesándola. ¿Puedes reformular tu pregunta?"
```

#### Criterios de Aceptación Fase 5
- [ ] Servidor LangGraph ejecutándose en puerto 8001
- [ ] Grafo de conversación construido correctamente
- [ ] Nodos básicos funcionando (message_processor, rag_search)
- [ ] Endpoints REST operativos
- [ ] Integración con PostgreSQL para checkpointing
- [ ] Logs estructurados y manejo de errores

---

## 🔗 Fase 6: Integración FSM Básica (1 semana)

### Objetivos
- Conectar conversaciones IA con órdenes FSM
- Implementar disparadores automáticos
- Crear flujo básico técnico-agente

### Tareas Específicas

#### Tarea 6.1: Extensión FSM para IA
```python
# extra-addons/patco_ai_agent/models/fsm_order.py
from odoo import models, fields, api
import logging
import requests
import json

_logger = logging.getLogger(__name__)

class FsmOrder(models.Model):
    _inherit = 'fsm.order'
    
    # Campos para IA
    x_ai_conversation_id = fields.Many2one(
        'ai.conversation', 
        string='Conversación IA',
        help='Conversación activa con el agente IA'
    )
    x_ai_enabled = fields.Boolean(
        'IA Habilitada', 
        default=True,
        help='Habilitar asistente IA para esta orden'
    )
    x_ai_status = fields.Selection([
        ('not_started', 'No Iniciado'),
        ('active', 'Activo'),
        ('completed', 'Completado'),
        ('error', 'Error')
    ], string='Estado IA', default='not_started')
    
    @api.model
    def create(self, vals):
        """Sobrescribir create para disparar IA automáticamente"""
        
        order = super().create(vals)
        
        # Disparar IA si hay técnico asignado y está habilitada
        if order.person_id and order.x_ai_enabled:
            order._trigger_ai_conversation()
        
        return order
    
    def write(self, vals):
        """Sobrescribir write para detectar asignación de técnico"""
        
        result = super().write(vals)
        
        # Si se asigna técnico, disparar IA
        if 'person_id' in vals and vals['person_id']:
            for order in self:
                if order.x_ai_enabled and not order.x_ai_conversation_id:
                    order._trigger_ai_conversation()
        
        return result
    
    def _trigger_ai_conversation(self):
        """Dispara conversación IA automáticamente"""
        
        try:
            if not self.person_id:
                _logger.warning(f"No se puede crear conversación IA para orden {self.name}: sin técnico asignado")
                return
            
            # Crear conversación IA
            conversation = self.env['ai.conversation'].create({
                'fsm_order_id': self.id,
                'technician_id': self.person_id.id,
                'state': 'initiated'
            })
            
            # Vincular conversación a la orden
            self.x_ai_conversation_id = conversation.id
            self.x_ai_status = 'active'
            
            # Iniciar conversación
            conversation.action_start_conversation()
            
            _logger.info(f"Conversación IA creada para orden {self.name} - Técnico: {self.person_id.name}")
            
        except Exception as e:
            _logger.error(f"Error creando conversación IA para orden {self.name}: {e}")
            self.x_ai_status = 'error'
    
    def action_start_ai_conversation(self):
        """Acción manual para iniciar conversación IA"""
        
        self.ensure_one()
        
        if not self.person_id:
            raise UserError("Debe asignar un técnico antes de iniciar la conversación IA")
        
        if self.x_ai_conversation_id:
            # Abrir conversación existente
            return self.x_ai_conversation_id.action_open_conversation()
        else:
            # Crear nueva conversación
            self._trigger_ai_conversation()
            return self.x_ai_conversation_id.action_open_conversation()
    
    def action_view_ai_conversation(self):
        """Acción para ver conversación IA"""
        
        self.ensure_one()
        
        if not self.x_ai_conversation_id:
            raise UserError("No hay conversación IA activa para esta orden")
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Conversación IA',
            'res_model': 'ai.conversation',
            'res_id': self.x_ai_conversation_id.id,
            'view_mode': 'form',
            'target': 'current'
        }
```

#### Tarea 6.2: Webhook para Comunicación Bidireccional
```python
# extra-addons/patco_ai_agent/controllers/ai_webhook.py
from odoo import http
from odoo.http import request
import json
import logging
import requests

_logger = logging.getLogger(__name__)

class AIWebhookController(http.Controller):
    
    @http.route('/ai/webhook/message', type='json', auth='user', methods=['POST'])
    def receive_ai_message(self, **kwargs):
        """Recibe mensajes desde el agente IA"""
        
        try:
            data = request.jsonrequest
            
            conversation_id = data.get('conversation_id')
            message = data.get('message')
            actions = data.get('actions', [])
            
            if not conversation_id or not message:
                return {'error': 'Faltan parámetros requeridos'}
            
            # Buscar conversación
            conversation = request.env['ai.conversation'].search([
                ('id', '=', int(conversation_id))
            ], limit=1)
            
            if not conversation:
                return {'error': 'Conversación no encontrada'}
            
            # Procesar mensaje del agente IA
            conversation._process_ai_message(message, actions)
            
            return {'success': True, 'message': 'Mensaje procesado'}
            
        except Exception as e:
            _logger.error(f"Error procesando mensaje IA: {e}")
            return {'error': str(e)}
    
    @http.route('/ai/webhook/user_message', type='json', auth='user', methods=['POST'])
    def send_user_message(self, **kwargs):
        """Envía mensaje del usuario al agente IA"""
        
        try:
            data = request.jsonrequest
            
            conversation_id = data.get('conversation_id')
            message = data.get('message')
            user_id = data.get('user_id')
            
            if not all([conversation_id, message, user_id]):
                return {'error': 'Faltan parámetros requeridos'}
            
            # Buscar conversación
            conversation = request.env['ai.conversation'].search([
                ('id', '=', int(conversation_id))
            ], limit=1)
            
            if not conversation:
                return {'error': 'Conversación no encontrada'}
            
            # Enviar mensaje al LangGraph server
            response = conversation._send_message_to_ai(message, user_id)
            
            return {'success': True, 'response': response}
            
        except Exception as e:
            _logger.error(f"Error enviando mensaje a IA: {e}")
            return {'error': str(e)}
    
    @http.route('/ai/conversation/<int:conversation_id>/status', type='json', auth='user')
    def get_conversation_status(self, conversation_id, **kwargs):
        """Obtiene estado actual de conversación"""
        
        try:
            conversation = request.env['ai.conversation'].browse(conversation_id)
            
            if not conversation.exists():
                return {'error': 'Conversación no encontrada'}
            
            return {
                'conversation_id': conversation.id,
                'state': conversation.state,
                'fsm_order': conversation.fsm_order_id.name,
                'technician': conversation.technician_id.name,
                'current_equipment': conversation.current_equipment_id.name if conversation.current_equipment_id else None,
                'message_count': conversation.message_count,
                'duration': conversation.duration
            }
            
        except Exception as e:
            _logger.error(f"Error obteniendo estado de conversación: {e}")
            return {'error': str(e)}
```

#### Criterios de Aceptación Fase 6
- [ ] Extensión FSM funcionando correctamente
- [ ] Conversaciones IA creándose automáticamente al asignar técnico
- [ ] Webhooks operativos para comunicación bidireccional
- [ ] Integración básica Odoo-LangGraph funcionando
- [ ] Estados de conversación actualizándose correctamente

---

## 📚 Fase 7: RAG y Búsqueda Semántica (1 semana)

### Objetivos
- Integrar búsqueda vectorial completa
- Optimizar relevancia de resultados RAG
- Implementar filtros contextuales

### Tareas Específicas

#### Tarea 7.1: Servicio RAG Avanzado
```python
# extra-addons/patco_ai_agent/services/vector_service.py
import psycopg2
import numpy as np
import logging
from typing import List, Dict, Any, Optional
import requests
import json
import os

_logger = logging.getLogger(__name__)

class VectorSearchService:
    
    def __init__(self):
        self.db_url = os.environ.get('DATABASE_URL')
        self.gemini_api_key = os.environ.get('GEMINI_API_KEY')
    
    def search_knowledge_base(
        self, 
        query: str, 
        context: Dict[str, Any] = None,
        limit: int = 5,
        similarity_threshold: float = 0.7
    ) -> List[Dict[str, Any]]:
        """Búsqueda semántica en base de conocimiento"""
        
        try:
            # Generar embedding de la consulta
            query_embedding = self._generate_embedding(query)
            
            # Construir filtros contextuales
            filters = self._build_context_filters(context or {})
            
            # Ejecutar búsqueda vectorial
            results = self._execute_vector_search(
                query_embedding, 
                filters, 
                limit, 
                similarity_threshold
            )
            
            # Enriquecer resultados con metadatos
            enriched_results = self._enrich_results(results)
            
            _logger.info(f"Búsqueda RAG completada: {len(enriched_results)} resultados")
            
            return enriched_results
            
        except Exception as e:
            _logger.error(f"Error en búsqueda RAG: {e}")
            return []
    
    def _generate_embedding(self, text: str) -> List[float]:
        """Genera embedding usando Gemini API"""
        
        url = "https://generativelanguage.googleapis.com/v1beta/models/embedding-001:embedContent"
        
        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": self.gemini_api_key
        }
        
        data = {
            "model": "models/embedding-001",
            "content": {"parts": [{"text": text}]}
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        return result['embedding']['values']
    
    def _build_context_filters(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Construye filtros basados en contexto"""
        
        filters = {}
        
        # Filtro por categoría de equipo
        if context.get('equipment_category_id'):
            filters['equipment_category_id'] = context['equipment_category_id']
        
        # Filtro por naturaleza de servicio
        if context.get('service_nature_id'):
            filters['service_nature_id'] = context['service_nature_id']
        
        # Filtro por tipo de documento
        if context.get('document_types'):
            filters['document_types'] = context['document_types']
        else:
            # Por defecto, priorizar manuales y procedimientos
            filters['document_types'] = ['manual', 'procedure', 'checklist']
        
        return filters
    
    def _execute_vector_search(
        self, 
        query_embedding: List[float], 
        filters: Dict[str, Any],
        limit: int,
        similarity_threshold: float
    ) -> List[Dict[str, Any]]:
        """Ejecuta búsqueda vectorial en PostgreSQL"""
        
        conn = psycopg2.connect(self.db_url)
        cursor = conn.cursor()
        
        try:
            # Query base con similitud coseno
            query = """
            SELECT 
                e.attachment_id,
                e.chunk_index,
                e.content,
                e.metadata,
                1 - (e.embedding <=> %s::vector) as similarity,
                a.name as document_name,
                a.x_document_type
            FROM ai_document_embeddings e
            JOIN ir_attachment a ON e.attachment_id = a.id
            WHERE 1 - (e.embedding <=> %s::vector) > %s
            """
            
            params = [query_embedding, query_embedding, similarity_threshold]
            
            # Aplicar filtros contextuales
            if filters.get('equipment_category_id'):
                query += " AND a.x_equipment_category_ids @> %s"
                params.append(json.dumps([filters['equipment_category_id']]))
            
            if filters.get('service_nature_id'):
                query += " AND a.x_service_nature_ids @> %s"
                params.append(json.dumps([filters['service_nature_id']]))
            
            if filters.get('document_types'):
                placeholders = ','.join(['%s'] * len(filters['document_types']))
                query += f" AND a.x_document_type IN ({placeholders})"
                params.extend(filters['document_types'])
            
            # Ordenar por similitud y limitar
            query += " ORDER BY e.embedding <=> %s::vector LIMIT %s"
            params.extend([query_embedding, limit])
            
            cursor.execute(query, params)
            results = cursor.fetchall()
            
            # Convertir a diccionarios
            documents = []
            for row in results:
                documents.append({
                    'attachment_id': row[0],
                    'chunk_index': row[1],
                    'content': row[2],
                    'metadata': row[3],
                    'similarity': float(row[4]),
                    'document_name': row[5],
                    'document_type': row[6]
                })
            
            return documents
            
        finally:
            cursor.close()
            conn.close()
    
    def _enrich_results(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Enriquece resultados con información adicional"""
        
        for result in results:
            # Agregar snippet destacado
            content = result['content']
            if len(content) > 300:
                result['snippet'] = content[:300] + "..."
            else:
                result['snippet'] = content
            
            # Agregar score de relevancia (0-100)
            result['relevance_score'] = int(result['similarity'] * 100)
            
            # Agregar tipo de documento legible
            doc_type_map = {
                'manual': 'Manual Técnico',
                'procedure': 'Procedimiento',
                'checklist': 'Lista de Verificación',
                'report': 'Reporte',
                'image': 'Imagen Técnica'
            }
            result['document_type_display'] = doc_type_map.get(
                result['document_type'], 
                result['document_type']
            )
        
        return results
```

#### Criterios de Aceptación Fase 7
- [ ] Búsqueda vectorial funcionando con PGVector
- [ ] Filtros contextuales aplicándose correctamente
- [ ] Resultados RAG con alta relevancia (>85%)
- [ ] Integración con LangGraph completada
- [ ] Performance de búsqueda optimizada (<2 segundos)

---

## 📄 Fase 8: Generación de Reportes con OnlyOffice (1 semana)

### Objetivos
- Implementar generación automática de reportes técnicos profesionales
- Integrar con OnlyOffice Document Server para creación de documentos
- Estructurar información desde conversaciones IA usando plantillas
- Crear sistema de plantillas reutilizables para diferentes tipos de servicio

### Arquitectura de Integración OnlyOffice

#### Stack Tecnológico para Reportes
- **OnlyOffice Document Server**: Servidor de documentos en puerto 8081
- **OnlyOffice Document Builder**: API para generación programática de documentos
- **Módulo onlyoffice_odoo**: Integración nativa con Odoo (ya disponible)
- **LangGraph Report Node**: Nodo especializado en generación de reportes
- **Plantillas DOCX**: Plantillas profesionales para diferentes tipos de servicio

#### Flujo de Generación de Reportes
```
Conversación IA Completada
    ↓
Extracción de Información Estructurada (Gemini)
    ↓
Selección de Plantilla según Tipo de Servicio
    ↓
Generación de Documento (OnlyOffice Document Builder)
    ↓
Almacenamiento en Odoo (ir.attachment)
    ↓
Vinculación con Orden FSM
    ↓
Notificación al Cliente y Técnico
```

### Tareas Específicas

#### Tarea 8.1: Servicio de Generación de Reportes con OnlyOffice
```python
# ai-services/langgraph/nodes/report_generator.py
import logging
from typing import Dict, Any, List
import google.generativeai as genai
import requests
import json
import os
from datetime import datetime
import tempfile
import base64

logger = logging.getLogger(__name__)

async def generate_report(state: Dict[str, Any]) -> Dict[str, Any]:
    """Genera reporte técnico desde conversación usando OnlyOffice"""
    
    try:
        conversation_history = state.get("messages", [])
        context = state.get("context", {})
        
        if not conversation_history:
            logger.warning("No hay historial de conversación para generar reporte")
            return state
        
        # Extraer información estructurada
        structured_data = await extract_structured_info(conversation_history, context)
        
        # Seleccionar plantilla según tipo de servicio
        template_type = determine_template_type(context, structured_data)
        
        # Generar documento con OnlyOffice Document Builder
        document_result = await create_onlyoffice_document(
            structured_data, 
            context, 
            template_type
        )
        
        # Almacenar documento en Odoo
        attachment_id = await store_document_in_odoo(
            document_result["content"],
            document_result["filename"],
            context
        )
        
        # Actualizar estado
        state["report_generated"] = True
        state["report_attachment_id"] = attachment_id
        state["report_filename"] = document_result["filename"]
        state["structured_data"] = structured_data
        
        logger.info(f"Reporte OnlyOffice generado exitosamente: {document_result['filename']}")
        
        return state
        
    except Exception as e:
        logger.error(f"Error generando reporte OnlyOffice: {e}")
        state["report_generated"] = False
        state["report_error"] = str(e)
        return state

def determine_template_type(context: Dict[str, Any], structured_data: Dict[str, Any]) -> str:
    """Determina el tipo de plantilla según el contexto del servicio"""
    
    # Obtener naturaleza del servicio desde contexto
    service_nature = context.get("service_nature", "")
    equipment_category = context.get("equipment_category", "")
    
    # Mapeo de tipos de servicio a plantillas
    template_mapping = {
        "preventivo": "mantenimiento_preventivo",
        "correctivo": "mantenimiento_correctivo", 
        "instalacion": "instalacion_equipo",
        "calibracion": "calibracion_tecnica",
        "inspeccion": "inspeccion_tecnica"
    }
    
    # Determinar plantilla por naturaleza de servicio
    for key, template in template_mapping.items():
        if key.lower() in service_nature.lower():
            return template
    
    # Plantilla por defecto
    return "servicio_general"

async def create_onlyoffice_document(
    structured_data: Dict[str, Any], 
    context: Dict[str, Any],
    template_type: str
) -> Dict[str, str]:
    """Crea documento usando OnlyOffice Document Builder API"""
    
    try:
        # URL del servidor OnlyOffice Document Server
        onlyoffice_url = os.getenv("ONLYOFFICE_SERVER_URL", "http://onlyoffice-documentserver:80")
        
        # Generar script de Document Builder
        builder_script = generate_document_builder_script(
            structured_data, 
            context, 
            template_type
        )
        
        # Llamar a OnlyOffice Document Builder API
        response = await call_document_builder_api(onlyoffice_url, builder_script)
        
        if response["success"]:
            return {
                "content": response["document_content"],
                "filename": generate_filename(context, structured_data),
                "format": "docx"
            }
        else:
            raise Exception(f"Error en Document Builder: {response['error']}")
            
    except Exception as e:
        logger.error(f"Error creando documento OnlyOffice: {e}")
        # Fallback: generar documento simple con contenido de texto
        return await create_fallback_document(structured_data, context)

def generate_document_builder_script(
    structured_data: Dict[str, Any], 
    context: Dict[str, Any],
    template_type: str
) -> str:
    """Genera script de OnlyOffice Document Builder para crear el documento"""
    
    fsm_order = context.get("fsm_order", {})
    servicio = structured_data.get("servicio", {})
    equipos = structured_data.get("equipos", [])
    
    script = f'''
    builder.CreateFile("docx");
    var oDocument = Api.GetDocument();
    var oParagraph, oRun;
    
    // Configurar estilos del documento
    var oMyStyle = oDocument.CreateStyle("Heading 1", "paragraph");
    oMyStyle.GetTextPr().SetFontSize(16);
    oMyStyle.GetTextPr().SetBold(true);
    oMyStyle.GetTextPr().SetColor(0, 51, 102, false);
    
    // ENCABEZADO DEL DOCUMENTO
    oParagraph = Api.CreateParagraph();
    oParagraph.SetStyle(oMyStyle);
    oRun = Api.CreateRun();
    oRun.AddText("REPORTE DE SERVICIO TÉCNICO PATCO");
    oParagraph.AddElement(oRun);
    oDocument.Push(oParagraph);
    
    // Línea separadora
    oParagraph = Api.CreateParagraph();
    oRun = Api.CreateRun();
    oRun.AddText("_".repeat(60));
    oParagraph.AddElement(oRun);
    oDocument.Push(oParagraph);
    
    // INFORMACIÓN GENERAL
    oParagraph = Api.CreateParagraph();
    oRun = Api.CreateRun();
    oRun.SetBold(true);
    oRun.AddText("INFORMACIÓN GENERAL");
    oParagraph.AddElement(oRun);
    oDocument.Push(oParagraph);
    
    oParagraph = Api.CreateParagraph();
    oRun = Api.CreateRun();
    oRun.AddText("Orden de Servicio: {fsm_order.get('name', 'N/A')}");
    oParagraph.AddElement(oRun);
    oDocument.Push(oParagraph);
    
    oParagraph = Api.CreateParagraph();
    oRun = Api.CreateRun();
    oRun.AddText("Técnico: {servicio.get('tecnico', 'N/A')}");
    oParagraph.AddElement(oRun);
    oDocument.Push(oParagraph);
    
    oParagraph = Api.CreateParagraph();
    oRun = Api.CreateRun();
    oRun.AddText("Cliente: {servicio.get('cliente', 'N/A')}");
    oParagraph.AddElement(oRun);
    oDocument.Push(oParagraph);
    
    oParagraph = Api.CreateParagraph();
    oRun = Api.CreateRun();
    oRun.AddText("Fecha: {servicio.get('fecha_inicio', 'N/A')} - {servicio.get('fecha_fin', 'N/A')}");
    oParagraph.AddElement(oRun);
    oDocument.Push(oParagraph);
    
    // EQUIPOS ATENDIDOS
    oParagraph = Api.CreateParagraph();
    oRun = Api.CreateRun();
    oRun.SetBold(true);
    oRun.AddText("EQUIPOS ATENDIDOS");
    oParagraph.AddElement(oRun);
    oDocument.Push(oParagraph);
    '''
    
    # Agregar información de equipos
    for i, equipo in enumerate(equipos):
        script += f'''
        oParagraph = Api.CreateParagraph();
        oRun = Api.CreateRun();
        oRun.SetBold(true);
        oRun.AddText("{equipo.get('nombre', f'Equipo {i+1}')}");
        oParagraph.AddElement(oRun);
        oDocument.Push(oParagraph);
        
        oParagraph = Api.CreateParagraph();
        oRun = Api.CreateRun();
        oRun.AddText("Problema: {equipo.get('problema_reportado', 'N/A')}");
        oParagraph.AddElement(oRun);
        oDocument.Push(oParagraph);
        
        oParagraph = Api.CreateParagraph();
        oRun = Api.CreateRun();
        oRun.AddText("Diagnóstico: {equipo.get('diagnostico', 'N/A')}");
        oParagraph.AddElement(oRun);
        oDocument.Push(oParagraph);
        
        oParagraph = Api.CreateParagraph();
        oRun = Api.CreateRun();
        oRun.AddText("Estado Final: {equipo.get('estado_final', 'N/A')}");
        oParagraph.AddElement(oRun);
        oDocument.Push(oParagraph);
        '''
    
    # Finalizar documento
    script += '''
    // OBSERVACIONES
    oParagraph = Api.CreateParagraph();
    oRun = Api.CreateRun();
    oRun.SetBold(true);
    oRun.AddText("OBSERVACIONES TÉCNICAS");
    oParagraph.AddElement(oRun);
    oDocument.Push(oParagraph);
    
    oParagraph = Api.CreateParagraph();
    oRun = Api.CreateRun();
    oRun.AddText("''' + structured_data.get('observaciones_tecnicas', 'Sin observaciones adicionales') + '''");
    oParagraph.AddElement(oRun);
    oDocument.Push(oParagraph);
    
    // PIE DE DOCUMENTO
    oParagraph = Api.CreateParagraph();
    oRun = Api.CreateRun();
    oRun.AddText("_".repeat(60));
    oParagraph.AddElement(oRun);
    oDocument.Push(oParagraph);
    
    oParagraph = Api.CreateParagraph();
    oRun = Api.CreateRun();
    oRun.SetItalic(true);
    oRun.AddText("Reporte generado automáticamente por PATCO IA - ''' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '''");
    oParagraph.AddElement(oRun);
    oDocument.Push(oParagraph);
    
    builder.SaveFile("docx", "''' + generate_filename(context, structured_data) + '''");
    builder.CloseFile();
    '''
    
    return script

async def call_document_builder_api(onlyoffice_url: str, script: str) -> Dict[str, Any]:
    """Llama a la API de OnlyOffice Document Builder"""
    
    try:
        # Endpoint de Document Builder
        builder_url = f"{onlyoffice_url}/docbuilder"
        
        # Preparar payload
        payload = {
            "async": False,
            "filetype": "docx",
            "key": f"patco_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "outputtype": "docx",
            "script": script
        }
        
        # Headers con JWT si está habilitado
        headers = {
            "Content-Type": "application/json"
        }
        
        jwt_secret = os.getenv("ONLYOFFICE_JWT_SECRET")
        if jwt_secret:
            import jwt
            token = jwt.encode(payload, jwt_secret, algorithm="HS256")
            headers["Authorization"] = f"Bearer {token}"
        
        # Realizar llamada HTTP
        response = requests.post(
            builder_url,
            json=payload,
            headers=headers,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get("error") == 0:
                # Descargar documento generado
                download_url = result.get("fileUrl")
                if download_url:
                    doc_response = requests.get(download_url, timeout=30)
                    return {
                        "success": True,
                        "document_content": base64.b64encode(doc_response.content).decode(),
                        "download_url": download_url
                    }
            
            return {
                "success": False,
                "error": result.get("error", "Error desconocido en Document Builder")
            }
        else:
            return {
                "success": False,
                "error": f"HTTP {response.status_code}: {response.text}"
            }
            
    except Exception as e:
        logger.error(f"Error llamando Document Builder API: {e}")
        return {
            "success": False,
            "error": str(e)
        }

async def create_fallback_document(
    structured_data: Dict[str, Any], 
    context: Dict[str, Any]
) -> Dict[str, str]:
    """Crea documento de respaldo en caso de fallo de OnlyOffice"""
    
    # Generar contenido de texto simple
    content = generate_simple_report_content(structured_data, context)
    
    # Convertir a base64 para almacenamiento
    content_b64 = base64.b64encode(content.encode('utf-8')).decode()
    
    return {
        "content": content_b64,
        "filename": generate_filename(context, structured_data, extension="txt"),
        "format": "txt"
    }

def generate_filename(
    context: Dict[str, Any], 
    structured_data: Dict[str, Any], 
    extension: str = "docx"
) -> str:
    """Genera nombre de archivo para el reporte"""
    
    fsm_order = context.get("fsm_order", {})
    order_name = fsm_order.get("name", "UNKNOWN").replace("/", "_")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    
    return f"Reporte_Servicio_{order_name}_{timestamp}.{extension}"

async def store_document_in_odoo(
    document_content: str, 
    filename: str, 
    context: Dict[str, Any]
) -> int:
    """Almacena el documento generado en Odoo como attachment"""
    
    try:
        # Usar MCP para crear attachment en Odoo
        mcp_client = context.get("mcp_client")
        if not mcp_client:
            raise Exception("Cliente MCP no disponible")
        
        # Preparar datos del attachment
        attachment_data = {
            "name": filename,
            "datas": document_content,
            "mimetype": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "res_model": "fsm.order",
            "res_id": context.get("fsm_order_id"),
            "x_document_type": "report",
            "description": "Reporte técnico generado automáticamente por IA"
        }
        
        # Crear attachment usando MCP
        result = await mcp_client.call_tool(
            "create_attachment",
            attachment_data
        )
        
        if result.get("success"):
            return result.get("attachment_id")
        else:
            raise Exception(f"Error creando attachment: {result.get('error')}")
            
    except Exception as e:
        logger.error(f"Error almacenando documento en Odoo: {e}")
        raise

def generate_simple_report_content(
    structured_data: Dict[str, Any], 
    context: Dict[str, Any]
) -> str:
    """Genera contenido de reporte simple como fallback"""
    
    fsm_order = context.get("fsm_order", {})
    servicio = structured_data.get("servicio", {})
    equipos = structured_data.get("equipos", [])
    
    content = f"""
REPORTE DE SERVICIO TÉCNICO PATCO
{'='*50}

INFORMACIÓN GENERAL
Orden de Servicio: {fsm_order.get('name', 'N/A')}
Técnico: {servicio.get('tecnico', 'N/A')}
Cliente: {servicio.get('cliente', 'N/A')}
Fecha: {servicio.get('fecha_inicio', 'N/A')} - {servicio.get('fecha_fin', 'N/A')}
Ubicación: {servicio.get('ubicacion', 'N/A')}

EQUIPOS ATENDIDOS
{'-'*20}
"""
    
    for i, equipo in enumerate(equipos, 1):
        content += f"""
{i}. {equipo.get('nombre', f'Equipo {i}')}
   Modelo: {equipo.get('modelo', 'N/A')}
   Problema: {equipo.get('problema_reportado', 'N/A')}
   Diagnóstico: {equipo.get('diagnostico', 'N/A')}
   Estado Final: {equipo.get('estado_final', 'N/A')}
"""
    
    content += f"""
OBSERVACIONES TÉCNICAS
{'-'*25}
{structured_data.get('observaciones_tecnicas', 'Sin observaciones adicionales')}

RECOMENDACIONES
{'-'*15}
{structured_data.get('recomendaciones', 'Sin recomendaciones específicas')}

CONCLUSIONES
{'-'*12}
Trabajo Completado: {'Sí' if structured_data.get('trabajo_completado') else 'No'}
Cliente Satisfecho: {structured_data.get('cliente_satisfecho', 'Pendiente')}

{'='*50}
Reporte generado automáticamente por PATCO IA
Fecha de generación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    return content
```

async def extract_structured_info(
    conversation_history: List[Dict], 
    context: Dict[str, Any]
) -> Dict[str, Any]:
    """Extrae información estructurada de la conversación"""
    
    # Concatenar toda la conversación
    full_conversation = "\n".join([
        f"{msg.get('role', 'user')}: {msg.get('content', '')}"
        for msg in conversation_history
    ])
    
    # Prompt para extracción estructurada
    extraction_prompt = f"""
    Analiza la siguiente conversación entre un técnico y un asistente IA durante un servicio técnico.
    Extrae la información estructurada en formato JSON.
    
    Conversación:
    {full_conversation}
    
    Extrae la siguiente información (usa null si no está disponible):
    {{
        "servicio": {{
            "fecha_inicio": "YYYY-MM-DD HH:MM",
            "fecha_fin": "YYYY-MM-DD HH:MM",
            "tecnico": "nombre del técnico",
            "cliente": "nombre del cliente",
            "ubicacion": "dirección o ubicación"
        }},
        "equipos": [
            {{
                "nombre": "nombre del equipo",
                "modelo": "modelo si se menciona",
                "problema_reportado": "descripción del problema",
                "diagnostico": "diagnóstico del técnico",
                "acciones_realizadas": ["acción 1", "acción 2"],
                "estado_final": "funcionando/reparado/pendiente/etc"
            }}
        ],
        "repuestos_utilizados": [
            {{
                "nombre": "nombre del repuesto",
                "cantidad": "cantidad usada",
                "observaciones": "observaciones si las hay"
            }}
        ],
        "mediciones": [
            {{
                "parametro": "qué se midió",
                "valor": "valor medido",
                "unidad": "unidad de medida",
                "estado": "normal/anormal/etc"
            }}
        ],
        "observaciones_tecnicas": "observaciones generales del técnico",
        "recomendaciones": "recomendaciones para el cliente",
        "trabajo_completado": true/false,
        "cliente_satisfecho": true/false/null,
        "proxima_visita_requerida": true/false,
        "fecha_proxima_visita": "YYYY-MM-DD si aplica"
    }}
    
    Responde SOLO con el JSON, sin texto adicional.
    """
    
    try:
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        model = genai.GenerativeModel('gemini-pro')
        
        response = model.generate_content(extraction_prompt)
        
        # Parsear JSON
        structured_data = json.loads(response.text)
        
        return structured_data
        
    except Exception as e:
        logger.error(f"Error extrayendo información estructurada: {e}")
        return {}

async def generate_report_content(
    structured_data: Dict[str, Any], 
    context: Dict[str, Any]
) -> str:
    """Genera contenido del reporte en formato profesional"""
    
    # Información básica del contexto
    fsm_order = context.get("fsm_order", {})
    
    # Prompt para generar reporte
    report_prompt = f"""
    Genera un reporte técnico profesional basado en la siguiente información estructurada.
    El reporte debe ser claro, detallado y seguir un formato estándar de servicios técnicos.
    
    Información del servicio:
    {json.dumps(structured_data, indent=2, ensure_ascii=False)}
    
    Información adicional del contexto:
    - Orden de servicio: {fsm_order.get('name', 'N/A')}
    - Tipo de servicio: {fsm_order.get('service_nature', 'N/A')}
    - Área técnica: {fsm_order.get('service_area', 'N/A')}
    
    Estructura del reporte:
    
    # REPORTE DE SERVICIO TÉCNICO
    
    ## INFORMACIÓN GENERAL
    - Orden de Servicio: [número]
    - Fecha y Hora: [fecha inicio] - [fecha fin]
    - Técnico Responsable: [nombre]
    - Cliente: [nombre]
    - Ubicación: [dirección]
    - Tipo de Servicio: [tipo]
    
    ## EQUIPOS ATENDIDOS
    [Para cada equipo:]
    ### [Nombre del Equipo]
    - **Modelo:** [modelo]
    - **Problema Reportado:** [descripción]
    - **Diagnóstico:** [diagnóstico técnico]
    - **Acciones Realizadas:**
      - [acción 1]
      - [acción 2]
    - **Estado Final:** [estado]
    
    ## REPUESTOS Y MATERIALES
    [Lista de repuestos utilizados con cantidades]
    
    ## MEDICIONES Y PRUEBAS
    [Tabla con parámetros medidos, valores y estados]
    
    ## OBSERVACIONES TÉCNICAS
    [Observaciones detalladas del técnico]
    
    ## RECOMENDACIONES
    [Recomendaciones para el cliente]
    
    ## CONCLUSIONES
    - Trabajo completado: [Sí/No]
    - Cliente satisfecho: [Sí/No/Pendiente]
    - Próxima visita requerida: [Sí/No]
    - Fecha próxima visita: [fecha si aplica]
    
    ## FIRMA DIGITAL
    [Espacio para firmas del técnico y cliente]
    
    ---
    Reporte generado automáticamente por el Sistema PATCO IA
    Fecha de generación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    
    Usa un lenguaje técnico profesional pero comprensible. Incluye todos los detalles relevantes.
    """
    
    try:
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        model = genai.GenerativeModel('gemini-pro')
        
        response = model.generate_content(report_prompt)
        
        return response.text
        
    except Exception as e:
        logger.error(f"Error generando contenido del reporte: {e}")
        return "Error generando el contenido del reporte."

#### Tarea 8.2: Integración con Módulo patco_ai_agent

```python
# extra-addons/patco_ai_agent/models/ai_conversation.py - Extensión para reportes
from odoo import models, fields, api
import logging
import requests
import json

_logger = logging.getLogger(__name__)

class AIConversation(models.Model):
    _inherit = 'ai.conversation'
    
    # Campos adicionales para reportes
    report_attachment_id = fields.Many2one(
        'ir.attachment', 
        string='Reporte Generado',
        help='Documento de reporte técnico generado automáticamente'
    )
    report_template_type = fields.Selection([
        ('servicio_general', 'Servicio General'),
        ('mantenimiento_preventivo', 'Mantenimiento Preventivo'),
        ('mantenimiento_correctivo', 'Mantenimiento Correctivo'),
        ('instalacion_equipo', 'Instalación de Equipo'),
        ('calibracion_tecnica', 'Calibración Técnica'),
        ('inspeccion_tecnica', 'Inspección Técnica')
    ], string='Tipo de Plantilla', default='servicio_general')
    
    report_generation_status = fields.Selection([
        ('pending', 'Pendiente'),
        ('processing', 'Procesando'),
        ('completed', 'Completado'),
        ('failed', 'Fallido')
    ], string='Estado de Generación', default='pending')
    
    report_error_message = fields.Text('Error de Generación')
    
    def action_generate_report(self):
        """Acción manual para generar reporte"""
        self.ensure_one()
        
        if self.state not in ['work_in_progress', 'checklist_exit', 'completed']:
            raise UserError("La conversación debe estar en progreso o completada para generar reporte")
        
        # Llamar al servicio LangGraph para generar reporte
        self._trigger_report_generation()
    
    def _trigger_report_generation(self):
        """Dispara la generación de reporte vía LangGraph"""
        
        try:
            # URL del servidor LangGraph
            langgraph_url = self.env['ir.config_parameter'].sudo().get_param(
                'patco_ai_agent.langgraph_server_url', 
                'http://langgraph-server:8001'
            )
            
            # Preparar contexto para LangGraph
            context = self._prepare_report_context()
            
            # Preparar historial de mensajes
            messages = self._get_conversation_messages()
            
            # Payload para LangGraph
            payload = {
                "conversation_id": f"report_{self.id}",
                "action": "generate_report",
                "context": context,
                "messages": messages
            }
            
            # Actualizar estado
            self.report_generation_status = 'processing'
            
            # Llamada asíncrona a LangGraph
            response = requests.post(
                f"{langgraph_url}/conversation/{self.id}/generate_report",
                json=payload,
                timeout=120
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    self._handle_report_generation_success(result)
                else:
                    self._handle_report_generation_error(result.get("error", "Error desconocido"))
            else:
                self._handle_report_generation_error(f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            _logger.error(f"Error disparando generación de reporte: {e}")
            self._handle_report_generation_error(str(e))
    
    def _prepare_report_context(self):
        """Prepara contexto para generación de reporte"""
        
        return {
            "fsm_order_id": self.fsm_order_id.id,
            "fsm_order": {
                "name": self.fsm_order_id.name,
                "partner_id": self.fsm_order_id.partner_id.name,
                "location_id": self.fsm_order_id.location_id.name if self.fsm_order_id.location_id else None,
                "service_nature": self.fsm_order_id.x_service_nature_id.name if self.fsm_order_id.x_service_nature_id else None,
                "service_area": self.fsm_order_id.x_service_area_id.name if self.fsm_order_id.x_service_area_id else None,
                "equipment_ids": [eq.id for eq in self.fsm_order_id.equipment_ids]
            },
            "technician_id": self.technician_id.id,
            "technician_name": self.technician_id.name,
            "conversation_id": self.id,
            "template_type": self.report_template_type,
            "equipment_category": self.current_equipment_id.category_id.name if self.current_equipment_id else None
        }
    
    def _get_conversation_messages(self):
        """Obtiene mensajes de la conversación desde discuss.channel"""
        
        messages = []
        if self.channel_id:
            # Obtener mensajes del canal
            channel_messages = self.env['mail.message'].search([
                ('res_id', '=', self.channel_id.id),
                ('model', '=', 'discuss.channel'),
                ('message_type', '=', 'comment')
            ], order='create_date asc')
            
            for msg in channel_messages:
                # Determinar rol del mensaje
                role = "assistant" if msg.author_id.name == "🤖 Asistente IA PATCO" else "user"
                
                messages.append({
                    "role": role,
                    "content": msg.body,
                    "timestamp": msg.create_date.isoformat(),
                    "author": msg.author_id.name
                })
        
        return messages
    
    def _handle_report_generation_success(self, result):
        """Maneja éxito en generación de reporte"""
        
        try:
            # Crear attachment si se proporcionó contenido
            if result.get("attachment_id"):
                attachment = self.env['ir.attachment'].browse(result["attachment_id"])
                if attachment.exists():
                    self.report_attachment_id = attachment.id
            
            # Actualizar estado
            self.report_generation_status = 'completed'
            self.state = 'report_generated'
            self.report_generated = True
            
            # Notificar en el canal
            if self.channel_id:
                self.channel_id.message_post(
                    body=f"✅ Reporte técnico generado exitosamente: {result.get('filename', 'reporte.docx')}",
                    message_type='notification'
                )
            
            _logger.info(f"Reporte generado exitosamente para conversación {self.id}")
            
        except Exception as e:
            _logger.error(f"Error procesando éxito de reporte: {e}")
            self._handle_report_generation_error(str(e))
    
    def _handle_report_generation_error(self, error_message):
        """Maneja error en generación de reporte"""
        
        self.report_generation_status = 'failed'
        self.report_error_message = error_message
        
        # Notificar error en el canal
        if self.channel_id:
            self.channel_id.message_post(
                body=f"❌ Error generando reporte: {error_message}",
                message_type='notification'
            )
        
        _logger.error(f"Error generando reporte para conversación {self.id}: {error_message}")
    
    def action_view_report(self):
        """Acción para ver el reporte generado"""
        self.ensure_one()
        
        if not self.report_attachment_id:
            raise UserError("No hay reporte generado para esta conversación")
        
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{self.report_attachment_id.id}?download=true',
            'target': 'new'
        }
    
    def action_regenerate_report(self):
        """Acción para regenerar reporte"""
        self.ensure_one()
        
        # Limpiar reporte anterior
        if self.report_attachment_id:
            self.report_attachment_id.unlink()
            self.report_attachment_id = False
        
        self.report_generation_status = 'pending'
        self.report_error_message = False
        
        # Generar nuevo reporte
        self._trigger_report_generation()
```

#### Tarea 8.3: Extensión del Servidor MCP para Reportes

```python
# ai-services/mcp/tools/report_tools.py
from typing import Dict, Any, List
import logging
import base64
from datetime import datetime

logger = logging.getLogger(__name__)

async def create_attachment(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Crea attachment en Odoo para almacenar reporte"""
    
    try:
        # Validar argumentos requeridos
        required_fields = ['name', 'datas', 'res_model', 'res_id']
        for field in required_fields:
            if field not in arguments:
                return create_error_response(
                    ErrorTypeEnum.VALIDATION_ERROR,
                    f"Campo requerido faltante: {field}"
                )
        
        # Preparar datos del attachment
        attachment_data = {
            'name': arguments['name'],
            'datas': arguments['datas'],
            'mimetype': arguments.get('mimetype', 'application/octet-stream'),
            'res_model': arguments['res_model'],
            'res_id': arguments['res_id'],
            'description': arguments.get('description', ''),
            'x_document_type': arguments.get('x_document_type', 'report')
        }
        
        # Crear attachment usando cliente Odoo
        odoo_client = get_odoo_client()
        attachment_id = odoo_client.create('ir.attachment', attachment_data)
        
        if attachment_id:
            return {
                "success": True,
                "attachment_id": attachment_id,
                "message": f"Attachment creado exitosamente: {arguments['name']}"
            }
        else:
            return create_error_response(
                ErrorTypeEnum.INTERNAL_ERROR,
                "Error creando attachment en Odoo"
            )
            
    except Exception as e:
        logger.error(f"Error creando attachment: {e}")
        return create_error_response(
            ErrorTypeEnum.INTERNAL_ERROR,
            f"Error interno: {str(e)}"
        )

async def update_fsm_order_report(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Actualiza orden FSM con información del reporte generado"""
    
    try:
        order_id = arguments.get('order_id')
        attachment_id = arguments.get('attachment_id')
        
        if not order_id:
            return create_error_response(
                ErrorTypeEnum.VALIDATION_ERROR,
                "order_id es requerido"
            )
        
        # Preparar datos de actualización
        update_data = {
            'x_ai_report_generated': True,
            'x_ai_report_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        if attachment_id:
            update_data['x_ai_report_attachment_id'] = attachment_id
        
        # Actualizar orden FSM
        odoo_client = get_odoo_client()
        result = odoo_client.write('fsm.order', [order_id], update_data)
        
        if result:
            return {
                "success": True,
                "order_id": order_id,
                "message": "Orden FSM actualizada con información de reporte"
            }
        else:
            return create_error_response(
                ErrorTypeEnum.INTERNAL_ERROR,
                "Error actualizando orden FSM"
            )
            
    except Exception as e:
        logger.error(f"Error actualizando FSM order: {e}")
        return create_error_response(
            ErrorTypeEnum.INTERNAL_ERROR,
            f"Error interno: {str(e)}"
        )

async def get_onlyoffice_server_status(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Verifica estado del servidor OnlyOffice"""
    
    try:
        import requests
        
        onlyoffice_url = arguments.get('server_url', 'http://onlyoffice-documentserver:80')
        
        # Verificar health check de OnlyOffice
        response = requests.get(f"{onlyoffice_url}/healthcheck", timeout=10)
        
        if response.status_code == 200:
            return {
                "success": True,
                "status": "healthy",
                "server_url": onlyoffice_url,
                "response_time": response.elapsed.total_seconds()
            }
        else:
            return {
                "success": False,
                "status": "unhealthy",
                "server_url": onlyoffice_url,
                "error": f"HTTP {response.status_code}"
            }
            
    except Exception as e:
        logger.error(f"Error verificando OnlyOffice: {e}")
        return {
            "success": False,
            "status": "error",
            "error": str(e)
        }
```

#### Tarea 8.4: Plantillas de Reportes OnlyOffice

```javascript
// ai-services/langgraph/templates/report_templates.js
// Plantillas de OnlyOffice Document Builder para diferentes tipos de servicio

const REPORT_TEMPLATES = {
    servicio_general: {
        name: "Reporte General de Servicio",
        sections: ["header", "general_info", "equipment", "observations", "footer"],
        styles: {
            title_color: [0, 51, 102],
            title_size: 16,
            section_size: 14,
            body_size: 11
        }
    },
    
    mantenimiento_preventivo: {
        name: "Reporte de Mantenimiento Preventivo",
        sections: ["header", "general_info", "checklist", "equipment", "measurements", "recommendations", "footer"],
        styles: {
            title_color: [0, 102, 51],
            title_size: 16,
            section_size: 14,
            body_size: 11
        }
    },
    
    mantenimiento_correctivo: {
        name: "Reporte de Mantenimiento Correctivo",
        sections: ["header", "general_info", "problem_analysis", "equipment", "repairs", "parts_used", "testing", "footer"],
        styles: {
            title_color: [153, 51, 0],
            title_size: 16,
            section_size: 14,
            body_size: 11
        }
    },
    
    instalacion_equipo: {
        name: "Reporte de Instalación de Equipo",
        sections: ["header", "general_info", "equipment_specs", "installation_process", "testing", "training", "footer"],
        styles: {
            title_color: [51, 102, 153],
            title_size: 16,
            section_size: 14,
            body_size: 11
        }
    }
};

function generateTemplateScript(templateType, data) {
    const template = REPORT_TEMPLATES[templateType] || REPORT_TEMPLATES.servicio_general;
    
    let script = `
    builder.CreateFile("docx");
    var oDocument = Api.GetDocument();
    var oParagraph, oRun, oTable;
    
    // Configurar estilos
    var oTitleStyle = oDocument.CreateStyle("Title", "paragraph");
    oTitleStyle.GetTextPr().SetFontSize(${template.styles.title_size});
    oTitleStyle.GetTextPr().SetBold(true);
    oTitleStyle.GetTextPr().SetColor(${template.styles.title_color.join(', ')}, false);
    
    var oSectionStyle = oDocument.CreateStyle("Section", "paragraph");
    oSectionStyle.GetTextPr().SetFontSize(${template.styles.section_size});
    oSectionStyle.GetTextPr().SetBold(true);
    
    var oBodyStyle = oDocument.CreateStyle("Body", "paragraph");
    oBodyStyle.GetTextPr().SetFontSize(${template.styles.body_size});
    `;
    
    // Generar secciones según plantilla
    template.sections.forEach(section => {
        script += generateSectionScript(section, data, template);
    });
    
    script += `
    builder.SaveFile("docx", "${data.filename}");
    builder.CloseFile();
    `;
    
    return script;
}

function generateSectionScript(sectionType, data, template) {
    switch (sectionType) {
        case 'header':
            return generateHeaderSection(data, template);
        case 'general_info':
            return generateGeneralInfoSection(data);
        case 'equipment':
            return generateEquipmentSection(data);
        case 'checklist':
            return generateChecklistSection(data);
        case 'measurements':
            return generateMeasurementsSection(data);
        case 'observations':
            return generateObservationsSection(data);
        case 'footer':
            return generateFooterSection(data);
        default:
            return '';
    }
}

function generateHeaderSection(data, template) {
    return `
    // ENCABEZADO
    oParagraph = Api.CreateParagraph();
    oParagraph.SetStyle(oTitleStyle);
    oParagraph.SetJc("center");
    oRun = Api.CreateRun();
    oRun.AddText("${template.name.toUpperCase()}");
    oParagraph.AddElement(oRun);
    oDocument.Push(oParagraph);
    
    // Logo y línea separadora
    oParagraph = Api.CreateParagraph();
    oParagraph.SetJc("center");
    oRun = Api.CreateRun();
    oRun.AddText("PATCO - Servicios Técnicos Especializados");
    oParagraph.AddElement(oRun);
    oDocument.Push(oParagraph);
    
    oParagraph = Api.CreateParagraph();
    oRun = Api.CreateRun();
    oRun.AddText("${"=".repeat(80)}");
    oParagraph.AddElement(oRun);
    oDocument.Push(oParagraph);
    `;
}

function generateGeneralInfoSection(data) {
    const servicio = data.structured_data?.servicio || {};
    const fsm_order = data.context?.fsm_order || {};
    
    return `
    // INFORMACIÓN GENERAL
    oParagraph = Api.CreateParagraph();
    oParagraph.SetStyle(oSectionStyle);
    oRun = Api.CreateRun();
    oRun.AddText("INFORMACIÓN GENERAL");
    oParagraph.AddElement(oRun);
    oDocument.Push(oParagraph);
    
    // Crear tabla de información general
    oTable = Api.CreateTable(2, 4);
    oTable.SetWidth("percent", 100);
    
    // Fila 1
    oTable.GetCell(0, 0).GetContent().GetElement(0).AddText("Orden de Servicio:");
    oTable.GetCell(0, 1).GetContent().GetElement(0).AddText("${fsm_order.name || 'N/A'}");
    oTable.GetCell(0, 2).GetContent().GetElement(0).AddText("Fecha:");
    oTable.GetCell(0, 3).GetContent().GetElement(0).AddText("${servicio.fecha_inicio || 'N/A'}");
    
    // Fila 2
    oTable.GetCell(1, 0).GetContent().GetElement(0).AddText("Técnico:");
    oTable.GetCell(1, 1).GetContent().GetElement(0).AddText("${servicio.tecnico || 'N/A'}");
    oTable.GetCell(1, 2).GetContent().GetElement(0).AddText("Cliente:");
    oTable.GetCell(1, 3).GetContent().GetElement(0).AddText("${servicio.cliente || 'N/A'}");
    
    oDocument.Push(oTable);
    `;
}

// Exportar funciones para uso en el generador de reportes
module.exports = {
    REPORT_TEMPLATES,
    generateTemplateScript,
    generateSectionScript
};
```

#### Criterios de Aceptación Fase 8
- [ ] Extracción de información estructurada funcionando con Gemini
- [ ] Generación de reportes DOCX con OnlyOffice Document Builder
- [ ] Integración completa con módulo patco_ai_agent
- [ ] Almacenamiento de reportes como attachments en Odoo
- [ ] Plantillas diferenciadas por tipo de servicio
- [ ] Sistema de fallback para casos de error
- [ ] Notificaciones automáticas al completar reporte
- [ ] Vinculación correcta con órdenes FSM
- [ ] Interfaz para visualizar y descargar reportes

---

## 🎨 Fase 9: Interfaz de Usuario con Canales Nativos (1 semana)

### Objetivos
- Implementar sistema de canales nativos de Odoo (mail.channel) para conversaciones IA
- Crear usuario bot IA dedicado y procesamiento automático de mensajes
- Eliminar necesidad de widgets frontend personalizados usando chatter nativo
- Garantizar soporte multimedia y móvil inmediato
- Integrar completamente con el ecosistema discuss de Odoo

### Arquitectura del Nuevo Enfoque

#### Sistema de Canales Nativos
- **Usuario Bot IA**: `res.users` dedicado para el asistente IA
- **Canales Automáticos**: `mail.channel` privado por cada orden FSM
- **Chatter Nativo**: Aprovecha el sistema de mensajería existente de Odoo
- **Soporte Multimedia**: Texto, imágenes y adjuntos nativamente soportados
- **Compatibilidad Móvil**: Funciona automáticamente en dispositivos móviles

#### Flujo de Conversación Nativo
```
Orden FSM Asignada → Técnico
    ↓
Creación Automática de Canal Privado (mail.channel)
    ↓
Adición de Técnico + Usuario Bot IA como Miembros
    ↓
Mensaje Inicial del Bot (channel.message_post())
    ↓
Técnico Responde en Chatter Nativo
    ↓
Detección Automática de Nuevos Mensajes (mail.message)
    ↓
Procesamiento con LangGraph + RAG
    ↓
Respuesta del Bot en Canal (with_user bot_id)
```

### Tareas Específicas

#### Tarea 9.1: Sistema de Usuario Bot IA y Canales Automáticos
```python
# extra-addons/patco_ai_agent/models/ai_bot_user.py
from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class AIBotUser(models.Model):
    _name = 'ai.bot.user'
    _description = 'Gestión de Usuario Bot IA'
    
    name = fields.Char('Nombre del Bot', default='🤖 Asistente IA PATCO')
    user_id = fields.Many2one('res.users', 'Usuario del Bot', required=True)
    partner_id = fields.Many2one('res.partner', 'Partner del Bot', required=True)
    is_active = fields.Boolean('Activo', default=True)
    
    @api.model
    def get_or_create_bot_user(self):
        """Obtiene o crea el usuario bot IA"""
        
        bot = self.search([('is_active', '=', True)], limit=1)
        
        if not bot:
            # Crear partner para el bot
            partner = self.env['res.partner'].create({
                'name': '🤖 Asistente IA PATCO',
                'is_company': False,
                'email': 'ai-bot@patco.com.pe',
                'phone': '+51-1-AI-PATCO',
                'category_id': [(4, self.env.ref('base.res_partner_category_0').id)],
                'comment': 'Usuario bot para asistente IA conversacional'
            })
            
            # Crear usuario para el bot
            user = self.env['res.users'].create({
                'name': '🤖 Asistente IA PATCO',
                'login': 'ai_bot_patco',
                'email': 'ai-bot@patco.com.pe',
                'partner_id': partner.id,
                'groups_id': [(4, self.env.ref('base.group_user').id)],
                'active': True,
                'is_system': True
            })
            
            # Crear registro del bot
            bot = self.create({
                'name': '🤖 Asistente IA PATCO',
                'user_id': user.id,
                'partner_id': partner.id,
                'is_active': True
            })
            
            _logger.info(f"Usuario bot IA creado: {bot.name} (ID: {bot.user_id.id})")
        
        return bot

# Extensión de fsm.order para integración con canales IA
class FsmOrder(models.Model):
    _inherit = 'fsm.order'
    
    # Campos para canales IA
    x_ai_channel_id = fields.Many2one(
        'mail.channel', 
        string='Canal IA',
        help='Canal de conversación con el asistente IA'
    )
    x_ai_enabled = fields.Boolean(
        'IA Habilitada', 
        default=True,
        help='Habilitar asistente IA para esta orden'
    )
    x_ai_status = fields.Selection([
        ('not_started', 'No Iniciado'),
        ('active', 'Activo'),
        ('completed', 'Completado'),
        ('error', 'Error')
    ], string='Estado IA', default='not_started')
    
    def write(self, vals):
        """Sobrescribir write para detectar asignación de técnico"""
        
        result = super().write(vals)
        
        # Si se asigna técnico, crear canal IA automáticamente
        if 'person_id' in vals and vals['person_id']:
            for order in self:
                if order.x_ai_enabled and not order.x_ai_channel_id:
                    order._create_ai_channel()
        
        return result
    
    def _create_ai_channel(self):
        """Crea canal privado de IA para la orden FSM"""
        
        try:
            if not self.person_id:
                _logger.warning(f"No se puede crear canal IA para orden {self.name}: sin técnico asignado")
                return
            
            # Obtener usuario bot IA
            bot = self.env['ai.bot.user'].get_or_create_bot_user()
            
            # Crear canal privado
            channel = self.env['mail.channel'].create({
                'name': f"🤖 IA - {self.name} - {self.person_id.name}",
                'channel_type': 'chat',
                'public': 'private',
                'description': f'Canal de asistente IA para orden {self.name}',
                'channel_partner_ids': [
                    (4, self.person_id.user_id.partner_id.id),  # Técnico
                    (4, bot.partner_id.id)  # Bot IA
                ]
            })
            
            # Vincular canal a la orden
            self.x_ai_channel_id = channel.id
            self.x_ai_status = 'active'
            
            # Enviar mensaje inicial del bot
            self._send_initial_ai_message(channel, bot)
            
            _logger.info(f"Canal IA creado para orden {self.name} - Canal ID: {channel.id}")
            
        except Exception as e:
            _logger.error(f"Error creando canal IA para orden {self.name}: {e}")
            self.x_ai_status = 'error'
    
    def _send_initial_ai_message(self, channel, bot):
        """Envía mensaje inicial del asistente IA"""
        
        message = f"""¡Hola {self.person_id.name}! 👋

Soy tu asistente IA para la orden de servicio **{self.name}**.

📋 **Detalles del servicio:**
• Cliente: {self.partner_id.name}
• Ubicación: {self.location_id.name if self.location_id else 'No especificada'}
• Equipos asignados: {len(self.equipment_ids)} equipos

Te ayudaré durante todo el proceso con:
🔍 Búsqueda en manuales técnicos
📝 Checklists dinámicos
🛠️ Procedimientos paso a paso
📊 Generación automática de reportes

¿Has llegado al sitio y estás listo para comenzar?"""
        
        # Enviar mensaje como usuario bot
        channel.with_user(bot.user_id).message_post(
            body=message,
            message_type='comment',
            subtype_xmlid='mail.mt_comment'
        )
```

#### Tarea 9.2: Procesamiento Automático de Mensajes del Técnico
```python
# extra-addons/patco_ai_agent/models/mail_message.py
from odoo import models, fields, api
import logging
import requests
import json

_logger = logging.getLogger(__name__)

class MailMessage(models.Model):
    _inherit = 'mail.message'
    
    x_processed_by_ai = fields.Boolean('Procesado por IA', default=False)
    x_ai_response_pending = fields.Boolean('Respuesta IA Pendiente', default=False)
    
    @api.model_create_multi
    def create(self, vals_list):
        """Sobrescribir create para detectar mensajes en canales IA"""
        
        messages = super().create(vals_list)
        
        # Procesar mensajes en canales IA
        for message in messages:
            if message._should_process_with_ai():
                message._process_message_with_ai()
        
        return messages
    
    def _should_process_with_ai(self):
        """Determina si el mensaje debe ser procesado por IA"""
        
        # Solo procesar mensajes de usuarios (no del bot)
        if self.author_id and self.author_id.email == 'ai-bot@patco.com.pe':
            return False
        
        # Solo procesar mensajes en canales IA
        if not self.res_model == 'mail.channel':
            return False
        
        # Verificar que el canal esté vinculado a una orden FSM con IA activa
        channel = self.env['mail.channel'].browse(self.res_id)
        fsm_order = self.env['fsm.order'].search([
            ('x_ai_channel_id', '=', channel.id),
            ('x_ai_status', '=', 'active')
        ], limit=1)
        
        return bool(fsm_order)
    
    def _process_message_with_ai(self):
        """Procesa el mensaje con el servicio IA"""
        
        try:
            # Obtener orden FSM asociada
            channel = self.env['mail.channel'].browse(self.res_id)
            fsm_order = self.env['fsm.order'].search([
                ('x_ai_channel_id', '=', channel.id)
            ], limit=1)
            
            if not fsm_order:
                return
            
            # Marcar como procesándose
            self.x_ai_response_pending = True
            
            # Preparar contexto para IA
            context = {
                'fsm_order_id': fsm_order.id,
                'fsm_order_name': fsm_order.name,
                'technician_id': fsm_order.person_id.id,
                'technician_name': fsm_order.person_id.name,
                'client_name': fsm_order.partner_id.name,
                'equipment_ids': fsm_order.equipment_ids.ids,
                'service_nature': fsm_order.x_service_nature_id.name if fsm_order.x_service_nature_id else None,
                'channel_id': channel.id
            }
            
            # Enviar mensaje al servidor LangGraph
            self._send_to_langgraph_server(context)
            
        except Exception as e:
            _logger.error(f"Error procesando mensaje con IA: {e}")
            self.x_ai_response_pending = False
    
    def _send_to_langgraph_server(self, context):
        """Envía mensaje al servidor LangGraph para procesamiento"""
        
        try:
            langgraph_url = self.env['ir.config_parameter'].sudo().get_param(
                'patco_ai_agent.langgraph_server_url', 
                'http://langgraph-server:8001'
            )
            
            payload = {
                'conversation_id': f"fsm_{context['fsm_order_id']}",
                'message': {
                    'role': 'user',
                    'content': self.body,
                    'timestamp': self.date.isoformat(),
                    'author_id': self.author_id.id,
                    'author_name': self.author_id.name
                },
                'context': context
            }
            
            # Llamada asíncrona al servidor LangGraph
            response = requests.post(
                f"{langgraph_url}/conversation/{payload['conversation_id']}/message",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Procesar respuesta del agente IA
                if result.get('response'):
                    self._send_ai_response(result['response'], context)
                
                # Ejecutar acciones si las hay
                if result.get('actions'):
                    self._execute_ai_actions(result['actions'], context)
                
                self.x_processed_by_ai = True
                self.x_ai_response_pending = False
                
            else:
                _logger.error(f"Error en servidor LangGraph: {response.status_code} - {response.text}")
                self.x_ai_response_pending = False
                
        except Exception as e:
            _logger.error(f"Error enviando mensaje a LangGraph: {e}")
            self.x_ai_response_pending = False
    
    def _send_ai_response(self, response_text, context):
        """Envía respuesta del agente IA al canal"""
        
        try:
            # Obtener usuario bot
            bot = self.env['ai.bot.user'].get_or_create_bot_user()
            channel = self.env['mail.channel'].browse(context['channel_id'])
            
            # Enviar respuesta como usuario bot
            channel.with_user(bot.user_id).message_post(
                body=response_text,
                message_type='comment',
                subtype_xmlid='mail.mt_comment'
            )
            
        except Exception as e:
            _logger.error(f"Error enviando respuesta IA: {e}")
    
    def _execute_ai_actions(self, actions, context):
        """Ejecuta acciones solicitadas por el agente IA"""
        
        try:
            fsm_order = self.env['fsm.order'].browse(context['fsm_order_id'])
            
            for action in actions:
                action_type = action.get('type')
                
                if action_type == 'update_fsm_order':
                    # Actualizar campos de la orden FSM
                    values = action.get('values', {})
                    if values:
                        fsm_order.write(values)
                        _logger.info(f"Orden FSM {fsm_order.name} actualizada por IA: {values}")
                
                elif action_type == 'create_checklist':
                    # Crear checklist dinámico
                    checklist_data = action.get('checklist_data', {})
                    # Implementar creación de checklist
                    
                elif action_type == 'search_knowledge':
                    # Realizar búsqueda en base de conocimiento
                    query = action.get('query', '')
                    # Implementar búsqueda RAG
                    
                elif action_type == 'generate_report':
                    # Disparar generación de reporte
                    # Implementar generación de reporte
                    pass
                
        except Exception as e:
            _logger.error(f"Error ejecutando acciones IA: {e}")
```

#### Tarea 9.3: Controlador para Gestión de Conversaciones
```python
# extra-addons/patco_ai_agent/controllers/ai_conversation_controller.py
from odoo import http
from odoo.http import request
import json
import logging

_logger = logging.getLogger(__name__)

class AIConversationController(http.Controller):
    
    @http.route('/ai/conversation/get_active', type='json', auth='user', methods=['POST'])
    def get_active_conversation(self, **kwargs):
        """Obtiene conversación IA activa para una orden FSM"""
        
        try:
            data = request.jsonrequest
            fsm_order_id = data.get('fsm_order_id')
            
            if not fsm_order_id:
                return {'error': 'fsm_order_id requerido'}
            
            # Buscar orden FSM con canal IA activo
            fsm_order = request.env['fsm.order'].browse(fsm_order_id)
            
            if fsm_order.x_ai_channel_id and fsm_order.x_ai_status == 'active':
                return {
                    'conversation_id': f"fsm_{fsm_order_id}",
                    'channel_id': fsm_order.x_ai_channel_id.id,
                    'channel_name': fsm_order.x_ai_channel_id.name,
                    'status': fsm_order.x_ai_status
                }
            else:
                return {'conversation_id': None}
                
        except Exception as e:
            _logger.error(f"Error obteniendo conversación activa: {e}")
            return {'error': str(e)}
    
    @http.route('/ai/conversation/create', type='json', auth='user', methods=['POST'])
    def create_conversation(self, **kwargs):
        """Crea nueva conversación IA para orden FSM"""
        
        try:
            data = request.jsonrequest
            fsm_order_id = data.get('fsm_order_id')
            
            if not fsm_order_id:
                return {'error': 'fsm_order_id requerido'}
            
            fsm_order = request.env['fsm.order'].browse(fsm_order_id)
            
            if not fsm_order.exists():
                return {'error': 'Orden FSM no encontrada'}
            
            # Crear canal IA si no existe
            if not fsm_order.x_ai_channel_id:
                fsm_order._create_ai_channel()
            
            return {
                'conversation_id': f"fsm_{fsm_order_id}",
                'channel_id': fsm_order.x_ai_channel_id.id,
                'status': 'created'
            }
            
        except Exception as e:
            _logger.error(f"Error creando conversación: {e}")
            return {'error': str(e)}
    
    @http.route('/ai/conversation/history', type='json', auth='user', methods=['POST'])
    def get_conversation_history(self, **kwargs):
        """Obtiene historial de mensajes de conversación"""
        
        try:
            data = request.jsonrequest
            conversation_id = data.get('conversation_id')
            
            if not conversation_id:
                return {'error': 'conversation_id requerido'}
            
            # Extraer fsm_order_id del conversation_id
            fsm_order_id = int(conversation_id.replace('fsm_', ''))
            fsm_order = request.env['fsm.order'].browse(fsm_order_id)
            
            if not fsm_order.x_ai_channel_id:
                return {'messages': []}
            
            # Obtener mensajes del canal
            messages = request.env['mail.message'].search([
                ('res_model', '=', 'mail.channel'),
                ('res_id', '=', fsm_order.x_ai_channel_id.id)
            ], order='date asc')
            
            message_list = []
            for msg in messages:
                # Determinar rol del mensaje
                role = 'assistant' if msg.author_id.email == 'ai-bot@patco.com.pe' else 'user'
                
                message_list.append({
                    'role': role,
                    'content': msg.body,
                    'timestamp': msg.date.isoformat(),
                    'author_name': msg.author_id.name
                })
            
            return {'messages': message_list}
            
        except Exception as e:
            _logger.error(f"Error obteniendo historial: {e}")
            return {'error': str(e)}
    
    @http.route('/ai/conversation/send_message', type='json', auth='user', methods=['POST'])
    def send_message(self, **kwargs):
        """Envía mensaje del usuario al canal IA"""
        
        try:
            data = request.jsonrequest
            conversation_id = data.get('conversation_id')
            message = data.get('message')
            
            if not conversation_id or not message:
                return {'error': 'conversation_id y message requeridos'}
            
            # Extraer fsm_order_id del conversation_id
            fsm_order_id = int(conversation_id.replace('fsm_', ''))
            fsm_order = request.env['fsm.order'].browse(fsm_order_id)
            
            if not fsm_order.x_ai_channel_id:
                return {'error': 'Canal IA no encontrado'}
            
            # Enviar mensaje al canal
            fsm_order.x_ai_channel_id.message_post(
                body=message,
                message_type='comment',
                subtype_xmlid='mail.mt_comment'
            )
            
            return {'success': True, 'message': 'Mensaje enviado'}
            
        except Exception as e:
            _logger.error(f"Error enviando mensaje: {e}")
            return {'error': str(e)}
```

#### Tarea 9.4: Vistas Integradas con Chatter Nativo
```xml
<!-- extra-addons/patco_ai_agent/views/fsm_order_ai_views.xml -->
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    
    <!-- Vista de formulario FSM con integración IA -->
    <record id="view_fsm_order_form_ai" model="ir.ui.view">
        <field name="name">fsm.order.form.ai</field>
        <field name="model">fsm.order</field>
        <field name="inherit_id" ref="fieldservice.fsm_order_form"/>
        <field name="arch" type="xml">
            
            <!-- Agregar campos IA en el header -->
            <xpath expr="//header" position="inside">
                <button name="action_open_ai_channel" 
                        string="💬 Abrir Chat IA" 
                        type="object" 
                        class="btn-primary"
                        attrs="{'invisible': [('x_ai_channel_id', '=', False)]}"/>
                <button name="action_create_ai_channel" 
                        string="🤖 Activar IA" 
                        type="object" 
                        class="btn-secondary"
                        attrs="{'invisible': [('x_ai_channel_id', '!=', False)]}"/>
            </xpath>
            
            <!-- Agregar grupo de campos IA -->
            <xpath expr="//group[@name='main_info']" position="after">
                <group name="ai_info" string="Asistente IA" 
                       attrs="{'invisible': [('x_ai_enabled', '=', False)]}">
                    <field name="x_ai_enabled"/>
                    <field name="x_ai_status" 
                           decoration-success="x_ai_status == 'active'"
                           decoration-warning="x_ai_status == 'not_started'"
                           decoration-danger="x_ai_status == 'error'"/>
                    <field name="x_ai_channel_id" 
                           attrs="{'invisible': [('x_ai_channel_id', '=', False)]}"/>
                </group>
            </xpath>
            
            <!-- Integrar canal IA en el chatter -->
            <xpath expr="//div[@class='oe_chatter']" position="before">
                <div class="oe_ai_chat_container" 
                     attrs="{'invisible': [('x_ai_channel_id', '=', False)]}">
                    <div class="oe_ai_chat_header">
                        <h4>🤖 Conversación con Asistente IA</h4>
                        <p>Chatea directamente con el asistente IA para obtener ayuda durante el servicio</p>
                    </div>
                    
                    <!-- Widget de chat IA integrado -->
                    <field name="x_ai_channel_id" 
                           widget="mail_thread" 
                           options="{'display_log_button': True, 'post_refresh': 'always'}"/>
                </div>
            </xpath>
            
        </field>
    </record>
    
    <!-- Vista de canal IA personalizada -->
    <record id="view_mail_channel_ai_form" model="ir.ui.view">
        <field name="name">mail.channel.ai.form</field>
        <field name="model">mail.channel</field>
        <field name="inherit_id" ref="mail.mail_channel_view_form"/>
        <field name="arch" type="xml">
            
            <!-- Personalizar vista para canales IA -->
            <xpath expr="//field[@name='name']" position="after">
                <field name="description" 
                       attrs="{'invisible': [('description', '=', False)]}"/>
            </xpath>
            
            <!-- Agregar información de orden FSM asociada -->
            <xpath expr="//group" position="after">
                <group name="fsm_info" string="Información FSM" 
                       attrs="{'invisible': [('name', 'not ilike', '🤖 IA -')]}">
                    <field name="fsm_order_id" 
                           compute="_compute_fsm_order_info" 
                           string="Orden FSM"/>
                    <field name="technician_id" 
                           compute="_compute_fsm_order_info" 
                           string="Técnico"/>
                </group>
            </xpath>
            
        </field>
    </record>

</odoo>
```

#### Tarea 9.5: Integración con Aplicación Móvil (Nativa)
```python
# extra-addons/patco_ai_agent/controllers/mobile_api.py
from odoo import http
from odoo.http import request
import json
import logging

_logger = logging.getLogger(__name__)

class MobileAIController(http.Controller):
    
    @http.route('/api/mobile/ai/conversation/start', type='json', auth='user', methods=['POST'])
    def mobile_start_conversation(self, **kwargs):
        """API móvil para iniciar conversación IA"""
        
        try:
            data = request.jsonrequest
            fsm_order_id = data.get('fsm_order_id')
            
            fsm_order = request.env['fsm.order'].browse(fsm_order_id)
            
            if not fsm_order.exists():
                return {'success': False, 'error': 'Orden no encontrada'}
            
            # Crear canal IA si no existe
            if not fsm_order.x_ai_channel_id:
                fsm_order._create_ai_channel()
            
            return {
                'success': True,
                'conversation_id': f"fsm_{fsm_order_id}",
                'channel_id': fsm_order.x_ai_channel_id.id,
                'welcome_message': f"¡Hola! Soy tu asistente IA para la orden {fsm_order.name}. ¿En qué puedo ayudarte?"
            }
            
        except Exception as e:
            _logger.error(f"Error en API móvil: {e}")
            return {'success': False, 'error': str(e)}
    
    @http.route('/api/mobile/ai/conversation/messages', type='json', auth='user', methods=['POST'])
    def mobile_get_messages(self, **kwargs):
        """API móvil para obtener mensajes"""
        
        try:
            data = request.jsonrequest
            conversation_id = data.get('conversation_id')
            last_message_id = data.get('last_message_id', 0)
            
            # Extraer fsm_order_id
            fsm_order_id = int(conversation_id.replace('fsm_', ''))
            fsm_order = request.env['fsm.order'].browse(fsm_order_id)
            
            if not fsm_order.x_ai_channel_id:
                return {'success': False, 'error': 'Canal no encontrado'}
            
            # Obtener mensajes nuevos
            domain = [
                ('res_model', '=', 'mail.channel'),
                ('res_id', '=', fsm_order.x_ai_channel_id.id),
                ('id', '>', last_message_id)
            ]
            
            messages = request.env['mail.message'].search(domain, order='date asc')
            
            message_list = []
            for msg in messages:
                role = 'assistant' if msg.author_id.email == 'ai-bot@patco.com.pe' else 'user'
                
                message_list.append({
                    'id': msg.id,
                    'role': role,
                    'content': msg.body,
                    'timestamp': msg.date.isoformat(),
                    'author_name': msg.author_id.name,
                    'has_attachments': bool(msg.attachment_ids)
                })
            
            return {
                'success': True,
                'messages': message_list,
                'last_message_id': messages[-1].id if messages else last_message_id
            }
            
        except Exception as e:
            _logger.error(f"Error obteniendo mensajes móvil: {e}")
            return {'success': False, 'error': str(e)}
```

### Criterios de Aceptación Fase 9
- [ ] Usuario bot IA creado automáticamente
- [ ] Canales privados generándose automáticamente al asignar técnico
- [ ] Mensajes del técnico procesándose automáticamente
- [ ] Respuestas IA enviándose al canal nativo
- [ ] Integración completa con chatter de Odoo
- [ ] Soporte multimedia funcionando (texto, imágenes, adjuntos)
- [ ] Compatibilidad móvil verificada
- [ ] API móvil operativa para aplicaciones nativas

### Beneficios del Nuevo Enfoque
- **Sin Desarrollo Frontend**: Elimina necesidad de widgets personalizados
- **Soporte Nativo**: Multimedia, notificaciones, móvil automático
- **Integración Perfecta**: Usa infraestructura existente de Odoo
- **Escalabilidad**: Aprovecha optimizaciones nativas de discuss
- **Mantenimiento**: Menor complejidad técnica y de mantenimiento
                this.addMessage({
                    role: "assistant",
                    content: response.response,
                    timestamp: new Date().toISOString()
                });
            }
            
        } catch (error) {
            console.error("Error enviando mensaje:", error);
            this.notification.add(_t("Error enviando mensaje al asistente IA"), {
                type: "danger"
            });
            
            // Agregar mensaje de error
            this.addMessage({
                role: "assistant",
                content: "Lo siento, tuve un problema procesando tu mensaje. ¿Puedes intentar de nuevo?",
                timestamp: new Date().toISOString(),
                isError: true
            });
            
        } finally {
            this.state.isLoading = false;
        }
    }
    
    addMessage(message) {
        this.state.messages.push(message);
        this.scrollToBottom();
    }
    
    scrollToBottom() {
        setTimeout(() => {
            if (this.chatContainer.el) {
                this.chatContainer.el.scrollTop = this.chatContainer.el.scrollHeight;
            }
        }, 100);
    }
    
    onKeyPress(event) {
        if (event.key === "Enter" && !event.shiftKey) {
            event.preventDefault();
            this.sendMessage();
        }
    }
    
    formatTimestamp(timestamp) {
        const date = new Date(timestamp);
        return date.toLocaleTimeString('es-PE', {
            hour: '2-digit',
            minute: '2-digit'
        });
    }
    
    getMessageClass(message) {
        const baseClass = "ai-chat-message";
        
        if (message.role === "user") {
            return `${baseClass} ai-chat-message-user`;
        } else if (message.isError) {
            return `${baseClass} ai-chat-message-error`;
        } else {
            return `${baseClass} ai-chat-message-assistant`;
        }
    }
}
```

```xml
<!-- extra-addons/patco_ai_agent/static/src/components/ai_chat_widget.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<templates xml:space="preserve">
    
    <t t-name="patco_ai_agent.AIChatWidget" owl="1">
        <div class="ai-chat-widget">
            <!-- Header del chat -->
            <div class="ai-chat-header">
                <div class="ai-chat-title">
                    <i class="fa fa-robot"/> Asistente IA PATCO
                </div>
                <div class="ai-chat-status">
                    <span t-if="state.isConnected" class="badge badge-success">
                        <i class="fa fa-circle"/> Conectado
                    </span>
                    <span t-else="" class="badge badge-danger">
                        <i class="fa fa-circle"/> Desconectado
                    </span>
                </div>
            </div>
            
            <!-- Contenedor de mensajes -->
            <div class="ai-chat-messages" t-ref="chatContainer">
                <div t-foreach="state.messages" t-as="message" t-key="message_index" 
                     t-att-class="getMessageClass(message)">
                    
                    <!-- Avatar del mensaje -->
                    <div class="ai-chat-avatar">
                        <i t-if="message.role === 'user'" class="fa fa-user"/>
                        <i t-else="" class="fa fa-robot"/>
                    </div>
                    
                    <!-- Contenido del mensaje -->
                    <div class="ai-chat-content">
                        <div class="ai-chat-text" t-esc="message.content"/>
                        <div class="ai-chat-timestamp" t-esc="formatTimestamp(message.timestamp)"/>
                    </div>
                </div>
                
                <!-- Indicador de carga -->
                <div t-if="state.isLoading" class="ai-chat-loading">
                    <div class="ai-chat-message ai-chat-message-assistant">
                        <div class="ai-chat-avatar">
                            <i class="fa fa-robot"/>
                        </div>
                        <div class="ai-chat-content">
                            <div class="ai-chat-typing">
                                <span></span>
                                <span></span>
                                <span></span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Input de mensaje -->
            <div class="ai-chat-input-container">
                <div class="ai-chat-input-wrapper">
                    <textarea 
                        class="ai-chat-input"
                        t-model="state.currentInput"
                        t-ref="messageInput"
                        placeholder="Escribe tu mensaje aquí..."
                        rows="1"
                        t-on-keypress="onKeyPress"
                        t-att-disabled="!state.isConnected or state.isLoading"/>
                    
                    <button 
                        class="ai-chat-send-btn btn btn-primary"
                        t-on-click="sendMessage"
                        t-att-disabled="!state.isConnected or state.isLoading or !state.currentInput.trim()">
                        <i class="fa fa-paper-plane"/>
                    </button>
                </div>
            </div>
        </div>
    </t>
    
</templates>
```

#### Criterios de Aceptación Fase 9
- [ ] Widget de chat integrado en vistas FSM
- [ ] Interfaz conversacional intuitiva y responsive
- [ ] Comunicación en tiempo real funcionando
- [ ] Historial de mensajes persistente
- [ ] Indicadores visuales de estado apropiados

---

## 🚀 Fase 10: Optimización y Producción (1 semana)

### Objetivos
- Optimizar performance del sistema completo
- Implementar monitoreo y alertas
- Preparar para despliegue en producción

### Tareas Específicas

#### Tarea 10.1: Optimizaciones de Performance
```python
# ai-services/shared/performance_monitor.py
import time
import logging
import psutil
import asyncio
from functools import wraps
from typing import Dict, Any, Callable
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class PerformanceMonitor:
    
    def __init__(self):
        self.metrics = {}
        self.alerts = []
    
    def measure_execution_time(self, operation_name: str):
        """Decorator para medir tiempo de ejecución"""
        
        def decorator(func: Callable):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                start_time = time.time()
                
                try:
                    result = await func(*args, **kwargs)
                    execution_time = time.time() - start_time
                    
                    # Registrar métrica
                    self._record_metric(operation_name, execution_time, "success")
                    
                    # Alertar si es muy lento
                    if execution_time > 5.0:  # 5 segundos
                        self._create_alert(
                            f"Operación lenta detectada: {operation_name}",
                            f"Tiempo de ejecución: {execution_time:.2f}s"
                        )
                    
                    return result
                    
                except Exception as e:
                    execution_time = time.time() - start_time
                    self._record_metric(operation_name, execution_time, "error")
                    
                    self._create_alert(
                        f"Error en operación: {operation_name}",
                        f"Error: {str(e)}"
                    )
                    
                    raise
            
            return wrapper
        return decorator
    
    def _record_metric(self, operation: str, duration: float, status: str):
        """Registra métrica de performance"""
        
        if operation not in self.metrics:
            self.metrics[operation] = {
                "total_calls": 0,
                "total_duration": 0,
                "avg_duration": 0,
                "max_duration": 0,
                "min_duration": float('inf'),
                "success_count": 0,
                "error_count": 0
            }
        
        metric = self.metrics[operation]
        metric["total_calls"] += 1
        metric["total_duration"] += duration
        metric["avg_duration"] = metric["total_duration"] / metric["total_calls"]
        metric["max_duration"] = max(metric["max_duration"], duration)
        metric["min_duration"] = min(metric["min_duration"], duration)
        
        if status == "success":
            metric["success_count"] += 1
        else:
            metric["error_count"] += 1
        
        logger.info(f"Métrica registrada - {operation}: {duration:.3f}s ({status})")
    
    def _create_alert(self, title: str, description: str):
        """Crea alerta de performance"""
        
        alert = {
            "timestamp": datetime.now().isoformat(),
            "title": title,
            "description": description,
            "severity": "warning"
        }
        
        self.alerts.append(alert)
        logger.warning(f"Alerta creada: {title} - {description}")
        
        # Mantener solo últimas 100 alertas
        if len(self.alerts) > 100:
            self.alerts = self.alerts[-100:]
    
    def get_system_metrics(self) -> Dict[str, Any]:
        """Obtiene métricas del sistema"""
        
        return {
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_percent": psutil.disk_usage('/').percent,
            "timestamp": datetime.now().isoformat()
        }
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Genera reporte de performance"""
        
        return {
            "operations": self.metrics,
            "system_metrics": self.get_system_metrics(),
            "recent_alerts": self.alerts[-10:],  # Últimas 10 alertas
            "generated_at": datetime.now().isoformat()
        }

# Instancia global
performance_monitor = PerformanceMonitor()
```

#### Tarea 10.2: Configuración de Producción
```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  # Servicios base existentes
  db:
    image: postgres:15
    container_name: odoo-patco-db-prod
    environment:
      - POSTGRES_DB=odoo_patco
      - POSTGRES_USER=odoo
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - PGDATA=/var/lib/postgresql/data/pgdata
    volumes:
      - odoo-db-data-prod:/var/lib/postgresql/data/pgdata
    restart: unless-stopped
    networks:
      - odoo-network-prod
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U odoo -d odoo_patco"]
      interval: 30s
      timeout: 10s
      retries: 10

  odoo:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: odoo-patco-app-prod
    depends_on:
      db:
        condition: service_healthy
    environment:
      - DB_HOST=db
      - DB_PORT=5432
      - ODOO_RC=/etc/odoo/odoo.conf
    volumes:
      - odoo-web-data-prod:/var/lib/odoo
      - ./config:/etc/odoo
      - ./extra-addons:/mnt/extra-addons
      - ./logs:/var/log/odoo
    restart: unless-stopped
    networks:
      - odoo-network-prod
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.odoo.rule=Host(`erp.patco.com.pe`)"
      - "traefik.http.routers.odoo.tls=true"
      - "traefik.http.routers.odoo.tls.certresolver=letsencrypt"

  # Servicios IA optimizados para producción
  langgraph-server:
    build:
      context: ./ai-services/langgraph
      dockerfile: Dockerfile.prod
    container_name: patco-langgraph-server-prod
    depends_on:
      - db
      - redis
    environment:
      - DATABASE_URL=postgresql://odoo:${DB_PASSWORD}@db:5432/odoo_patco
      - REDIS_URL=redis://redis:6379/0
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - LOG_LEVEL=INFO
      - WORKERS=4
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped
    networks:
      - odoo-network-prod
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: '1.0'

  mcp-server:
    build:
      context: ./ai-services/mcp
      dockerfile: Dockerfile.prod
    container_name: patco-mcp-server-prod
    depends_on:
      - odoo
    environment:
      - ODOO_URL=http://odoo:8069
      - ODOO_DB=odoo_patco
      - ODOO_USERNAME=${ODOO_AI_USER}
      - ODOO_PASSWORD=${ODOO_AI_PASSWORD}
      - LOG_LEVEL=INFO
    restart: unless-stopped
    networks:
      - odoo-network-prod

  vector-indexer:
    build:
      context: ./ai-services/indexer
      dockerfile: Dockerfile.prod
    container_name: patco-vector-indexer-prod
    depends_on:
      - db
    environment:
      - DATABASE_URL=postgresql://odoo:${DB_PASSWORD}@db:5432/odoo_patco
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - INDEXING_SCHEDULE=0 2 * * *  # Diario a las 2 AM
      - LOG_LEVEL=INFO
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped
    networks:
      - odoo-network-prod

  # Redis para caché y sesiones
  redis:
    image: redis:7-alpine
    container_name: patco-redis-prod
    command: redis-server --appendonly yes
    volumes:
      - redis-data-prod:/data
    restart: unless-stopped
    networks:
      - odoo-network-prod

  # Nginx para balanceo de carga
  nginx:
    image: nginx:alpine
    container_name: patco-nginx-prod
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./nginx/ssl:/etc/nginx/ssl
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      - odoo
      - langgraph-server
    restart: unless-stopped
    networks:
      - odoo-network-prod

volumes:
  odoo-web-data-prod:
  odoo-db-data-prod:
  redis-data-prod:

networks:
  odoo-network-prod:
    driver: bridge
```

#### Criterios de Aceptación Fase 10
- [ ] Sistema optimizado para producción
- [ ] Monitoreo de performance implementado
- [ ] Configuración de producción lista
- [ ] Documentación de despliegue completa
- [ ] Tests de carga pasando satisfactoriamente

---

## 📋 Resumen del Plan de Implementación

### Cronograma Total: 8-10 Semanas

| Semana | Fases | Entregables Clave |
|--------|-------|-------------------|
| **1** | Fase 0-1 | Infraestructura + Módulo base |
| **2** | Fase 2-3 | PGVector + Indexador |
| **3** | Fase 4 | Servidor MCP |
| **4-5** | Fase 5 | LangGraph Core |
| **6** | Fase 6 | Integración FSM |
| **7** | Fase 7 | RAG Completo |
| **8** | Fase 8 | Generación de Reportes |
| **9** | Fase 9 | Interfaz de Usuario |
| **10** | Fase 10 | Optimización y Producción |

### Hitos Críticos
1. **Semana 2**: Sistema de indexación funcionando
2. **Semana 4**: Conversaciones básicas operativas
3. **Semana 6**: Integración FSM completa
4. **Semana 8**: Reportes automáticos generándose
5. **Semana 10**: Sistema listo para producción

### Riesgos y Mitigaciones
- **Riesgo**: Latencia alta en búsquedas RAG
  - **Mitigación**: Optimización de índices y caché
- **Riesgo**: Límites de API de Gemini
  - **Mitigación**: Implementar rate limiting y fallbacks
- **Riesgo**: Complejidad de integración
  - **Mitigación**: Desarrollo incremental con validación continua

Este plan asegura una implementación controlada y medible, con cada fase completamente funcional antes de proceder a la siguiente, minimizando riesgos y maximizando las posibilidades de éxito del proyecto.
```