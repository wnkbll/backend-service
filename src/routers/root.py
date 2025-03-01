from fastapi import APIRouter

router = APIRouter()


@router.get("/", name="default:root")
async def root():
    return {"message": "OK"}
