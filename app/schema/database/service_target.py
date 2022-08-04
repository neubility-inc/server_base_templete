from pydantic import BaseModel


class ServiceTargetBase(BaseModel):
    service_target_name: str = None
    description: str = None


class ServiceTargetCreate(ServiceTargetBase):
    service_target_id: str


class ServiceTargetUpdate(ServiceTargetBase):
    service_target_id: str = None
