from django import forms

class SongForm(forms.Form):
    song_title = forms.CharField(label='', widget=forms.TextInput(attrs={'id' : 'song_title'}))
