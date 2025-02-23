from fastapi import status, HTTPException,APIRouter
from user.schemas import UserModel,LoginUserModel
from user.user_service import UserService

user_router = APIRouter()
service = UserService()

# Get all users
@user_router.get("/users", status_code=status.HTTP_200_OK)
def get_users():
    return service.get_users()

# Get a single user
@user_router.get("/users/{user_id}", status_code=status.HTTP_200_OK)
def get_a_user(user_id: int):
    user=service.get_a_user(user_id)
    if user:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

# Create a user
@user_router.post("/", status_code=status.HTTP_201_CREATED)
def create_a_user(user_data: UserModel):
    user = service.create_a_user(user_data)
    if user:
        print(user)
        return user
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User details is not valid.")

# Update a user
@user_router.put("/{user_id}", status_code=status.HTTP_200_OK)
def update_a_user(user_id: int, user_data: UserModel):
    user=service.update_a_user(user_id,user_data)
    if user:
       return user
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="User detail is invalid")

# Delete a user
@user_router.delete("/{user_id}", status_code=status.HTTP_200_OK)
def delete_a_user(user_id: int):
   data=service.delete_a_user(user_id)
   if data:
       return data
   else:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user not deleted.") 

# login a user
@user_router.post("/login", status_code=status.HTTP_200_OK)
def login_a_user(user: LoginUserModel):
    dbuser=service.login_a_user(user)
    if dbuser[3]==user.email:
        return {"message:":"Login successful"}
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Login Failed..")
   
