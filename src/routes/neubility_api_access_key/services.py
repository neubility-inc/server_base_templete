import datetime
from sqlalchemy.orm.session import Session

from src.routes.neubility_api_access_key import NeubilityApiAccessKeyBaseHandler
from src.database.repository.neubility_api_access_key import NeubilityApiAccessKey

class NeubilityApiAccessKeyHandler(NeubilityApiAccessKeyBaseHandler):
    pass
    #@classmethod
    #async def get_connect_info(cls, mcno: int = None):
        #connect_info = await ConnectInfoCollection.get_connect_info(mcno)
        #return connect_info
    
    @classmethod
    async def get_neubility_api_access_key_by_user_id(cls, user_id: str, database: Session):
        access_key = await NeubilityApiAccessKey.get_api_access_key_by_user_id( user_id, database )
        print("-------------{}".format( access_key ))
        return 0