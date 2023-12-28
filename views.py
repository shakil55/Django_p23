from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth  import authenticate,  login, logout,get_user_model
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm, BlogPostForm,UserRegistrationForm
from django.views.generic import UpdateView
from django.contrib import messages

from django.contrib.sites.shortcuts import get_current_site  
# from django.utils.encoding import force_bytes, force_text  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from django.contrib.auth.models import User  
from django.core.mail import EmailMessage  
from .forms import *
# from django.utils.encoding import force_bytes, force_str


def blogs(request):
    posts = BlogPost.objects.all()
    posts = BlogPost.objects.filter().order_by('-dateTime')
    posts = BlogPost.objects.select_related('category').order_by('-dateTime')
    categories = Category.objects.all()
    return render(request, "blog.html", {'posts': posts, 'categories': categories})

def blogs_comments(request, slug):
    post = BlogPost.objects.filter(slug=slug).first()
    comments = Comment.objects.filter(blog=post, approved=True)  # Only fetch approved comments
    if request.method == "POST":
        user = request.user
        content = request.POST.get('content', '')
        blog_id = request.POST.get('blog_id', '')
        comment = Comment(user=user, content=content, blog=post)
        comment.save()  # Comments are saved as unapproved by default
    return render(request, "blog_comments.html", {'post': post, 'comments': comments})


def Delete_Blog_Post(request, slug):
    posts = BlogPost.objects.get(slug=slug)
    if request.method == "POST":
        posts.delete()
        return redirect('/')
    return render(request, 'delete_blog_post.html', {'posts':posts})

def search(request):
    if request.method == "POST":
        searched = request.POST.get('searched', '')
        blogs = BlogPost.objects.filter(title__icontains=searched)
        return render(request, "search.html", {'searched': searched, 'blogs': blogs})
    else:
        return render(request, "search.html")
        


@login_required(login_url = '/login')
def add_blogs(request):
    if request.method=="POST":
        form = BlogPostForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            blogpost = form.save(commit=False)
            blogpost.author = request.user
            blogpost.save()
            obj = form.instance
            alert = True
            return render(request, "add_blogs.html",{'obj':obj, 'alert':alert})
    else:
        form=BlogPostForm()
    return render(request, "add_blogs.html", {'form':form})

class UpdatePostView(UpdateView):
    model = BlogPost
    template_name = 'edit_blog_post.html'
    fields = ['title', 'slug', 'content', 'image']


def user_profile(request, myid):
    post = BlogPost.objects.filter(id=myid)
    return render(request, "user_profile.html", {'post':post})

def Profile(request):
    return render(request, "profile.html")

def edit_profile(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile(user=request.user)
    if request.method=="POST":
        form = ProfileForm(data=request.POST, files=request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            alert = True
            return render(request, "edit_profile.html", {'alert':alert})
    else:
        form=ProfileForm(instance=profile)
    return render(request, "edit_profile.html", {'form':form})


# def Register(request):
#     if request.method == "POST":
#         form = UserRegistrationForm1(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password1')  # You may want to change this depending on your registration form
#             user = authenticate(username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 messages.success(request, "Registration successful")
#                 return redirect("/")
#         else:
#             messages.error(request, "Registration failed. Please check the form.")
#     else:
#         form = UserRegistrationForm1()

#     return render(request, "register.html", {'form': form})

def Login(request):
    if request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("/")
        else:
            messages.error(request, "Invalid Credentials")
        return render(request, 'blog.html')   
    return render(request, "login.html")

def Logout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('/login')


# from .models import Category , BlogPost
# def categories(request, category_id=None):
#     categories = Category.objects.all()
#     category = get_object_or_404(Category, pk=category_id)
#     blog_posts = BlogPost.objects.filter(category=category)
#     return render(request, 'categories.html', {'categories': categories, 'category': category, 'blog_posts': blog_posts})


def categories(request, category_id):
    category = Category.objects.get(pk=category_id)
    category_posts = BlogPost.objects.filter(category=category)
    categories = Category.objects.all()
    # return {'categories': categories}
    return render(request, 'categories.html', {'categories': categories, 'category_posts': category_posts})


from django.contrib.auth.decorators import login_required

@login_required  # Make this view accessible to authenticated admins only
def approve_comment(request, comment_id):
    comment = Comment.objects.get(pk=comment_id)
    comment.approved = True
    comment.save()
    return redirect("blog_comments", slug=comment.blog.slug)
    # You can add a redirect or return response as needed

from .forms import BlogPostForm
def edit_blog_post(request, slug):
    blog_post = get_object_or_404(BlogPost, slug=slug)

    if request.method == 'POST':
        form = BlogPostForm(request.POST, instance=blog_post)
        if form.is_valid():
            form.save()
            return redirect('some_success_url')  # Redirect to a success page or another URL
    else:
        form = BlogPostForm(instance=blog_post)

    return render(request, 'edit_blog_post.html', {'form': form, 'blog_post': blog_post})


# class MyRegistrationView(SignupView):
#     template_name = 'register.html' 
# from django.contrib.sites.shortcuts import get_current_site
# from django.contrib.auth import login
# from django.core.mail import EmailMessage
# from django.http import HttpResponse
# from django.shortcuts import render, redirect
# from django.template.loader import render_to_string
# from django.utils.encoding import force_bytes, force_str
# from django.utils.http import urlsafe_base64_encode

# from allauth.account.views import SignupView
# from allauth.account.forms import BaseSignupForm
# from allauth.account.utils import complete_signup

# from .token import account_activation_token  # Make sure to import your token

# class MyRegistrationView(SignupView):
#     form_class = UserRegistrationForm  # Use the appropriate form class
#     template_name= 'register.html'
#     def form_valid(self, form):
#         # This method is called when the form is valid
#         response = super().form_valid(form)
#         # You can add your custom logic here, e.g., send verification email
#         self.send_verification_email(self.user)
#         return response

#     def send_verification_email(self, user):
#         current_site = get_current_site(self.request)
#         mail_subject = 'Activate your account.'
#         message = render_to_string('acc_active_email.html', {
#             'user': user,
#             'domain': current_site.domain,
#             'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#             'token': account_activation_token.make_token(user),
#         })
#         to_email = user.email
#         email = EmailMessage(
#             mail_subject, message, to=[to_email]
#         )
#         email.send()

#     def get(self, *args, **kwargs):
#         # This method is called for a GET request, you can add custom logic here if needed
#         return super().get(*args, **kwargs)

#     def post(self, *args, **kwargs):
#         # This method is called for a POST request, you can add custom logic here if needed
#         return super().post(*args, **kwargs)

#     def get_success_url(self):
#         # This method determines the URL to redirect to after successful registration
#         return '/success/'  # Change this to your desired URL



# from allauth.account.views import SignupView
# from allauth.account.utils import send_email_confirmation

# class MyRegistrationView(SignupView):
#     # template_name = 'register.html'

#     def form_valid(self, form):
#         response = super().form_valid(form)
#         # Send confirmation email
#         send_email_confirmation(self.request, self.user)
#         return response

# def activate(request, uidb64, token):
#     from allauth.account.models import EmailConfirmation, EmailConfirmationHMAC

#     try:
#         email_confirmation = EmailConfirmationHMAC.from_key(uidb64)
#     except EmailConfirmation.DoesNotExist:
#         email_confirmation = None

#     if email_confirmation and not email_confirmation.email_address.verified:
#         email_confirmation.confirm(request)
#         return HttpResponse('Thank you for your email confirmation. Now you can log in to your account.')
#     else:
#         return HttpResponse('Activation link is invalid or the email address is already verified!')


from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from allauth.account.models import EmailConfirmation, EmailConfirmationHMAC
from allauth.account.utils import send_email_confirmation
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
                    
# @login_required
def my_registration_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            # form.save()  # Save the user instance
            # # Additional logic after saving the user
            return redirect('success_page')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/sign_up.html', {'form': form})

# @require_POST
def activate(request, uidb64, token):
    try:
        email_confirmation = EmailConfirmationHMAC.from_key(uidb64)
    except EmailConfirmationHMAC.DoesNotExist:
        email_confirmation = None

    if email_confirmation and not email_confirmation.email_address.verified:
        email_confirmation.confirm(request)
        messages.success(request, 'Thank you for your email confirmation. Now you can log in to your account.')
    else:
        messages.error(request, 'Activation link is invalid or the email address is already verified!')

    return redirect('login')