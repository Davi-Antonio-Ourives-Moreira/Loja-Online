import fastapi
import uvicorn
import json

app = fastapi.FastAPI()

"""
Rota de produtos da api
    """
@app.get("/produtos-loja")
def produtos():
    with open("api\data_produtos.json", "r", encoding="utf-8") as produtos_json:
        return json.load(produtos_json)
    
"""
Rodar api
    """
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, log_level="info")
