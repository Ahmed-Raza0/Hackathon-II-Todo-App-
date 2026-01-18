from fastapi import FastAPI

app = FastAPI(title="Todo Phase III API")

@app.get("/health")
def health():
    return {"status": "ok"}