from django import forms

from .models import Season, Drop, Product, Order, Delivery, ProductVariant


class SupplierForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'name',
        'data-val': 'true',
        'data-val-required': 'Please enter name',
    }))
    address = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'address',
        'data-val': 'true',
        'data-val-required': 'Please enter address',
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'id': 'email',
        'data-val': 'true',
        'data-val-required': 'Please enter email',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'password',
        'data-val': 'true',
        'data-val-required': 'Please enter password',
    }))
    retype_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'retype_password',
        'data-val': 'true',
        'data-val-required': 'Please enter retype_password',
    }))


class BuyerForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'name',
        'data-val': 'true',
        'data-val-required': 'Please enter name',
    }))
    address = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'address',
        'data-val': 'true',
        'data-val-required': 'Please enter address',
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'id': 'email',
        'data-val': 'true',
        'data-val-required': 'Please enter email',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'password',
        'data-val': 'true',
        'data-val-required': 'Please enter password',
    }))
    retype_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'retype_password',
        'data-val': 'true',
        'data-val-required': 'Please enter retype_password',
    }))


class SeasonForm(forms.ModelForm):
    class Meta:
        model = Season
        fields = ['name', 'description']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'name'
            }),
            'description': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'description'
            })
        }


class DropForm(forms.ModelForm):
    class Meta:
        model = Drop
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'name'
            })
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
    name = forms.CharField(required=False)
    # dynamic variants
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        variants = ProductVariant.objects.filter(
            product=self.instance
        )
        for i in range(len(variants) + 1):
            field_name = 'variant_%s' % (i,)
            self.fields[field_name] = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control',}))
            try:
                self.initial[field_name] = variants[i].variant

            except IndexError:
                self.initial[field_name] = ""
        # create an extra blank field
        #field_name = 'variant_%s' % (i + 1,)
        #self.fields[field_name] = forms.CharField(required=False)

    def clean(self):
        variants = set()
        i = 0
        field_name = 'variant_%s' % (i,)
        while self.cleaned_data.get(field_name):
           variant = self.cleaned_data[field_name]
           print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
           print(variant)
           if variant in variants:
               self.add_error(field_name, 'Duplicate')
           else:
               variants.add(variant)
           i += 1
           field_name = 'variant_%s' % (i,)
        self.cleaned_data["variants"] = variants
    def get_variant_fields(self):
        for field_name in self.fields:
            if field_name.startswith('variant_'):
                yield self[field_name]
    def save(self):
        product = self.instance
        product.name = self.cleaned_data['name']
        product.save()
        #test
        #product.variant_set.all().delete()
        for variant in self.cleaned_data["variants"]:
           print("***********************************")
           print(variant)
           ProductVariant.objects.create(
               product=product,
               variant=variant,
           )


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'supplier', 'product', 'design', 'color', 'buyer', 'season', 'drop'
        ]

        widgets = {
            'supplier': forms.Select(attrs={
                'class': 'form-control', 'id': 'supplier'
            }),
            'product': forms.Select(attrs={
                'class': 'form-control', 'id': 'product'
            }),
            'design': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'design'
            }),
            'color': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'color'
            }),
            'buyer': forms.Select(attrs={
                'class': 'form-control', 'id': 'buyer'
            }),
            'season': forms.Select(attrs={
                'class': 'form-control', 'id': 'season'
            }),
            'drop': forms.Select(attrs={
                'class': 'form-control', 'id': 'drop'
            }),
        }


class DeliveryForm(forms.ModelForm):
    class Meta:
        model = Delivery
        fields = '__all__'

        widgets = {
            'order': forms.Select(attrs={
                'class': 'form-control', 'id': 'order'
            }),
            'courier_name': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'courier_name'
            }),
        }
