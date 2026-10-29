from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from prometheus_fastapi_instrumentator import Instrumentator
import asyncio

app = FastAPI()
Instrumentator().instrument(app).expose(app)

@app.get("/health", response_class=JSONResponse)
def health_check():
    return JSONResponse(content={"status": "healthy_ok"}, status_code=200)

@app.get("/users")
def get_users():
    users = [{"id": 1, "name": "Amir"}, 
             {"id": 2, "name": "Bapi Da"},
             {"id": 3, "name": "HeartBroken Hero"},
             {"id": 4, "name": "Charlie"}]
    return users

@app.get("/products")
def get_products():
    products = [{"id": 1, "name": "Phone", "Model": "Iphone"}, 
                {"id": 2, "name": "laptop", "Model": "Asus Tuf"},
                {"id": 3, "name": "Tablet", "Model": "Samsung Tab"},
                {"id": 4, "name": "Watch", "Model": "Timex Watch"}
                ]
    return products

@app.get("/simulate_error")
def simulate_error():
    raise HTTPException(status_code=500,
                        detail="There's an error to be fixed.")

@app.get("/simulate_timeout")
async def simulate_timeout():
    await asyncio.sleep(5)
    return {"status": "timeout_success",
            "message": "Timeout simulated successfully after 5 seconds."}

@app.get("/simulate_rate_limit")
def simulate_rate_limit():
    raise HTTPException(status_code=429, detail="Rate limit exceeded.")

@app.get("/simulate_authentication_error")
def simulate_authentication_error():
    raise HTTPException(status_code=401, detail="Authentication failed.")

@app.get("/simulate_timeout_scenario_2")
async def simulate_timeout_scenario_2():
    await asyncio.sleep(30)
    return {"status": "timeout_success",
            "message": "Timeout simulated successfully after 30 seconds."}  