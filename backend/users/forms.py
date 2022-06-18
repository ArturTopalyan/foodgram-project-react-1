from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.forms import ModelForm


User = get_user_model()


class ss(ModelForm):
    model
class CreateUserForm(UserCreationForm):
    fields
