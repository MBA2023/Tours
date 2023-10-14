from django import forms


class BookForm(forms.Form):
    fio = forms.CharField()
    phone = forms.CharField()
    start_time = forms.DateTimeField()
