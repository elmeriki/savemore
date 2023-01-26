from import_export import resources
from stock.models import *

class StockResources(resources.ModelResource):
    class Meta:
        models = Stock
        # db_table = ''
        # managed = True
        # verbose_name = 'ModelName'
        # verbose_name_plural = 'ModelNames'


