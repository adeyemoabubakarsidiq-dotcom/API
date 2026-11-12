from __future__ import annotations
 
from typing import Any
from uuid import uuid4
 
from fastapi import FastAPI, HTTPException, status
 
app = FastAPI(title="Backend Engineering API", version="0.1.0")
 
ITEMS: dict[str, dict[str, Any]] = {}
 
 
@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
 
 
@app.get("/items")
def list_items(q: str | None = None, limit: int = 20) -> list[dict[str, Any]]:
    items = list(ITEMS.values())
    if q:
        q_lower = q.lower()
        items = [i for i in items if q_lower in str(i.get("name", "")).lower()]
    return items[: max(limit, 0)]
 
 
@app.get("/items/{item_id}")
def get_item(item_id: str) -> dict[str, Any]:
    if item_id not in ITEMS:
        raise HTTPException(status_code=404, detail="Item not found")
    return ITEMS[item_id]
@app.post("/items", status_code=status.HTTP_201_CREATED)
def create_item(body: dict[str, Any]) -> dict[str, Any]:
    name = body.get("name")
    price = body.get("price")
    if not isinstance(name, str) or not isinstance(price, (int, float)):
        raise HTTPException(status_code=400, detail="name:str and price:number required")
    item_id = str(uuid4())[:8]
    item = {"id": item_id, "name": name, "price": float(price)}
    ITEMS[item_id] = item
    return item
 
 
@app.put("/items/{item_id}")
def replace_item(item_id: str, body: dict[str, Any]) -> dict[str, Any]:
    if item_id not in ITEMS:
        raise HTTPException(status_code=404, detail="Item not found")
    name = body.get("name")
    price = body.get("price")
    if not isinstance(name, str) or not isinstance(price, (int, float)):
        raise HTTPException(status_code=400, detail="name:str and price:number required")
    item = {"id": item_id, "name": name, "price": float(price)}
    ITEMS[item_id] = item
    return item
 
 
@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: str) -> None:
    if item_id not in ITEMS:
        raise HTTPException(status_code=404, detail="Item not found")
    del ITEMS[item_id]
