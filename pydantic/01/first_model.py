from pydantic import BaseModel

class User(BaseModel):
    id:int
    name:str
    is_active:bool

# below we have id as it , but if we put it as string as well pydantic will
# automatically conver tot int

input_data = {'id':101,'name':'ritik','is_active':True}
user = User(**input_data)
print(user)
