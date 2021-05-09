from mongoengine import Document, StringField

class Employee(Document):
    name = StringField(required=True)

    def to_dict(self):
        return {
            'name': self.name,
            '_id': str(self.id),
        }
