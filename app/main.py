# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.routes.users.UsersRoutes import router as users_router
from app.routes.reservations.ReservationsRoutes import router as reservations_router
from app.routes.rooms.RoomsRoutes import router as rooms_router
from app.controllers.auth.AuthController import router as auth_router


from app.database import engine, Base


from fastapi.openapi.utils import get_openapi

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version="1.0.0",
        description="API para reservas de salas",
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }

    # Añade seguridad a TODAS las rutas
    for path in openapi_schema["paths"].values():
        for operation in path.values():
            operation.setdefault("security", []).append({"BearerAuth": []})

    app.openapi_schema = openapi_schema
    return app.openapi_schema




# crear tablas si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Gestor Reservas Salas - API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(rooms_router, prefix="/rooms", tags=["Rooms"])
app.include_router(reservations_router, prefix="/reservations", tags=["Reservations"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

# Asigna esta función personalizada al app
app.openapi = custom_openapi
