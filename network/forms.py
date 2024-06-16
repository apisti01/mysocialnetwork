from django import forms
from .models import Profile, Post, FriendRequest, Comment


class ProfileForm(forms.ModelForm):
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Profile
        fields = ['bio', 'location', 'birth_date', 'image']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']


class FriendRequestForm(forms.ModelForm):
    class Meta:
        model = FriendRequest
        fields = ['from_user', 'to_user']


class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 1, 'cols': 20}), label='add a comment:')

    class Meta:
        model = Comment
        fields = ['content']