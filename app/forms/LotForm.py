from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Length, Regexp

class LotForm(FlaskForm):
    prime_location_name = StringField("Location Name", validators=[DataRequired(), Length(max=100)])
    price_per_hour = FloatField("Price", validators=[DataRequired(), NumberRange(min=0)])
    num_spots = IntegerField("Number Of Spots", validators=[DataRequired(), NumberRange(min=1)])
    address = StringField("Location Address", validators=[DataRequired(), Length(max=200)])
    pincode = StringField(
        "Pincode",
        validators=[
            DataRequired(),
            Length(min=6, max=6, message="Pincode must be exactly 6 digits"),
            Regexp(r'^[0-9]{6}$', message="Pincode must contain only digits"),
        ]
    )
    submit = SubmitField("Submit")
