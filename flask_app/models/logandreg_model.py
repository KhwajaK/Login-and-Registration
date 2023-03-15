from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
import re
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 


class Users:
    DB = "login_and_registration_schema"
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
                
    @classmethod
    def get_all(cls):
        query = """
        SELECT * FROM users;
        """
        results = connectToMySQL(cls.DB).query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        return users
    
    @classmethod
    def get_one(cls, data):
        query = """
        SELECT * FROM users WHERE id = %(id)s;
        """
        results = connectToMySQL(cls.DB).query_db(query, data)
        return cls(results[0])


    @classmethod
    def save(cls, data):
        query = """
        INSERT into users (first_name, last_name, email, password)
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s); 
        """ 
        results = connectToMySQL(cls.DB).query_db(query, data)
        return results

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(cls.DB).query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @staticmethod
    def validate_new_user(user):
        is_valid = True
        if len(user['first_name']) < 2:
            flash('First name must be at least two characters')
            is_valid=False
        if len(user['last_name']) <2:
            flash('Last name must be at least two characters')
            is_valid=False            
        if not EMAIL_REGEX.match(user['email']):
            flash('Invalid email address')
            is_valid=False
        if len(user['password']) < 8 :
            flash('Password must be at least 8 characters')
            is_valid = False
        if user['conf_password'] != user['password']:
            flash('Passwords do not match, dummy')
            is_valid = False
        return is_valid
    

    # @classmethod
    # def update(cls, data):
    #     query = """
    #     UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s, password = %(password)s WHERE id = %(id)s;
    #     """
    #     return connectToMySQL(cls.DB).query_db(query,data)

    # @classmethod
    # def delete(cls, id):
    #     query= """
    #     DELETE FROM users WHERE id = %(id)s;
    #     """
    #     data = {"id": id}
    #     results = connectToMySQL(cls.DB).query_db(query, data)