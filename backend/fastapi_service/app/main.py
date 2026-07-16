from fastapi import FastAPI

app = FastAPI(title="Enterprise Commerce — Analytics Service")

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "fastapi_service"}