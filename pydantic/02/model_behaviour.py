# model valdator and field validator

from pydantic import BaseModel, field_validator, model_validator,computed_field


class User(BaseModel):
    username:str

    #  field_validator is a decorator
    @field_validator('username')
    # here we are passing whole class as well as value which is username here
    def username_length(cls,v):
        if len(v) < 4:
            raise ValueError("Username must be atleast 4 characters")

        return v

# model validator is used after the values are checked
class Signup(BaseModel):
    password:str
    confirm_password:str

    @model_validator(mode='after')
    def password_match(cls, values):
        if values.password != values.confirm_password:
            raise ValueError('Password do not match')
        return values

class Product(BaseModel):
    price:float
    quantity:int

    @computed_field
    @property
    def total_price(self)->float:
        return self.price * self.quantity

