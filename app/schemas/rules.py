from pydantic import BaseModel, Field

class RulesBase(BaseModel):
    soluongsanbaytoida: int = Field(default=10, ge=0)
    soluongsanbaytrunggiantoida: int = Field(default=2, ge=0)
    thoigianbaytoithieu: int = Field(default=30, gt=0)
    thoigiandungtoida: int = Field(default=20)
    thoigiandungtoithieu: int = Field(default=10, gt=0)
    thoigianchamnhatdatve: int = Field(default=1, gt=0)
    thoigianchamnhathuydatve: int = Field(default=1, gt=0)

    class Config:
        from_attributes = True

class RulesCreate(BaseModel):
    soluongsanbaytoida: int = Field(default=10, ge=0)
    soluongsanbaytrunggiantoida: int = Field(default=2, ge=0)
    thoigianbaytoithieu: int = Field(default=30, gt=0)
    thoigiandungtoida: int = Field(default=20)
    thoigiandungtoithieu: int = Field(default=10, gt=0)
    thoigianchamnhatdatve: int = Field(default=1, gt=0)
    thoigianchamnhathuydatve: int = Field(default=1, gt=0)

    class Config:
        from_attributes = True

class RulesUpdate(BaseModel):
    soluongsanbaytoida: int | None = Field(None, ge=0)
    soluongsanbaytrunggiantoida: int | None = Field(None, ge=0)
    thoigianbaytoithieu: int | None = Field(None, gt=0)
    thoigiandungtoida: int | None = None
    thoigiandungtoithieu: int | None = Field(None, gt=0)
    thoigianchamnhatdatve: int | None = Field(None, gt=0)
    thoigianchamnhathuydatve: int | None = Field(None, gt=0)

    class Config:
        from_attributes = True

class RulesInDB(RulesBase):
    @property
    def thoi_gian_bay_format(self) -> str:
        return f"{self.thoigianbaytoithieu} phút"

    @property
    def thoi_gian_dung_format(self) -> str:
        return f"{self.thoigiandungtoithieu} - {self.thoigiandungtoida} phút"

    @property
    def thoi_gian_dat_ve_format(self) -> str:
        return f"{self.thoigianchamnhatdatve} giờ trước giờ bay"

    @property
    def thoi_gian_huy_ve_format(self) -> str:
        return f"{self.thoigianchamnhathuydatve} giờ trước giờ bay"

    class Config:
        from_attributes = True 