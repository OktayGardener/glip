from django import forms

class SongForm(forms.Form):
    song_title = forms.CharField(widget=forms.TextInput(attrs={'id' : 'song_title'}))
