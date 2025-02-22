import hashlib
import mysql.connector
from user.schemas import UserModel,LoginUserModel
from database import dbcon


class UserService():    
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
      

        
  