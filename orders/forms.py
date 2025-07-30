from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['design_type', 'size', 'description', 'field_upload']
        labels = {
            'design_type': 'Choose one Design type',
            'size': 'Choose the size of your Design',
            'description': 'Give us more details about your custom design',
            'field_upload': 'You can upload some images (Optional)',
        }

        widgets = {
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Write here'
            }),

            'design_type': forms.Select(attrs={'class': 'form-select'}),
            'size': forms.Select(attrs={'class': 'form-select'}),

        }
