from django import forms
from pagedown.widgets import PagedownWidget
from .models import Post


class post_form(forms.ModelForm):
    caption = forms.CharField(widget=PagedownWidget(show_preview=False))
    class Meta:
        model = Post
        fields = [
            'post_title',
            'caption',
            'post_img',
            'tag'
    ]