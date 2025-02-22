from fastapi import status, HTTPException,APIRouter
import hashlib
import mysql.connector
from user.schemas import UserModel,LoginUserModel
from database import dbcon
from user.user_service import UserService

user_router = APIRouter()
service = UserService()

# Get all users
@user_router.get("/users", status_code=status.HTTP_200_OK)
def get_users():
    mydb = dbcon.get_db_connection()
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user;")
    users = cursor.fetchall()
    cursor.close()
    mydb.close()
    return users

# Get a single user
@user_router.get("/users/{user_id}", status_code=status.HTTP_200_OK)
def get_a_user(user_id: int):
    mydb = dbcon.get_db_connection()
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user WHERE id = %s;", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    mydb.close()
    if user:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

# Create a user
@user_router.post("/", status_code=status.HTTP_201_CREATED)
def create_a_user(user: UserModel):
    mydb = dbcon.get_db_connection()
    cursor = mydb.cursor()
    hashed_password = hashlib.sha256(user.password.encode()).hexdigest()
    try:
        cursor.execute(
            "INSERT INTO user (username, password, email) VALUES (%s, %s, %s);",
            (user.username, hashed_password, user.email)
        )
        mydb.commit()
        user_id = cursor.lastrowid
    except mysql.connector.Error as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error: {err}")
    finally:
        cursor.close()
        mydb.close()
    return {"message": "User added successfully.", "user_id": user_id}

# Update a user
@user_router.put("/{user_id}", status_code=status.HTTP_200_OK)
def update_a_user(user_id: int, user: UserModel):
    mydb = dbcon.get_db_connection()
    cursor = mydb.cursor()
    hashed_password = hashlib.sha256(user.password.encode()).hexdigest()
    cursor.execute(
        "UPDATE user SET username = %s, password = %s, email = %s WHERE id = %s;",
        (user.username, hashed_password, user.email, user_id)
    )
    mydb.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    cursor.close()
    mydb.close()
    return {"message": "User updated successfully."}

# Delete a user
@user_router.delete("/{user_id}", status_code=status.HTTP_200_OK)
def delete_a_user(user_id: int):
    mydb = dbcon.get_db_connection()
    cursor = mydb.cursor()
    cursor.execute("DELETE FROM user WHERE id = %s;", (user_id,))
    mydb.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    cursor.close()
    mydb.close()
    return {"message": "User deleted successfully."}


# Create a user
@user_router.post("/login", status_code=status.HTTP_200_OK)
def login_a_user(user: LoginUserModel):
    dbuser=service.login_a_user(user)
    if dbuser[3]==user.email:
        return {"message:":"Login successful"}
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Login Failed..")
   
