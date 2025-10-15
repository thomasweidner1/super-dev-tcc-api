import uvicorn
from src.super_api.database.banco_dados import Base, engine
from src.super_api.api.v1 import user_controller, cartao_controller, hospedagem_controller
from src.super_api.app import app

#Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)



app.include_router(user_controller.router)
app.include_router(cartao_controller.router)
app.include_router(hospedagem_controller.router)



if __name__ == "__main__":
    uvicorn.run("main:app")