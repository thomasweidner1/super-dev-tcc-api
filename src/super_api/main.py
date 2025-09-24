import uvicorn
from src.super_api.database.banco_dados import Base, engine, popular_banco_dados
from src.super_api.api.v1 import user_controller
from src.super_api.app import app

# Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
popular_banco_dados()


app.include_router(user_controller.router)



if __name__ == "__main__":
    uvicorn.run("main:app")