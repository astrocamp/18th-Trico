from django import forms


class SearchForm(forms.Form):
    keyword = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "請輸入關鍵字..."}),
    )
