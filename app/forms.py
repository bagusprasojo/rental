from wtforms import Form, StringField, SelectField

class CustomerForm(Form):    
    name = StringField('Name')
    city = StringField('City')
    addr = StringField('Address')
    pin = StringField('Post Code')