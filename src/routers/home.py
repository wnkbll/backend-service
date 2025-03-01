from fastapi import APIRouter

router = APIRouter()


@router.get("/", name="home")
async def home():
    return {"message": "OK"}
