from fastapi import FastAPI

app = FastAPI(title="N2P-CRM01 API", version="1.0.0")

@app.get("/")
def read_root():
    return {"message": "N2P-CRM01 API is running!"}

@app.get("/health")
def health_check():
    return {"status": "ok"}
