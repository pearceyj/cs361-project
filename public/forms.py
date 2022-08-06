from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length
class SettingsForm(FlaskForm):
    location = StringField('Location',validators=[DataRequired(),Length(min=2, max=20)])
    remember = BooleanField('Remember Location')
    submit = SubmitField('Add Location')
