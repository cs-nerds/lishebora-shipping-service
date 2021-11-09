from fastapi import FastAPI

app = FastAPI(
    title="Lishe Bora Shipping Service",
    description="Fast API service for lishe bora shipping service"
)



@app.get("/")
def root():
    return {"message": "Hello from shipping service"}