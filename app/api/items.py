from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel

# 创建路由器
router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={404: {"description": "未找到"}},
)

# 定义数据模型
class Item(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    price: float
    is_available: bool = True

# 模拟数据库
items_db = [
    Item(id=1, name="笔记本电脑", description="高性能笔记本电脑", price=5999.99),
    Item(id=2, name="智能手机", description="最新款智能手机", price=3999.99),
]

# 获取所有商品
@router.get("/", response_model=List[Item])
async def get_items():
    return items_db

# 获取单个商品
@router.get("/{item_id}", response_model=Item)
async def get_item(item_id: int):
    for item in items_db:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="商品未找到")

# 创建新商品
@router.post("/", response_model=Item)
async def create_item(item: Item):
    # 生成新ID
    new_id = max([i.id for i in items_db], default=0) + 1
    new_item = Item(
        id=new_id,
        name=item.name,
        description=item.description,
        price=item.price,
        is_available=item.is_available
    )
    items_db.append(new_item)
    return new_item

# 更新商品
@router.put("/{item_id}", response_model=Item)
async def update_item(item_id: int, item: Item):
    for i, stored_item in enumerate(items_db):
        if stored_item.id == item_id:
            updated_item = Item(
                id=item_id,
                name=item.name,
                description=item.description,
                price=item.price,
                is_available=item.is_available
            )
            items_db[i] = updated_item
            return updated_item
    raise HTTPException(status_code=404, detail="商品未找到")

# 删除商品
@router.delete("/{item_id}")
async def delete_item(item_id: int):
    for i, stored_item in enumerate(items_db):
        if stored_item.id == item_id:
            del items_db[i]
            return {"message": "商品已删除"}
    raise HTTPException(status_code=404, detail="商品未找到") 