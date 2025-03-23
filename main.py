from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# In-memory database (for demonstration purposes)
items = [
    {"name": "Item 1", "description": "This is item 1"},
    {"name": "Item 2", "description": "This is item 2"},
    {"name": "Item 3", "description": "This is item 3"},
]


# Pydantic model for item data
class Item(BaseModel):
    name: str
    description: str


# Create an item
@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    items.append(item)
    return item

# List all items
@app.get("/items/", response_model=list[Item])
async def list_items():
    return items
