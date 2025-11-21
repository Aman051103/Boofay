from django import forms
from market_place.models import food, r_attribute

class GetFood(forms.ModelForm):

    parent_id=forms.IntegerField(widget=forms.NumberInput(attrs={'type': 'hidden', 'id': 'parent'}))

    name=forms.CharField(widget=forms.TextInput(attrs={'class': 'col-12 my-3', 'placeholder': 'for eg.- Cheese burger', 'style': 'border-radius: 4px; border: 1px solid grey'}))

    category=forms.CharField(widget=forms.TextInput(attrs={'class': 'col-12 my-3', 'placeholder': 'for eg.- Fast food', 'style': 'border-radius: 4px; border: 1px solid grey'}))

    sub_category=forms.CharField(widget=forms.TextInput(attrs={'class': 'col-12 my-3', 'placeholder': 'for eg.- Burgers', 'style': 'border-radius: 4px; border: 1px solid grey'}))

    description=forms.CharField(widget=forms.Textarea(attrs={'class': 'col-12 my-3', 'placeholder': 'describe the specialities/ ingredients of your item here...', 'rows': '5', 'style': 'border-radius: 6px; border: 1px solid grey'}))


    class Meta:
        model=food
        fields=('parent_id', 'name', 'category', 'sub_category', 'description', 'preparation_time_in_minutes', 'price', 'image')



class GetProfile(forms.ModelForm):

    restaurant_user_id=forms.IntegerField(widget=forms.NumberInput(attrs={'type': 'hidden', 'id': 'parent'}))

    # name=forms.CharField(widget=forms.TextInput(attrs={'class': 'col-12 my-3', 'placeholder': 'for eg.- Cheese burger', 'style': 'border-radius: 4px; border: 1px solid grey'}))

    # category=forms.CharField(widget=forms.TextInput(attrs={'class': 'col-12 my-3', 'placeholder': 'for eg.- Fast food', 'style': 'border-radius: 4px; border: 1px solid grey'}))

    # sub_category=forms.CharField(widget=forms.TextInput(attrs={'class': 'col-12 my-3', 'placeholder': 'for eg.- Burgers', 'style': 'border-radius: 4px; border: 1px solid grey'}))

    # description=forms.CharField(widget=forms.Textarea(attrs={'class': 'col-12 my-3', 'placeholder': 'describe the specialities/ ingredients of your item here...', 'rows': '5', 'style': 'border-radius: 6px; border: 1px solid grey'}))


    class Meta:
        model=r_attribute
        exclude=('restaurant_id', 'parent')