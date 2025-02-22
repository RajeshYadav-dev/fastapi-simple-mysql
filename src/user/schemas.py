from pydantic import BaseModel

# User model
class UserModel(BaseModel):
    username: str
    password: str
    email: str
    
# User model
class LoginUserModel(BaseModel):
    email: str
    password: str    