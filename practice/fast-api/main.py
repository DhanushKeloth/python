from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
app = FastAPI()

items=[]
class Item(BaseModel):
    text:str
    is_done:bool=False
@app.get("/home")
def read_root():
    return {"Hello": "World"}

@app.post("/items")
def create_item(item:Item)->Item:
    items.append(item)
    return item


# @app.get("/items")
# def get_items():
#     return items

@app.get("/items/{item_id}") 
def get_item(item_id:int):
    if item_id<len(items):
        return items[item_id]
    else:
        raise HTTPException(status_code=404,detail="Item not found")
    
# request and path parameters
@app.get("/items",)
def list_items(limit:int=10):
    return items[0:limit]
 