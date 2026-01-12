from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.models import Vendedor
from backend.models.schemas import VendedorLogin, VendedorResponse
from backend.utils.distribuicao import redistribuir_clientes

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/login")
async def login(vendedor_login: VendedorLogin, db: Session = Depends(get_db)):
    """Login de vendedor ou administrador"""
    vendedor = db.query(Vendedor).filter(
        Vendedor.nome == vendedor_login.nome,
        Vendedor.senha == vendedor_login.senha
    ).first()
    
    if not vendedor:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    
    vendedor.online = True
    vendedor.ultimo_acesso = datetime.now()
    db.commit()
    
    # Redistribuir clientes apenas se não for admin
    if not vendedor.is_admin:
        redistribuir_clientes(db)
    
    return {
        "id": vendedor.id,
        "nome": vendedor.nome,
        "is_admin": vendedor.is_admin
    }

@router.post("/logout/{vendedor_id}")
async def logout(vendedor_id: int, db: Session = Depends(get_db)):
    """Logout de vendedor ou administrador"""
    vendedor = db.query(Vendedor).filter(Vendedor.id == vendedor_id).first()
    if vendedor:
        vendedor.online = False
        db.commit()
        
        # Redistribuir clientes apenas se não for admin
        if not vendedor.is_admin:
            redistribuir_clientes(db)
    
    return {"message": "Logout realizado"}

@router.get("/vendedores", response_model=List[VendedorResponse])
async def get_vendedores(db: Session = Depends(get_db)):
    """Lista todos os vendedores (não inclui admins)"""
    return db.query(Vendedor).filter(Vendedor.is_admin == False).all()
