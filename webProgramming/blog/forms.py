from django import forms
from .models import Post, News, Product, Purchase, Event, Reply, User, shuttleHours, Notes


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('topic', 'text', 'type',)


class ReplyForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea, label='')

    class Meta:
        model = Reply
        fields = ('text',)


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ('topic', 'content', 'image')


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'size', 'type', 'gender', 'stock', 'price', 'image')


class DateInput(forms.DateInput):
    input_type = 'date'


class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ('name', 'content', 'place', 'organizator', 'image1')


class PurchaseForm(forms.ModelForm):
    amount = forms.CharField(widget=forms.NumberInput, label='')

    class Meta:
        model = Purchase
        fields = ('amount',)


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'firstname', 'lastname', 'gender', 'program')


class ShuttleForm(forms.ModelForm):
    class Meta:
        model = shuttleHours
        fields = ('name', 'quota', 'hour')


class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ('lesson', 'topic', 'note')
