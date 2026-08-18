from sentence_transformers import SentenceTransformer

model = SentenceTransformer( "BAAI/bge-small-en-v1.5")

def local_embedder(text: str) -> list[float]:

  embedding = model.encode(text)
  return embedding.tolist()
