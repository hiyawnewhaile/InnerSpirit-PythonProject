from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

class User():
    def __init__(self, data):
        self.id = data['id']
        self.first_name  = data['first_name']
        self.last_name  = data['last_name']
        self.email  = data['email']
        self.password  = data['password']
        self.created_at  = data['created_at']
        self.updated_at  = data['updated_at']

    @staticmethod
    def validate_user(data):
        
        is_valid = True

        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if len(data['first_name']) < 3 or len(data['first_name'])> 20:
            is_valid = False
            flash("First Name must be atleast 3 characters, up to 20 characters")

        if len(data['last_name']) < 3 or len(data['last_name'])> 20:
            is_valid = False
            flash("Last Name must be atleast 3 characters, up to 20 characters")

        # email must be unique
        if len(User.get_user_by_email(data)) != 0:
            is_valid = False
            flash("E-mail is already registered")

        if not email_regex.match(data['email']):
            is_valid = False
            flash("Please provide a valid e-mail")

        if len(data['password']) < 8 or len(data['password']) > 20:
            is_valid = False
            flash("password must be atleast 8 characters long and less that 20 characters")

        if data['password'] != data['confirm_password']:
            is_valid = False
            flash("passwords must match")

        return is_valid

    @classmethod
    def create_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUE(%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        
        results = connectToMySQL('inner_spirit_schema').query_db(query, data)

        return results

    @classmethod
    def get_user_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"

        results = connectToMySQL('inner_spirit_schema').query_db(query, data)

        users = []

        for user in results:
            users.append(User(user))

        return users