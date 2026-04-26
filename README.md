docker run --rm --network="host" -v $(pwd):/app -e QDRANT_HOST="172.20.8.1" -e OLLAMA_HOST="http://172.20.8.1:11434" -e QDRANT_API_KEY="test" ai-data-loader



docker run -d --name qdrant-p 6333:6333-p 6334:6334 -e QDRANT__SERVICE__API_KEY="test" -v $(pwd)/qdrant_storage:/qdrant/storage:z qdrant/qdrant
