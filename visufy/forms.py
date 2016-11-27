from django import forms

class SongForm(forms.Form):
    query = forms.CharField(label='', widget=forms.TextInput(attrs={'id' : 'query'}))
