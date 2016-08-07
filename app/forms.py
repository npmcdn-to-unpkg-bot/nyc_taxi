from flask.ext.wtf import Form
from wtforms import SelectField
from wtforms.validators import DataRequired


class QueryForm(Form):
    neighborhood = SelectField('Neighborhood', choices=[('asd', 'asd')])
    blocks = SelectField('Block', choices=[('', '')])
