from fastapi import FastAPI
from routes.user_routes import router as user_router
from routes.product_routes import router as product_router
from routes.order_routes import router as order_router

app = FastAPI()

app.include_router(user_router)
app.include_router(product_router)
app.include_router(order_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

