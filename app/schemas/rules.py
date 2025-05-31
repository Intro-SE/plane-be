from pydantic import BaseModel, Field

class RuleBase(BaseModel):
    max_airports: int = Field(default=10, ge=0)
    max_transit_airports: int = Field(default=2, ge=0)
    min_flight_time: int = Field(default=30, gt=0)
    max_transit_time: int = Field(default=20)
    min_transit_time: int = Field(default=10, gt=0)
    latest_booking_time: int = Field(default=1, gt=0)
    latest_cancel_time: int = Field(default=1, gt=0)

    class Config:
        from_attributes = True

class RuleCreate(BaseModel):
    max_airports: int = Field(default=10, ge=0)
    max_transit_airports: int = Field(default=2, ge=0)
    min_flight_time: int = Field(default=30, gt=0)
    max_transit_time: int = Field(default=20)
    min_transit_time: int = Field(default=10, gt=0)
    latest_booking_time: int = Field(default=1, gt=0)
    latest_cancel_time: int = Field(default=1, gt=0)

    class Config:
        from_attributes = True

class RuleUpdate(BaseModel):
    max_airports: int | None = Field(None, ge=0)
    max_transit_airports: int | None = Field(None, ge=0)
    min_flight_time: int | None = Field(None, gt=0)
    max_transit_time: int | None = None
    min_transit_time: int | None = Field(None, gt=0)
    latest_booking_time: int | None = Field(None, gt=0)
    latest_cancel_time: int | None = Field(None, gt=0)

    class Config:
        from_attributes = True

class RuleInDB(RuleBase):
    @property
    def flight_time_format(self) -> str:
        return f"{self.min_flight_time} minutes"

    @property
    def transit_time_format(self) -> str:
        return f"{self.min_transit_time} - {self.max_transit_time} minutes"

    @property
    def booking_time_format(self) -> str:
        return f"{self.latest_booking_time} hours before departure"

    @property
    def cancel_time_format(self) -> str:
        return f"{self.latest_cancel_time} hours before departure"

    class Config:
        from_attributes = True