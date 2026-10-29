from fastapi import FastAPI

app = FastAPI(title="Toutiao Backend")


@app.get("/")
async def read_root() -> dict[str, str]:
    return {"message": "Toutiao Backend API"}

# uv run uvicorn main:app --reload