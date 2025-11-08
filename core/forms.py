from django import forms
from .models import ContactMessage


class ContactMessageForm(forms.ModelForm):
    """فرم تماس با ما"""
    class Meta:
        model = ContactMessage
        fields = ['name', 'phone', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'rounded-2xl rounded-tr-sm text-sm text-zinc-600 w-full bg-[#f0f0f0] px-5 py-3.5 placeholder:text-zinc-400 placeholder:text-xs focus:outline-1 focus:outline-zinc-300',
                'placeholder': 'نام و نام خانوادگی شما...'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'rounded-2xl rounded-tr-sm text-sm text-zinc-600 w-full bg-[#f0f0f0] px-5 py-3.5 placeholder:text-zinc-400 placeholder:text-xs focus:outline-1 focus:outline-zinc-300',
                'placeholder': 'شماره تلفن شما...'
            }),
            'message': forms.Textarea(attrs={
                'class': 'rounded-2xl rounded-tr-sm text-sm text-zinc-600 w-full bg-[#f0f0f0] px-5 py-3.5 placeholder:text-zinc-400 placeholder:text-xs focus:outline-1 focus:outline-zinc-300 resize-none',
                'rows': 5,
                'placeholder': 'متن پیام شما...'
            }),
        }

