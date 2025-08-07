from django import forms
from .models import Order, Comment


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['design_type', 'size', 'description', 'file_upload']
        labels = {
            'design_type': 'Choose one Design type',
            'size': 'Choose the size of your Design',
            'description': 'Give us more details about your custom design',
            'file_upload': 'You can upload an image (Optional)',
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


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['public_name', 'content', 'image', ]
        labels = {
            'public_name': 'Write your public name',
            'content': 'Write your comment',
            'image': 'upload an image(optional)',
        }

        widgets = {'public_name': forms.TextInput(
            attrs={'class': 'form-control', }),
                   'content': forms.Textarea(
                       attrs={
                           'class': 'form-control',
                           'rows': 3,
                           'placeholder': 'Write here'}),
                   'image': forms.ClearableFileInput(
                       attrs={
                           'class': 'form-control-file', }),
        }
