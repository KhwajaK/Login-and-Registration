from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
from flask_app.models import logandreg_model

class Posts:
    DB= "login_and_registration_schema"
    def __init__(self,data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_name = None
    
    @classmethod
    def save_post(cls,data):
        query = """ INSERT INTO posts (user_id, content) VALUE (%(user_id)s, %(content)s)
        ;"""
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @staticmethod
    def verify_post(post):
        is_valid = True
        if len(post['content']) == 0:
            flash("Post content can not be blank")
            is_valid = False
        return is_valid
    
    @classmethod
    def all_user_posts(cls):
        query = """ SELECT * FROM posts 
        JOIN users ON posts.user_id = users.id ORDER BY posts.created_at DESC;
        """ 
        results = connectToMySQL(cls.DB).query_db(query)
        users_posts = []
        for x in results:
            one_post = cls(x)
            user_data={
                'id': x['users.id'],
                'first_name':x['first_name'],
                'last_name':x['last_name'],
                'email': x['email'],
                'password': x['password'],
                "created_at": x["created_at"],
                "updated_at": x["updated_at"]
            }
            one_post.user_name = logandreg_model.Users.display_one(user_data)
            users_posts.append(one_post)
        return users_posts
    
    @classmethod
    def delete_posts(cls, data):
        query= """
        DELETE FROM posts WHERE id = %(id)s;
        """
        return connectToMySQL(cls.DB).query_db(query, data)
    
    # data = {"id": id}