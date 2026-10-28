from pydantic import BaseModel
from typing import List, Optional

class Address(BaseModel):
    street:str
    city:str
    postal_code:str

class User(BaseModel):
    id:int
    name:str
    address:Address

# below reply can be optional or there can be a list
# of replies and inside it we can have more replies which
# will be type of comments

# this below is called forward referencing
class Comment(BaseModel):
    id:int
    content:str
    replies:Optional[List['Comment']] = None

Comment.model_rebuild()

address = Address(
    street = "123 road",
    city="Banglore",
    postal_code=1020
)

user = User(
    id=1,
    name="Ritik",
    address=address
)

comment = Comment(
    id=1,
    content="first comment",
    replies = [
        Comment(id=2,content="reply1"),
        Comment(id=3,content="reply2")
    ]
)