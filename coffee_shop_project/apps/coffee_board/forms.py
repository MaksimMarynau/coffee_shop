from django import forms
from django.contrib.auth import get_user_model
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
        fields = ('name','email','body')
        widgets = {'body': forms.Textarea(attrs={'rows':10,
                                                   'cols':40,
                                                   'style':'resize:none;'}),
        }


class CommentFormAuthenticated(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {'body': forms.Textarea(attrs={'rows':10,
                                                   'cols':40,
                                                   'style':'resize:none;'}),
        }


class RegistrationForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        )


class UserUpdateForm(forms.ModelForm):

    username = forms.CharField()

    class Meta:
        model = get_user_model()
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
        )


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].label = False


class SellerForm(forms.ModelForm):
    class Meta:
        model = Seller
        fields = ('address',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].label = False


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
            'available'
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
    fields='__all__',
    max_num=4,
    extra=4,
)


class SearchForm(forms.Form):
    query = forms.CharField(label='')
