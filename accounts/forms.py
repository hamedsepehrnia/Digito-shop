# forms.py
from django import forms
from .models import MyUser, Address


class CompleteProfileForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['fullname', 'age', 'province', 'city', 'gender']
        widgets = {
            'fullname': forms.TextInput(attrs={'class' : "rounded-2xl rounded-tr-sm text-sm text-zinc-600 w-full bg-[#f0f0f0] px-5 py-3.5 placeholder:text-zinc-400 placeholder:text-xs focus:outline-1 focus:outline-zinc-300", 'placeholder' : "نام و نام خانوادگی", 'type':"text"}),
            'age': forms.TextInput(attrs={ 'class' : "rounded-2xl rounded-tr-sm text-sm text-zinc-600 w-full bg-[#f0f0f0] px-5 py-3.5 placeholder:text-zinc-400 placeholder:text-xs focus:outline-1 focus:outline-zinc-300", 'placeholder' : "سن" ,'type' : "text"}),
            'province': forms.TextInput(attrs={ 'class' : "appearance-none rounded-2xl rounded-tr-sm text-sm text-zinc-600 w-full bg-[#f0f0f0] px-5 py-3.5 placeholder:text-zinc-400 placeholder:text-xs focus:outline-1 focus:outline-zinc-300"}),
            'city': forms.TextInput(attrs={ 'class' : "appearance-none rounded-2xl rounded-tr-sm text-sm text-zinc-600 w-full bg-[#f0f0f0] px-5 py-3.5 placeholder:text-zinc-400 placeholder:text-xs focus:outline-1 focus:outline-zinc-300"}),
            'gender': forms.Select(attrs={ 'class' : "appearance-none rounded-2xl rounded-tr-sm text-sm text-zinc-600 w-full bg-[#f0f0f0] px-5 py-3.5 placeholder:text-zinc-400 placeholder:text-xs focus:outline-1 focus:outline-zinc-300"}),
        }
class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['subject', 'first_name', 'last_name', 'address_details', 'phone_number', 'province', 'city', 'postal_code', 'additional_info']
        widgets = {
            'subject': forms.TextInput(attrs={
                'class': 'rounded-2xl rounded-tr-sm text-sm text-zinc-600 w-full bg-[#f0f0f0] px-5 py-3.5 placeholder:text-zinc-400 placeholder:text-xs focus:outline-1 focus:outline-zinc-300',
                'placeholder': 'عنوان آدرس (مثلا: منزل، محل کار)',
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'rounded-2xl rounded-tr-sm text-sm text-zinc-600 w-full bg-[#f0f0f0] px-5 py-3.5 placeholder:text-zinc-400 placeholder:text-xs focus:outline-1 focus:outline-zinc-300',
                'placeholder': 'نام',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'rounded-2xl rounded-tr-sm text-sm text-zinc-600 w-full bg-[#f0f0f0] px-5 py-3.5 placeholder:text-zinc-400 placeholder:text-xs focus:outline-1 focus:outline-zinc-300',
                'placeholder': 'نام خانوادگی',
            }),
            'province': forms.TextInput(attrs={
                'class': 'rounded-2xl rounded-tr-sm text-sm text-zinc-600 w-full bg-[#f0f0f0] px-5 py-3.5 placeholder:text-zinc-400 placeholder:text-xs focus:outline-1 focus:outline-zinc-300',
                'placeholder': 'استان',
            }),
            'city': forms.TextInput(attrs={
                'class': 'rounded-2xl rounded-tr-sm text-sm text-zinc-600 w-full bg-[#f0f0f0] px-5 py-3.5 placeholder:text-zinc-400 placeholder:text-xs focus:outline-1 focus:outline-zinc-300',
                'placeholder': 'شهر',
            }),
            'address_details': forms.TextInput(attrs={
                'class': 'rounded-2xl rounded-tr-sm text-sm text-zinc-600 w-full bg-[#f0f0f0] px-5 py-3.5 placeholder:text-zinc-400 placeholder:text-xs focus:outline-1 focus:outline-zinc-300',
                'placeholder': 'خیابان و کوچه و شماره پلاک و واحد',
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'rounded-2xl rounded-tr-sm text-sm text-zinc-600 w-full bg-[#f0f0f0] px-5 py-3.5 placeholder:text-zinc-400 placeholder:text-xs focus:outline-1 focus:outline-zinc-300',
                'placeholder': 'تلفن همراه',
            }),
            'postal_code': forms.TextInput(attrs={
                'class': 'rounded-2xl rounded-tr-sm text-sm text-zinc-600 w-full bg-[#f0f0f0] px-5 py-3.5 placeholder:text-zinc-400 placeholder:text-xs focus:outline-1 focus:outline-zinc-300',
                'placeholder': 'کد پستی محل تحویل',
            }),
            'additional_info': forms.Textarea(attrs={
                'class': 'rounded-2xl rounded-tr-sm text-sm text-zinc-600 w-full bg-[#f0f0f0] px-5 py-3.5 placeholder:text-zinc-400 placeholder:text-xs focus:outline-1 focus:outline-zinc-300',
                'placeholder': 'نکات مهم درباره تحویل محصول',
                'rows': 7,
            }),
        }