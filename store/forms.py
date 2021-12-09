from django import forms

from .models import Office, Drop, Product, Order, Delivery, ProductVariant


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


class OfficeForm(forms.ModelForm):
    class Meta:
        model = Office
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
    sport = forms.CharField(required=False)
    name = forms.CharField(required=True)

    # initialize the form
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
         # create the variant_option
        #variant_option_name = 'option_%s_variant_%s' % (i, i)
        #self.fields[variant_option_name] = forms.CharField(required=False, label="Variant value")

    #def get_variant_fields(self):
        #for variant_option_name in self.fields:
            #if variant_option_name.startswith('option_'):
                #yield self[variant_option_name]

    # filtering user input data
    def clean(self):
        # for some reason self
        variants = set()
        i = 0
        field_name = 'variant_%s' % (i,)
        while self.cleaned_data.get(field_name):
           variant = self.cleaned_data[field_name]
           if variant in variants:
               self.add_error(field_name, 'Duplicate')
           else:
               variants.add(variant)
           i += 1
           field_name = 'variant_%s' % (i,)
        self.cleaned_data["variants"] = variants

    def save(self):
        product = self.instance
        product.name = self.cleaned_data['name']
        product.sortno = self.cleaned_data['sortno']
        product.save()

        #product.variant_set.all().delete()



class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'supplier', 'product', 'design', 'color', 'buyer', 'office', 'drop'
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
            'office': forms.Select(attrs={
                'class': 'form-control', 'id': 'office'
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
