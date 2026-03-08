from fastapi import APIRouter
from services.aof_service import AOFService

router = APIRouter(prefix="/aof", tags=["AOF Management"])

@router.get("/status")
def get_aof_status():
    return AOFService.get_aof_status()

@router.post("/rewrite")
def trigger_aof_rewrite():
    return AOFService.trigger_aof_rewrite()