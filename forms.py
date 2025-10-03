from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, SelectField, TextAreaField, DateField
from wtforms.validators import DataRequired, NumberRange, Optional, Length

class ProductForm(FlaskForm):
    name = StringField("Prdouct Name", validators=[DataRequired(), Length(min=2, max=100)])
    barcode = StringField("Barcode", validators=[Optional(), Length(max=50)])
    price = FloatField("Price", validators=[DataRequired(), NumberRange(min=0)])
    stock = IntegerField("Stock", validators=[DataRequired(), NumberRange(min=0)])
    min_stock = IntegerField("Minimum Stock", validators=[DataRequired(), NumberRange(min=0)])
    category_id = SelectField('Category', coerce=int, validators=[DataRequired()])

class CategoryForm(FlaskForm):
    name = StringField("Category Name", validators=[DataRequired(), Length(min=2, max=50)])
    description = TextAreaField("Description", validators=[Optional(), Length(max=200)])

class StockMovementForm(FlaskForm):
    product_id = SelectField("Product", coerce=int, validators=[DataRequired()])
    type = SelectField('Process Type', 
                       choices=[('inflow', 'Inflow'), ('outflow', 'Outflow')],
                       validators=[DataRequired()])
    amount = IntegerField('Amount', validators=[DataRequired(), NumberRange(min=1)])
    description = TextAreaField('Description', validators=[Optional(), Length(max=200)])

class ReportForm(FlaskForm):
    starting_date = DateField('Starting Date', validators=[DataRequired()])
    ending_date = DateField('Ending Date', validators=[DataRequired()])
    category_id = SelectField('Category (Optional)', validators=[Optional()])


    