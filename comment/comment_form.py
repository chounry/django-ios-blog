from django import forms


class Comment_form(forms.Form):
    obj_id = forms.IntegerField(widget=forms.HiddenInput)
    content_type = forms.CharField(widget=forms.HiddenInput)
    comment = forms.CharField(widget=forms.Textarea, label='')