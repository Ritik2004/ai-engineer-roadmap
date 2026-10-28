from pydantic import BaseModel, Field
from typing import Optional

# field helps to write more details and value
# to a Field

# ... signify that this field is required not optional
class Employee(BaseModel):
    id:int
    name:str=Field(
        ...,
        min_length=3,
        max_length=50,
        description="Employee name",
        example="Ritik"
    )
    department:Optional[str]='General'
    salary:float=Field(...,ge=10000)
