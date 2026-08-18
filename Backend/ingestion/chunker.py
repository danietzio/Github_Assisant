from sqlalchemy.ext.asyncio import AsyncSession
from models import Repository, CodeChunk
from pathlib import Path
from embedder import local_embedder

async def chunk_repository(db: AsyncSession, repo: Repository) -> list[CodeChunk]:

  repo_path = Path(repo.local_path)
  allowed_extensions = [".py", ".js", ".jsx", ".ts"]
  SPLIT_SIZE = 50
  chunk_list: list[CodeChunk] = []

  for file in repo_path.rglob("*"):
    if file.is_file() and file.suffix in allowed_extensions:
      content = file.read_text()
      lines = content.splitlines()

      for start in range(0, len(lines), SPLIT_SIZE):
        chunk_lines = lines[start:start+SPLIT_SIZE]
        chunk = "\n".join(chunk_lines)
        new_chunk = CodeChunk(
            local_path=str(file.relative_to(repo_path)),
            repository_id=repo.id,
            start_line=start + 1,
            finish_line=start + len(chunk_lines),
            content=chunk,
            embedding=local_embedder(chunk)
          )

        db.add(new_chunk)
        chunk_list.append(new_chunk)

        
  await db.commit()

  return chunk_list
