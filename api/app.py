from fastapi import FastAPI
from analyzer.generate_apis import generate_recommended_apis

app = FastAPI()

@app.get("/")
def home():
    return {"message": "AutoAPI is running!"}

@app.get("/recommended-apis")
def recommended():
    return generate_recommended_apis()
