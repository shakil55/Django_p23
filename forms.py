from django import forms
from .models import Profile, BlogPost
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone_no', 'bio', 'facebook', 'instagram', 'linkedin', 'image', )
     
        
class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ('title', 'slug', 'content', 'image')
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Title of the Blog'}),
            'slug': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Copy the title with no space and a hyphen in between'}),
            'content': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Content of the Blog'}),
        }


# class UserRegistrationForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ('username',  'email')
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# class UserRegistrationForm1(UserCreationForm):
#     email = forms.EmailField(max_length=200, help_text='*Required')
     
#     class Meta:
#         model = User
#         fields = ('username', 'email')

#     # def try_save(self):
#     #     # Custom logic to save the user or perform additional actions
#     #     # You can access form fields using self.cleaned_data['field_name']
#     #     username = self.cleaned_data('username', 'email')
      
    
#     #     # Perform your custom logic here

#     #     # Save the user
#     #     user = super().save(commit=False)
#     #     user.email = email
#     #     user.save()

#     #     return user
#         def try_save(self, request):
#         # Custom logic to save the user or perform additional actions
#         # You can access form fields using self.cleaned_data['field_name']
#          user= self.cleaned_data['username']
#          email = self.cleaned_data['email']

#         # Perform your custom logic here

#         # Save the user
#          user = super().save(commit=False)
#          user.email = email
#          user.save()

#          return user 
#     class Media:
#         css = {
#             'all': ('https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css',),
#         }


#21.12.23
class UserRegistrationForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))        

    def save(self,username):
        # Custom logic to save the user data
        cleaned_data = self.cleaned_data
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        # Example: Create a new user
        user = User.objects.create_user(username, email, password)
        user.save()

# class UserRegistrationForm(UserCreationForm):
#     email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2']