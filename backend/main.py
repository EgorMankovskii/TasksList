from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

tasks = []
current_id = 0


class Item(BaseModel):
    id: int = None
    title: str
    completed: bool = False


@app.get("/items")
def items(completed: Optional[bool] = None):
    if completed is None:
        return tasks
    else:
        return list(filter(lambda item: item["completed"] == completed, tasks))


@app.get("/items/{item_id}")
def find_item(item_id: int):
    for task in tasks:
        if task["id"] == item_id:
            break
    else:
        raise HTTPException(status_code=404, detail="Item not found")
    return task


@app.post("/items")
def create_item(item: Item):
    global current_id
    current_id += 1
    item.id = current_id
    tasks.append(item.model_dump())
    return item


@app.put("/items/{item_id}")
def update_item(item_id: int, updated_item: Item):
    for task in tasks:
        if task["id"] == item_id:
            data = updated_item.model_dump()
            data["id"] = task["id"]
            task.update(data)
            break
    else:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_item


@app.put("/items/{item_id}/completed")
def update_item_completed(item_id: int):
    for task in tasks:
        if task["id"] == item_id:
            task["completed"] = not task["completed"]
            break
    else:
        raise HTTPException(status_code=404, detail="Item not found")
    return task


@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    for task in tasks:
        if task["id"] == item_id:
            tasks.remove(task)
            break
    else:
        raise HTTPException(status_code=404, detail="Item not found")
    return tasks