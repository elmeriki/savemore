import re
from stock.models import *
from django import forms
# import attr


class StockForm(forms.Form):
    class meta:
        model=Stock
        fields ='__all__'