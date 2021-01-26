from models.base_model import BaseModel
import peewee as pw
from werkzeug.security import generate_password_hash
import re
from flask_login import UserMixin
from playhouse.hybrid import hybrid_property


class User(UserMixin, BaseModel):
    username = pw.CharField(unique=False)
    email = pw.CharField(unique=True, null=False)
    password_hash = pw.TextField(null=False)
    password = None
    image_path = pw.TextField(null=True)

    def follow(self,idol):
        from models.fanidol import FanIdol
        if self.follow_status(idol)== None:
            relationship = FanIdol(idol=idol, fan=self.id)
            if not idol.is_private:
                relationship.is_approved = True
            return relationship.save()
        else:
            return 0

    def unfollow(self, idol):
        from models.fanidol import FanIdol
        return FanIdol.delete().where(FanIdol.fan==self.id,FanIdol.idol==idol).execute()


    def follow_status(self,idol):
        from models.fanidol import FanIdol
        return FanIdol.get_or_none(FanIdol.fan==self.id, FanIdol.idol==idol.id)


    @hybrid_property
    def idols(self):
        from models.fanidol import FanIdol
        idols = FanIdol.select(FanIdol.idol).where(FanIdol.fan==self.id, FanIdol.is_approved==True)
        return User.select().where( User.id.in_(idols))

    @hybrid_property
    def fans(self):
        from models.fanidol import FanIdol
        fans = FanIdol.select(FanIdol.fan).where(FanIdol.idol==self.id, FanIdol.is_approved==True)
        return User.select().where( User.id.in_(fans))

    @hybrid_property
    def idol_requests(self):
        from models.fanidol import FanIdol
        idols = FanIdol.select(FanIdol.idol).where(FanIdol.fan==self.id, FanIdol.is_approved==False)
        return User.select().where( User.id.in_(idols) )

    @hybrid_property
    def fan_requests(self):
        from models.fanidol import FanIdol
        fans = FanIdol.select(FanIdol.fan).where(FanIdol.idol==self.id, FanIdol.is_approved==False)
        return User.select().where( User.id.in_(fans))

    def approve_request(self, fan):
        from models.fanidol import FanIdol
        relationship = fan.follow_status(self)
        relationship.is_approved = True
        return relationship.save()

    @hybrid_property
    def full_image_path(self):
        if self.image_path:
            from app import app
            return app.config.get("S3_LOCATION") + self.image_path
        else:
            return ""



    def validate(self):
        #email unique
        existing_user_email = User.get_or_none(User.email == self.email)
        if existing_user_email and existing_user_email.id != self.id:
            self.errors.append (f'User with email: {self.email} already exists.')
        #username unique
        existing_user_username = User.get_or_none(User.username == self.username)
        if existing_user_username and existing_user_username.id != self.id:
            self.errors.append (f'User with username: {self.username} already exist.')

        # Password should be longer than 6 characters
        if self.password:
            if len(self.password) <= 6:
                self.errors.append ('Please provide password more than 6 characters.')

            # Password should have both uppercase and lowercase characters
            # Password should have at least one special character 
            has_lower = re.search (r"[a-z]", self.password)
            has_upper = re.search (r"[A-Z]", self.password)
            has_special = re.search (r"[ \! \# \$ \% \& \' \( \) \* \+ \, \- \. \/ \: \; \< \= \> \? \@ \[ \\ \] \^ \_ \` \{ \| \} \~ ]", self.password)

            if has_lower and has_upper and has_special:
                self.password_hash = generate_password_hash(self.password)
            else:
                self.errors.append ("Password must contain uppercase, lowercase and special character.")
