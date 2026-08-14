from fastapi import FastAPI
from app.api.embeddings import router as embeddings_router


app = FastAPI()

app.include_router(embeddings_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}