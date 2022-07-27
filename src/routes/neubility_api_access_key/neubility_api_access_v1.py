

from src.routes.neubility_api_access_key import NeubilityApiAccessKeyBaseController
from src.routes.neubility_api_access_key.services import NeubilityApiAccessKeyHandler

from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from fastapi.params import Depends
from src.database.database import database
from sqlalchemy.orm.session import Session


neubility_api_access_key_v1_router = InferringRouter()


@cbv(neubility_api_access_key_v1_router)
class NeubilityApiAccessKeyController(NeubilityApiAccessKeyBaseController):
    @neubility_api_access_key_v1_router.get("/value", tags=["key"])
    async def neubility_api_access_key(self, user_id: str = '', database: Session = Depends(database.session)):
        response = await NeubilityApiAccessKeyHandler.get_neubility_api_access_key_by_user_id(user_id, database)
        return {"result": response, 'message': '', 'code': 200}