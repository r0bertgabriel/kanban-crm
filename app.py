from fastapi import Depends, FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from backend.database import engine, get_db
from backend.models.models import Base
from backend.routes import admin, auth, vendedor
from backend.utils.populate import populate_database
from backend.websocket import manager

# Criar tabelas
Base.metadata.create_all(bind=engine)

# FastAPI App
app = FastAPI(
    title="CRM Kanban - Sistema de Vendas",
    description="Sistema completo de CRM com distribuição inteligente de clientes",
    version="2.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rotas
app.include_router(auth.router)
app.include_router(vendedor.router)
app.include_router(admin.router)

# WebSocket
@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await manager.connect(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_text()
            # Processar mensagens se necessário
    except WebSocketDisconnect:
        manager.disconnect(user_id)

# Rota raiz
@app.get("/")
async def read_root():
    return FileResponse("static/index.html")

@app.get("/admin")
async def read_admin():
    return FileResponse("static/admin.html")

# Popular banco na inicialização
@app.on_event("startup")
async def startup_event():
    db = next(get_db())
    try:
        populate_database(db)
    finally:
        db.close()

# Servir arquivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
