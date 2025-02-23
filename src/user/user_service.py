import hashlib
import mysql.connector
from user.schemas import UserModel,LoginUserModel
from database import dbcon


class UserService():    
  
  def get_users(self):
    mydb = dbcon.get_db_connection()
    cursor = mydb.cursor(dictionary=True)
    try:
      cursor.execute("SELECT * FROM user;")
      users = cursor.fetchall()
      if len(users)>0:
        return users
    except mysql.connector.Error as err:
        raise Exception(f"Something went wrong:{err}")
    finally:
      cursor.close()
      mydb.close()
      
  
  def get_a_user(self,user_id: int):
    mydb = dbcon.get_db_connection()
    cursor = mydb.cursor(dictionary=True)
    try:
      cursor.execute("SELECT * FROM user WHERE id = %s;", (user_id,))
      user = cursor.fetchone()
      if user:
        return user
    except mysql.connector.Error as err:
        raise Exception(f"Something went wrong:{err}")
    finally:
      cursor.close()
      mydb.close()
      
  def create_a_user(self,user_data: UserModel):
    mydb = dbcon.get_db_connection()
    cursor = mydb.cursor()
    hashed_password = hashlib.sha256(user_data.password.encode()).hexdigest()
    try:
        cursor.execute(
            "INSERT INTO user (username, password, email) VALUES (%s, %s, %s);",
            (user_data.username, hashed_password, user_data.email)
        )
        mydb.commit()
        return user_data
    except mysql.connector.Error as err:
        raise Exception(f"Something went wrong:{err}")
    finally:
        cursor.close()
        mydb.close()      
    
  def update_a_user(self,user_id: int, user: UserModel):
    mydb = dbcon.get_db_connection()
    cursor = mydb.cursor()
    try:
      hashed_password = hashlib.sha256(user.password.encode()).hexdigest()
      cursor.execute(
          "UPDATE user SET username = %s, password = %s, email = %s WHERE id = %s;",
          (user.username, hashed_password, user.email, user_id)
      )
      mydb.commit()
      if cursor.rowcount == 0:
          return {"message:":"user updated"}
    except mysql.connector.Error as err:
        raise Exception(f"Something went wrong:{err}")
    finally:
      cursor.close()
      mydb.close()    
  
  
  def delete_a_user(self,user_id: int):
    mydb = dbcon.get_db_connection()
    cursor = mydb.cursor()
    try:
      cursor.execute("DELETE FROM user WHERE id = %s;", (user_id,))
      mydb.commit()
      if cursor.rowcount > 0:
        return {"message:":"user deleted"}
    except mysql.connector.Error as err:
        raise Exception(f"Something went wrong:{err}") 
    finally:
      cursor.close()
      mydb.close()
    
  def login_a_user(self,user: LoginUserModel):
    mydb = dbcon.get_db_connection()
    cursor = mydb.cursor()
    try:
      cursor.execute("SELECT * FROM user WHERE email = %s;", (user.email,))
      user = cursor.fetchone()
      if user:
          return user
      else:
        return None  
    except mysql.connector.Error as err:
        raise Exception(f"Something went wrong:{err}")
    finally:
      cursor.close()
      mydb.close()
      

        
  