
from django import forms
from .models import Category, Expense



class ExpenseSearchForm(forms.ModelForm):
    

    class Meta:
        model = Expense
        fields = ("name",)
    from_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    to_date = from_date
    food = forms.BooleanField()
    home = forms.BooleanField()
    clothes = forms.BooleanField()
    transport = forms.BooleanField()
    sort_by = forms.ChoiceField(choices=(('', ''), ("1", "category"), ("2", "date")))
    order = forms.ChoiceField(choices=(("1", "ascending"),("2", "descending")))



    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in ("name", "from_date", "to_date", "food", "clothes", "home", "transport", "sort_by", "order"):
            self.fields[field].required = False
        

    
 

        
