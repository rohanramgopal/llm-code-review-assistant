from pathlib import Path
from typing import List
import faiss
import numpy as np
from app.utils.logger import get_logger

logger = get_logger(__name__)

_model = None


def get_model():
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        logger.info("Loading sentence transformer model...")
        _model = SentenceTransformer("all-MiniLM-L6-v2")
        logger.info("Sentence transformer model loaded.")
    return _model


class CodeRAG:
    def __init__(self) -> None:
        self.documents: List[str] = []
        self.metadata: List[str] = []
        self.index = None

    def chunk_text(self, text: str, chunk_size: int = 1200, overlap: int = 200) -> List[str]:
        chunks: List[str] = []
        start = 0
        while start < len(text):
            end = min(start + chunk_size, len(text))
            chunks.append(text[start:end])
            if end == len(text):
                break
            start = max(0, end - overlap)
        return chunks

    def build_from_files(self, files: list[Path]) -> None:
        self.documents.clear()
        self.metadata.clear()

        for file_path in files:
            try:
                text = file_path.read_text(encoding="utf-8", errors="ignore")
                chunks = self.chunk_text(text)
                for chunk in chunks:
                    self.documents.append(chunk)
                    self.metadata.append(str(file_path))
            except Exception as exc:
                logger.warning("Failed reading %s: %s", file_path, exc)

        if not self.documents:
            self.index = None
            return

        model = get_model()
        embeddings = model.encode(self.documents, convert_to_numpy=True)
        dim = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(np.array(embeddings, dtype=np.float32))

    def retrieve(self, query: str, k: int = 5) -> list[dict]:
        if self.index is None or not self.documents:
            return []

        model = get_model()
        q = model.encode([query], convert_to_numpy=True)
        distances, indices = self.index.search(np.array(q, dtype=np.float32), min(k, len(self.documents)))
        results = []
        for idx in indices[0]:
            results.append({
                "path": self.metadata[idx],
                "content": self.documents[idx]
            })
        return results
