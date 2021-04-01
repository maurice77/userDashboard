
from django.db import models
from django.db.models.fields import CharField, DateTimeField, EmailField
import bcrypt
import re #Regex

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):

    def chk_pass(self,email,passwd):
        user = self.filter(email = email)
        print(user)

        if user:
            return bcrypt.checkpw(passwd.encode(),user[0].password.encode())

        return False

    def email_exists(self,email,exclude_id = 0):
        if exclude_id == 0:
            return self.filter(email = email)
        else:
            return self.filter(email = email).exclude(id = exclude_id)

    def email_validator(self,email,tipo,exclude_id = 0): #'tipo: register o login'
        errors = {}
        if email == "":
            errors["email"] = "Email is required!"
        elif not EMAIL_REGEX.match(email):    # probar si un campo coincide con el patrón        
            errors["email"] = "Invalid email address!"
        elif tipo == "register":
            if self.email_exists(email,exclude_id):
                errors["email"] = "Email already exists in the DB!"

        return errors

    def login_validator(self,post_data): #para el login
        errors = {}

        field_name = "email"
        field_value = post_data["email"]
        if field_value == "":
            errors[field_name] = "Email is required!"
        
        #if not self.email_exists(field_value) or not self.chk_pass(post_data["password"]):
        if not self.chk_pass(post_data["email"],post_data["password"]): #esta rutina chequea la existencia del mail...
            errors[field_name] = "Incorrect email and/or password!"

        return errors

    def datagral_validator(self,post_data):
        return self.user_validator(post_data,True,False)

    def password_validator(self,post_data):
        return self.user_validator(post_data,False,True)

    def user_validator(self,post_data,chkDataGral = True,chkPass = True):
        errors = {}

        if chkDataGral:

            field_name = "email"
            field_value = post_data[field_name]
            if "id" in post_data:
                email_errors = self.email_validator(field_value,"register",exclude_id=post_data["id"])
            else:
                email_errors = self.email_validator(field_value,"register")
            if email_errors:
                errors[field_name] = email_errors["email"]

            field_name = "first_name"
            field_value = post_data[field_name]
            if field_value == "":
                errors[field_name] = "First Name is required!"
            elif len(field_value)<2 or len(field_value)>100:
                errors[field_name] = "First Name must be between 2 and 100 characters."

            field_name = "last_name"
            field_value = post_data[field_name]
            if field_value == "":
                errors[field_name] = "Last Name is required!"
            elif len(field_value)<2 or len(field_value)>100:
                errors[field_name] = "Last Name must be between 2 and 100 characters."

        if chkPass:
            field_name = "password"
            field_value = post_data[field_name]
            if field_value == "":
                errors[field_name] = "Password is required!"
            elif len(field_value)<8 or len(field_value)>50:
                errors[field_name] = "Password must be between 8 and 100 characters."
            elif post_data['confirm_password'] == "":
                errors["confirm_password"] = "Confirm password please!"
            elif field_value != post_data["confirm_password"]:
                errors["confirm_password"] = "Password and confirmation do not match. Please check!" 

        return errors

class User(models.Model):
    email = EmailField(max_length=100, unique = True)
    first_name = CharField(max_length=100)
    last_name = CharField(max_length=100)
    password = CharField(max_length=100)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    #user_proxy
    #messages_from
    #messages_for
    #comments

    objects = UserManager()

    @property
    def full_name(self):
        return  f"{self.first_name} {self.last_name}" #'%s %s' % (self.first_name, self.last_name)


