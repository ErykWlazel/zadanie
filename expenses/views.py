
from django.views.generic.list import ListView

from .forms import ExpenseSearchForm
from .models import Expense, Category
from django.db.models import Sum
from .reports import summary_per_category, total_amount_spent, summary_per_year_month




class ExpenseListView(ListView):
    model = Expense
    paginate_by = 20



    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = object_list if object_list is not None else self.object_list
        
        form = ExpenseSearchForm(self.request.GET)
        if form.is_valid():
            name = form.cleaned_data.get("name", "").strip()
            from_date = form.cleaned_data.get("from_date")
            to_date = form.cleaned_data.get("to_date")
            food = form.cleaned_data.get("food")
            clothes = form.cleaned_data.get("clothes")
            home = form.cleaned_data.get("home")
            transport = form.cleaned_data.get("transport")
            user_choices = []
            sort_by = form.cleaned_data.get("sort_by")
            order = form.cleaned_data.get("order")
        
            
            for id, sub_cat in ((1,food), (2,home), (3,clothes), (4,transport)):
                if sub_cat is True:
                    user_choices.append(id)

            
            if name:
                queryset = queryset.filter(name__icontains=name)
            if from_date:
                queryset = queryset.filter(date__gte=from_date)
            if to_date:
                queryset = queryset.filter(date__lte=to_date)
            if food or clothes or home or transport:
                queryset = queryset.filter(category__in=user_choices)
            if sort_by == '1':
                if order == '1':
                    queryset = queryset.order_by("category")
                elif order == '2':
                    queryset = queryset.order_by("-category")
            if sort_by == '2':
                if order == '1':
                    queryset = queryset.order_by("date")
                elif order == '2':
                    queryset = queryset.order_by("-date")
                
        return super().get_context_data(
            
            form=form,
            object_list=queryset,
            summary_per_category=summary_per_category(queryset),
            total_amount_spent=total_amount_spent(Expense.objects),
            summary_per_year_month=summary_per_year_month(Expense.objects),
            **kwargs
        )


class CategoryListView(ListView):
    model = Category
    
    paginate_by = 5


