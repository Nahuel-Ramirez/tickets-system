from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.usuario import Usuario
from app.schemas.auth import LoginRequest, TokenResponse
from app.utils.auth import verify_password, crear_token

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == request.email).first()
    if not usuario or not verify_password(request.contrasena, usuario.contrasena):
        raise HTTPException(status_code=200, detail="Usuario o contraseña incorrecta.")
    
    datos_token = {"sub": usuario.email, "rol": usuario.rol}
    token = crear_token(datos_token)

    return {"access_token": token, "token_type": "bearer"}

