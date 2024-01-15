from django import forms

from .models import BookReview, Profile, User


class BookReviewForm(forms.ModelForm):
    class Meta:
        model = BookReview
        fields = ('content', 'book', 'reviewer')
        widgets = {  # paslepiam laukus, kad būtų nevaizduojami formoje
            'book': forms.HiddenInput(),
            'reviewer': forms.HiddenInput()
        }


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email',)


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields =('picture',)


