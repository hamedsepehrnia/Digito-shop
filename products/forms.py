from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'recommendation', 'bought_by_author']
        widgets = {
            'content': forms.Textarea(attrs={
                'placeholder': 'متن دیدگاه',
                'class': 'rounded-2xl rounded-tr-sm text-sm text-zinc-600 w-full bg-white border border-zinc-200 px-5 py-3.5 placeholder:text-zinc-400 placeholder:text-xs focus:outline-1 focus:outline-zinc-300',
                'rows': 7,
                'cols': 30,
            }),
            'recommendation': forms.CheckboxInput(attrs={
                'class': 'hidden peer',
            }),
            'bought_by_author': forms.CheckboxInput(attrs={
                'class': 'hidden peer',
            }),
        }