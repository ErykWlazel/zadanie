from collections import OrderedDict
import datetime

from django.db.models import Sum, Value
from django.db.models.functions import Coalesce


def summary_per_category(queryset):
    return OrderedDict(
        sorted(
            queryset.annotate(category_name=Coalesce("category__name", Value("-")))
            .order_by()
            .values("category_name")
            .annotate(s=Sum("amount"))
            .values_list("category_name", "s")
            
        )
    )

def summary_per_year_month(objects):
    #objects.filter(date='2021-02-03').aggregate(Sum('amount'))
    
    unique_date = set()
    for row in objects.values_list('date'):
        unique_date.add(row[0].strftime("%Y-%m"))

    dict_of_unique_date_amount_sum = OrderedDict()
    for udate in unique_date:

        unique_date_amount_sum = objects.filter(date__year=udate[0:4], date__month=udate[5:]).values_list("date", "amount").aggregate(Sum('amount'))
        
        dict_of_unique_date_amount_sum[udate] = unique_date_amount_sum['amount__sum']
        
        
    return dict_of_unique_date_amount_sum
        
        
    


def total_amount_spent(objects):
    return (
        objects.aggregate(Sum('amount'))
    )