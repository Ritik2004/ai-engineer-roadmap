from pydantic import BaseModel,Field,field_validator, model_validator,computed_field

class Booking(BaseModel):
    use_id:int
    room_id:int
    nights:int=Field(...,ge=1)
    rate_per_night=float

    @computed_field
    @property
    def total_amount(self)->float:
        return self.nights*self.rate_per_night