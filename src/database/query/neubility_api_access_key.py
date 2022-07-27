from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.sql.expression import null
from typing import List
from sqlalchemy.orm.session import Session
from fastapi.params import Depends
from src.database.database import database
from src.database.models.neubility_api_access_key_model import NeubilityApiAccessKeyModel
from fastapi import HTTPException

class NeubilityApiAccessKey():
    #__tablename__= "neubility_api_access_key"

    @classmethod
    def get_api_access_key_by_user_id(cls, api_key: str, database: Session) -> List[NeubilityApiAccessKeyModel]:
        api_access_key = database.query(NeubilityApiAccessKeyModel).get({'value': api_key})
        if api_access_key is None:
            raise HTTPException(
                status_code=406, detail="unauthorized key"
            )
        
        print( '-----------------{}'.format(api_access_key ))
        return list(api_access_key)


    @classmethod
    def get_api_access_key_by_value(cls, api_key: str, database: Session = Depends(database.session)) -> List[NeubilityApiAccessKeyModel]:
        print(api_key)
        print("1")
        print( type(database) )
        print("2")
        api_access_key = database.query(NeubilityApiAccessKeyModel).all()
        
        if api_access_key is None:
            raise HTTPException(
                status_code=406, detail="unauthorized key"
            )
        
        print( '-----------------{}'.format(api_access_key ))
        return list(api_access_key)