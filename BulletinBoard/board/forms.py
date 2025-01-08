from django import forms

from .models import Ad


class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['title', 'content', 'category']
        widgets = {
            'content': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
        }

        def clean_category(self):
            category = self.cleaned_data.get('category')
            if not category:
                raise forms.ValidationError('Выберите хотя бы одну категорию.')
            return category
