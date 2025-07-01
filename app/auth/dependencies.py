from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.usuario import Usuario
from app.utils.auth import SECRET_KEY, ALGORITHM
from app.models.usuario import RolUsuario

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login") #Ruta del login

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Devuelve usuario autenticado a partir del token
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate":"Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(Usuario).filter(Usuario.email == email).first()
    if user is None:
        raise credentials_exception
    return user


def is_admin(user: Usuario = Depends(get_current_user)):
    if user.rol != RolUsuario.admin:
        raise HTTPException(status_code=403, detail="Solo el administrador puede realizar esta acción.")
    return user

def is_operador(user: Usuario = Depends(get_current_user)):
    if user.rol not in [RolUsuario.admin, RolUsuario.operador]:
        raise HTTPException(status_code=403, detail="Solo operadores o administradores pueden realizar esta acción.")
    return user
