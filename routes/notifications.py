from fastapi import APIRouter

router = APIRouter(prefix="/notifications", tags=["notifications"])

@router.post("/test")
async def test_notification(payload: dict):
    return {"status": "ok", "message": payload.get("message")}