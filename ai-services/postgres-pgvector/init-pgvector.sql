-- Script de inicialización para PGVector
-- Se ejecuta automáticamente cuando se crea la base de datos

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

-- Confirmar que la extensión está instalada
SELECT 'PGVector extension installed successfully' as status;