from pydantic import BaseModel


class CodeBase(BaseModel):
    category: str = ""
    value: str = ""
    code: int = -1
    code_desc: str = None
    memo: str = None


class CodeCreate(CodeBase):
    pass


class CodeUpdate(CodeBase):
    pass
