from wtforms import Form, StringField, TextAreaField


class PostForm(Form):
    title = StringField('title')
    body = TextAreaField('body')
