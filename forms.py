from flask.ext.wtf import Form, TextField, TextAreaField, SubmitField
 
class ContactForm(Form):
    message = TextAreaField("Message")
