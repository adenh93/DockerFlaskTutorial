from flask_wtf import FlaskForm as Form
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length

class CommentForm(Form):
  name = StringField(
    'Name',
    validators=[DataRequired(), Length(max=255)]
  )
  title = StringField(
    'Title',
    validators=[DataRequired(), Length(max=255)]
  )
  body = TextAreaField(
    'Comment',
    validators=[DataRequired()]
  )