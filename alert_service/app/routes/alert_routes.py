from fastapi import APIRouter, Depends, Request

from ..services.alert_handler import AlertService


alert_router = APIRouter(prefix="/alert")


def get_alert_service():
    return AlertService()


@alert_router.post("/")
async def receive_alert(
    request: Request, alert_service: AlertService = Depends(get_alert_service)
):
    data = await request.json()
    alert_service.handle_alert(data)
    return {"message": "Alert received"}
