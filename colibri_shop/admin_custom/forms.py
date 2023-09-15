from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from users.models import User

from orders.models import Order
from products.models import Product, ProductCategory, ProductBrands, Basket


class AdminUserUpdateForm(UserChangeForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control py-4 font-weight-light small",
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control py-4 font-weight-light small",
    }))
    image = forms.ImageField(widget=forms.FileInput(attrs={
        "class": "custom-file-input font-weight-light small"}),
        required=False)
    username = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control py-4 font-weight-light small"
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        "class": "form-control py-4 font-weight-light small"
    }))
    is_verified_email = forms.CheckboxInput(attrs={
        "class": "form-check form-switch"
    })
    is_staff = forms.CheckboxInput(attrs={
        "style": "position: absolute; top: 10px; left: 5px;"
    })

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'image', 'username', 'email', 'is_verified_email', 'is_staff')


# class AdminUserCreateForm(UserCreationForm):
#     pass


class AdminProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = (
            'name', 'description', 'price',
            'quantity', 'size', 'sex',
            'category', 'brand', 'image'
        )
        widgets = {
            'name': forms.TextInput(attrs={
                "class": "form-control py-4 font-weight-light small",
            }),
            'description': forms.TextInput(attrs={
                "class": "form-control py-4 font-weight-light small",
            }),
            'price': forms.NumberInput(attrs={
                "class": "form-control py-4 font-weight-light small",
            }),
            'quantity': forms.NumberInput(attrs={
                "class": "form-control py-4 font-weight-light small",
            }),
            'size': forms.Select(attrs={
                "class": "form-control py-4 font-weight-light small",
            }),
            'sex': forms.Select(attrs={
                "class": "form-control py-4 font-weight-light small",
            }),
            'category': forms.Select(attrs={
                "class": "form-control py-4 font-weight-light small",
            }),
            'brand': forms.Select(attrs={
                "class": "form-control py-4 font-weight-light small",
            }),
            'image': forms.FileInput(attrs={
                "class": "form-control py-4 font-weight-light small",
            }),
        }


class AdminCategoryForm(forms.Form):
    class Meta:
        model = ProductCategory
        fields = (
            'name', 'description', 'sex'
        )
        widgets = {
            'name': forms.TextInput(attrs={
                "class": "form-control py-4 font-weight-light small",
            }),
            'description': forms.TextInput(attrs={
                "class": "form-control py-4 font-weight-light small",
            }),
            'sex': forms.Select(attrs={
                "class": "form-select py-3 font-weight-light small",
            })
        }


class AdminBrandForm(forms.Form):
    class Meta:
        model = ProductBrands
        fields = (
            'name', 'description', 'image'
        )
        widgets = {
            'name': forms.TextInput(attrs={
                "class": "form-control py-4 font-weight-light small",
            }),
            'description': forms.TextInput(attrs={
                "class": "form-control py-4 font-weight-light small",
            }),
            'image': forms.ImageField(attrs={
                "class": "form-control py-4 font-weight-light small",
            })
        }


class AdminBasketUpdateForm(forms.Form):
    class Meta:
        model = Basket
        fields = (
            'user', 'product', 'quantity'
        )
        widgets = {
            'user': forms.Select(attrs={
                "class": "form-select py-3 font-weight-light small",
            }),
            'description': forms.TextInput(attrs={
                "class": "form-control py-4 font-weight-light small",
            }),
            'quantity': forms.TextInput(attrs={
                "class": "form-control py-4 font-weight-light small",
            }),
        }


class AdminOrderUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            'first_name', 'last_name', 'email',
            'address', 'basket_history',
            'status', 'initiator'
        )
        widgets = {
            'first_name': forms.TextInput(attrs={
                "class": "form-control py-4 font-weight-light small",
            }),
            'last_name': forms.TextInput(attrs={
                "class": "form-control py-4 font-weight-light small",
            }),
            'email': forms.EmailInput(attrs={
                "class": "form-control py-4 font-weight-light small",
            }),
            'address': forms.TextInput(attrs={
                "class": "form-control py-4 font-weight-light small",
            }),
            'basket_history': forms.Textarea(attrs={
                "class": "form-control py-4 font-weight-light small",
                "readonly": True,
            }),
            'status': forms.Select(attrs={
                "class": "form-select py-3 font-weight-light small",
            }),
            'initiator': forms.Select(attrs={
                "class": "form-select py-3 font-weight-light small",
            }),
        }
