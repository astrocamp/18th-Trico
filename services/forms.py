from django import forms
from .models import Service
from django_ckeditor_5.widgets import CKEditor5Widget


class ServiceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)
          self.fields["description"].required = False
    class Meta:
        model = Service
        fields = [
            "title",
            "description",
            "photo",
            "category",
            "standard_title",
            "standard_description",
            "standard_price",
            "standard_delivery_time",
            "premium_title",
            "premium_description",
            "premium_price",
            "premium_delivery_time",
            "tags",
        ]
        widgets = {
            "category": forms.CheckboxSelectMultiple(),
            "description": CKEditor5Widget(
                  attrs={"class": "django_ckeditor_5"}, config_name="extends"
                  )
        }
        # description = CKEditor5Widget(attrs={"class": "django_ckeditor_5"}, config_name="extends")

    def __init__(self, *args, **kwargs):
        self.premium_enabled = kwargs.pop("premium_enabled", False)
        super().__init__(*args, **kwargs)

        if self.premium_enabled:
            self.fields["premium_title"].required = True
            self.fields["premium_description"].required = True
            self.fields["premium_price"].required = True
            self.fields["premium_delivery_time"].required = True
        else:
            self.fields["premium_title"].required = False
            self.fields["premium_description"].required = False
            self.fields["premium_price"].required = False
            self.fields["premium_delivery_time"].required = False

    def clean(self):
        cleaned_data = super().clean()

        premium_title = cleaned_data.get("premium_title")
        premium_description = cleaned_data.get("premium_description")
        premium_price = cleaned_data.get("premium_price")
        premium_delivery_time = cleaned_data.get("premium_delivery_time")

        if premium_title or premium_description or premium_price or premium_delivery_time:
            if not premium_title:
                self.add_error("premium_title", "請填寫專業方案名稱")
            if not premium_description:
                self.add_error("premium_description", "請填寫專業方案描述")
            if not premium_price:
                self.add_error("premium_price", "請填寫專業方案價格")
            if not premium_delivery_time:
                self.add_error("premium_delivery_time", "請填寫專業方案交付時間")

        return cleaned_data
