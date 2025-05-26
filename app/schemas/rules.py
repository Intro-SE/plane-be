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

class RulesCreate(BaseModel):
    SOLUONGSANBAYTOIDA: int = Field(default=10, ge=0)
    SOLUONGSANBAYTRUNGGIANTOIDA: int = Field(default=2, ge=0)
    THOIGIANBAYTOITHIEU: int = Field(default=30, gt=0)
    THOIGIANDUNGTOIDA: int = Field(default=20)
    THOIGIANDUNGTOITHIEU: int = Field(default=10, gt=0)
    THOIGIANCHAMNHATDATVE: int = Field(default=1, gt=0)
    THOIGIANCHAMNHATHUYDATVE: int = Field(default=1, gt=0)

    class Config:
        from_attributes = True

class RulesUpdate(BaseModel):
    SOLUONGSANBAYTOIDA: int | None = Field(None, ge=0)
    SOLUONGSANBAYTRUNGGIANTOIDA: int | None = Field(None, ge=0)
    THOIGIANBAYTOITHIEU: int | None = Field(None, gt=0)
    THOIGIANDUNGTOIDA: int | None = None
    THOIGIANDUNGTOITHIEU: int | None = Field(None, gt=0)
    THOIGIANCHAMNHATDATVE: int | None = Field(None, gt=0)
    THOIGIANCHAMNHATHUYDATVE: int | None = Field(None, gt=0)

    class Config:
        from_attributes = True

class RulesInDB(RulesBase):
    @property
    def thoi_gian_bay_format(self) -> str:
        return f"{self.THOIGIANBAYTOITHIEU} phút"

    @property
    def thoi_gian_dung_format(self) -> str:
        return f"{self.THOIGIANDUNGTOITHIEU} - {self.THOIGIANDUNGTOIDA} phút"

    @property
    def thoi_gian_dat_ve_format(self) -> str:
        return f"{self.THOIGIANCHAMNHATDATVE} giờ trước giờ bay"

    @property
    def thoi_gian_huy_ve_format(self) -> str:
        return f"{self.THOIGIANCHAMNHATHUYDATVE} giờ trước giờ bay"

    class Config:
        from_attributes = True 