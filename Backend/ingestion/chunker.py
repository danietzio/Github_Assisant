from sqlalchemy.ext.asyncio import AsyncSession

from models import Repository, CodeChunk

from pathlib import Path

from ingestion.embedder import local_embedder


async def chunk_repository(
    db: AsyncSession,
    repo: Repository
) -> list[CodeChunk]:

    repo_path = Path(repo.local_path)

    allowed_extensions = {".py", ".js", ".jsx", ".ts"}

    SPLIT_SIZE = 50

    chunk_data = []

    # 1. Find files and create chunks
    for file in repo_path.rglob("*"):

        if not file.is_file():
            continue

        if file.suffix not in allowed_extensions:
            continue

        content = file.read_text(
            encoding="utf-8",
            errors="ignore"
        )

        lines = content.splitlines()

        for start in range(0, len(lines), SPLIT_SIZE):

            chunk_lines = lines[start:start + SPLIT_SIZE]

            chunk = "\n".join(chunk_lines)

            chunk_data.append({
                "local_path": str(file.relative_to(repo_path)),
                "start_line": start + 1,
                "finish_line": start + len(chunk_lines),
                "content": chunk,
            })

    print(f"Created {len(chunk_data)} chunks")

    # 2. Embed all chunks in batches
    texts = [
        chunk["content"]
        for chunk in chunk_data
    ]

    embeddings = local_embedder(texts)

    print(f"Created {len(embeddings)} embeddings")

    # 3. Create database objects
    chunk_list = []

    for data, embedding in zip(chunk_data, embeddings):

        new_chunk = CodeChunk(
            local_path=data["local_path"],
            repository_id=repo.id,
            start_line=data["start_line"],
            finish_line=data["finish_line"],
            content=data["content"],
            embedding=embedding,
        )

        db.add(new_chunk)
        chunk_list.append(new_chunk)

    # 4. One database commit
    await db.commit()

    print(f"Repo chunked: {len(chunk_list)} chunks")

    return chunk_list