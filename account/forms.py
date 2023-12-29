from django import forms

from account.models import CustomUser


class TbmUserSignupForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = (
            "first_name",
            "last_name",
            "password",
            "email",
        )

    def __init__(self, *args, **kwargs):
        signup_required_fields = ["first_name", "last_name", "email", "password"]
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if field_name in signup_required_fields:
                field.required = True
            else:
                field.required = False

    