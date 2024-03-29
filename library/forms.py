from django import forms

from .models import BookReview, Profile, User, BookInstance


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


class DateInput(forms.DateInput):
    input_type = 'date'


class UserBookCreateForm(forms.ModelForm):
    class Meta:
        model = BookInstance
        fields = ('book', 'reader', 'due_back',)
        widgets = {
            'reader': forms.HiddenInput(),
            'due_back': DateInput(),
        }


