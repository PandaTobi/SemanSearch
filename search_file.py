from pathlib import Path
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import json

model = SentenceTransformer("all-MiniLM-L6-v2")
# list of pretrained: https://sbert.net/docs/sentence_transformer/pretrained_models.html

def index_files(root_path):
    paths = []
    embeddings = []

    for path in Path(root_path).rglob("*"):
        if path.is_file() or path.is_dir():
            description = str(path.name).lower()
            paths.append(str(path.resolve()))
            embedding = model.encode(description)
            embeddings.append(embedding)

    embeddings_np = np.array(embeddings).astype("float32")

    faiss_index = faiss.IndexFlatL2(embeddings_np.shape[1])
    faiss_index.add(embeddings_np)
    faiss.write_index(faiss_index, "file_index.faiss")

    with open("file_paths.json", "w") as f:
        json.dump(paths, f)

    print("Indexing complete.")

def semantic_search(query):
    query_embedding = model.encode(query).astype("float32").reshape(1, -1)
    index = faiss.read_index("file_index.faiss")

    with open("file_paths.json", "r") as f:
        paths = json.load(f)

    D, I = index.search(query_embedding, len(paths))
    results = [paths[i] for i in I[0]]
    return results

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["index", "search"])
    parser.add_argument("--path", help="Directory to index")
    parser.add_argument("--query", help="Search query")

    args = parser.parse_args()

    if args.action == "index" and args.path:
        index_files(args.path)
    elif args.action == "search" and args.query:
        matches = semantic_search(args.query)
        for match in matches:
            print(match)