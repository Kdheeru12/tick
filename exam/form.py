from django import forms
from .models import Profile,Challenge,Post
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "photo",
            "Mobile",
            "gender",
            "date",
            "address",
            "state",
            "city",
            "pincode",
            "age",
            "intrests"
        ]
        widgets = {
            "Mobile": forms.NumberInput(attrs={'class':'form-control'}),
            "gender": forms.TextInput(attrs={'class':'form-control'}),
            "date": forms.DateInput(attrs={'class':'form-control'}),
            "address": forms.Textarea(attrs={'class':'form-control'}),
            "state": forms.TextInput(attrs={'class':'form-control'}),
            "city": forms.TextInput(attrs={'class':'form-control'}),
            "pincode": forms.NumberInput(attrs={'class':'form-control'}),
            "age": forms.NumberInput(attrs={'class':'form-control'}),
            "intrests": forms.TextInput(attrs={'class':'form-control'}),
        }
class ChallengeForm(forms.ModelForm):
    class Meta:
        model = Challenge
        fields = [
            "title",
            "about",
            "image",
            "start_date",
            "end_date",
            "reward",
        ]
        widgets = {
            "title": forms.TextInput(attrs={'class':'form-control'}),
            "start_date": forms.DateInput(attrs={'class':'form-control'}),
            "about": forms.Textarea(attrs={'class':'form-control'}),
            "reward": forms.TextInput(attrs={'class':'form-control'}),
            "end_date": forms.DateInput(attrs={'class':'form-control'}),
        }
        
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "title",
            "challenge",
            "video",

        ]
        widgets = {
            "title": forms.TextInput(attrs={'class':'form-control'}),
            "video": forms.FileInput(attrs={'class':'form-control'}),
            "challenge": forms.Select(attrs={'class':'form-control'}),

        }