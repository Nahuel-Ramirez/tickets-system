from app.database import SessionLocal

def test_connection():
    try:
        db = SessionLocal()
        print("Conexion a la base de datos exitosa")
    except Exception as e:
        print(f"Error de conexion: {e}")
    finally:
        db.close()

test_connection()
