from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from .models import Mod

class ModForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fieldname in ['mod_link']:
            self.fields[fieldname].help_text = None

    class Meta:
        model = Mod
        fields = ['mod_link']
        labels = {
            'mod_link': 'URL da Oficina Steam',
        }
        widgets = {
            'mod_link': forms.URLInput(attrs={
                'placeholder': 'Cole o link completo do mod aqui',
                'class': 'form-control' 
            }),
        }

    def clean_mod_link(self):
        urls = self.cleaned_data.get('mod_link')
        if urls:
            for url in urls.split(';'):
                url = url.strip()
                if 'steamcommunity.com/' not in url or 'filedetails/' not in url:
                    raise forms.ValidationError(f"URL inválida: {url}")
        return urls

class ModManualForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fieldname in ['mod_id', 'workshop_id', 'name', 'mod_link']:
            self.fields[fieldname].help_text = None
    
    def clean_mod_link(self):
        url = self.cleaned_data.get('mod_link')

        if url and 'steamcommunity.com/sharedfiles/filedetails/' not in url:
            raise forms.ValidationError("URL inválida. Por favor, insira um link da Oficina Steam.")
            
        return url
    
    class Meta:
        model = Mod
        fields = ['mod_id', 'workshop_id', 'name', 'mod_link']
        labels = {
            'mod_id': 'ID do Mod (Ex: Brita_2)',
            'workshop_id': 'ID do Workshop (Ex: 2460154811)',
            'name': 'Nome do Mod',
            'mod_link': 'URL da Oficina Steam (Opcional)',
        }
        widgets = {
            'mod_id': forms.TextInput(attrs={
                'placeholder': 'O nome interno do mod',
                'class': 'form-control'
            }),
            'workshop_id': forms.TextInput(attrs={
                'placeholder': 'O número encontrado na URL',
                'class': 'form-control'
            }),
            'name': forms.TextInput(attrs={
                'placeholder': 'O nome de exibição do mod',
                'class': 'form-control'
            }),
            'mod_link': forms.URLInput(attrs={
                'placeholder': 'Opcional: o link completo do mod',
                'class': 'form-control'
            }),
        }