import peewee as pw
from models.user import User
from models.base_model import BaseModel
from playhouse.hybrid import hybrid_property

class Image(BaseModel):
    image_url = pw.TextField(null=False)
    user = pw.ForeignKeyField(User, backref="images", on_delete="CASCADE")

    @hybrid_property
    def full_image_path(self):
        from app import app
        return app.config.get("S3_LOCATION") + self.image_url