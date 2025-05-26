from pydantic import BaseModel, Field

class RulesBase(BaseModel):
    SOLUONGSANBAYTOIDA: int = Field(default=10, ge=0)
    SOLUONGSANBAYTRUNGGIANTOIDA: int = Field(default=2, ge=0)
    THOIGIANBAYTOITHIEU: int = Field(default=30, gt=0)
    THOIGIANDUNGTOIDA: int = Field(default=20)
    THOIGIANDUNGTOITHIEU: int = Field(default=10, gt=0)
    THOIGIANCHAMNHATDATVE: int = Field(default=1, gt=0)
    THOIGIANCHAMNHATHUYDATVE: int = Field(default=1, gt=0)

    class Config:
        from_attributes = True

class RulesCreate(RulesBase):
    pass

class RulesUpdate(RulesBase):
    pass

class RulesInDB(RulesBase):
    pass 