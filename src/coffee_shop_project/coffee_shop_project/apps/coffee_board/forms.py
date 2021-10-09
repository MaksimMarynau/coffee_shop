from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _

from .models import (
    Comment,
    Seller,
    Product,
    ProductImages,
)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {'body': forms.Textarea(attrs={'rows':10,
                                                   'cols':40,
                                                   'style':'resize:none;'}),
        }


class RegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        )

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
        )

class SellerForm(forms.ModelForm):
    class Meta:
        model = Seller
        fields = ('phone', 'address')


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = (
            'title',
            'price',
            'description',
            'country',
            'image',
            'tags',
        )
        labels = {
            "title": _("Product title"),
            "price": _("What price?"),
            "description": _("Explain your product"),
            "country": _("Country of production"),
            "image": _("Add main image"),
            "tags": _("Tags of your product"),
        }

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        if self.instance:
            # If the instance has no image, they haven't uploaded anything
            if self.instance.image is None:
                # Alter the field in the form
                self.fields['image'].disabled = True


AIFormSet = forms.inlineformset_factory(
    Product,
    ProductImages,
    fields='__all__'
)

class SearchForm(forms.Form):
    query = forms.CharField(label='')
