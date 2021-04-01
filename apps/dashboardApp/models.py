from django.db import models
from django.db import models
from django.db.models.fields import DateTimeField, TextField, IntegerField
from ..loginApp.models import User

class UserMoreInfoManager(models.Manager):

    def user_level_validator(self,post_data): #'tipo: register o login'
        errors = {}

        user_level = int(post_data["user_level"])

        if user_level:
            if user_level < 1 or user_level > 9:
                errors["user_level"] = "User Level must be between 1[normal] to 9[admmin]"
        else:
            errors["user_level"] = "User Level is undefined! [1-9]"

        if (self.filter(user_level = 9).count() <= 1 and 
        user_level < 9 and 
        self.get(user_id = int(post_data["id"])).user_level == 9):
            errors["user_level"]=f"User {self.get(user_id = int(post_data['id'])).user.full_name} is the only Admin!"
        
        return errors

class UserMoreInfo(models.Model):
    user = models.OneToOneField(User, related_name="user_proxy", on_delete=models.CASCADE)
    user_level = models.IntegerField(default=1)
    description = TextField()
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    objects = UserMoreInfoManager()

    @property
    def level_name(self):
        if (self.user_level == 9):
            return "admin"
        else:
            return "normal"

