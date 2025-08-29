from fastapi import FastAPI, Depends
from sqlalchemy.orm import  Session
from app.database import get_db
from sqlalchemy import text 

app = FastAPI()

@app.get("/test-db/")
def test_db(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"message": "hola, Conexión exitosa con la base de datos"}
    except Exception as e:
        return {"error": str(e)}
