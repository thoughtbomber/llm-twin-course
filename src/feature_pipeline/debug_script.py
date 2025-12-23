import bytewax.operators as op
from bytewax.dataflow import Dataflow
from core.db.qdrant import QdrantDatabaseConnector
from data_flow.stream_input import RabbitMQSource
from data_flow.stream_output import QdrantOutput
from data_logic.dispatchers import (
    ChunkingDispatcher,
    CleaningDispatcher,
    EmbeddingDispatcher,
    RawDispatcher,
)

# >>> DEBUG: Test input (uncomment to run locally without RabbitMQ)
from bytewax.testing import TestingSource
TEST_DATA = [
    {
        "type": "posts",
        "id": "post_001",
        "content": {"title": "Hello", "body": "This is a test post for debugging."},
        "metadata": {"author_id": "user_123"},
    },
    {
        "type": "articles",
        "id": "art_001",
        "content": {"headline": "Debugging Works", "text": "Bytewax pipeline validated locally."},
        "metadata": {"source": "internal"},
    },
]
# <<<

# >>> DEBUG: Simple validation function (optional)
def validate_embedded_chunk(item):
    """Basic sanity check: ensure embedding and ID exist."""
    assert hasattr(item, 'chunk_id'), f"Missing chunk_id in {item}"
    assert hasattr(item, 'embedding'), f"Missing embedding in {item}"
    assert isinstance(item.embedding, list), "Embedding must be a list"
    assert len(item.embedding) > 0, "Embedding is empty"
    print(f"✅ Valid embedded chunk: {item.chunk_id[:10]}...")
    return item
# <<<

flow = Dataflow("Streaming ingestion pipeline")

# >>> DEBUG: Uncomment this line to use test data instead of RabbitMQ
stream = op.input("input", flow, TestingSource(TEST_DATA))
# <<<

stream = op.map("raw dispatch", stream, RawDispatcher.handle_mq_message)
stream = op.map("clean dispatch", stream, CleaningDispatcher.dispatch_cleaner)

stream = op.flat_map("chunk dispatch", stream, ChunkingDispatcher.dispatch_chunker)
stream = op.map("embedded chunk dispatch", stream, EmbeddingDispatcher.dispatch_embedder)

# >>> DEBUG: Add validation before final output (uncomment when testing)
stream = op.map("validate embedding", stream, validate_embedded_chunk)
# <<<
