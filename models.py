from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.timezone import now
from slugify import slugify
 
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(upload_to="profile_pics", blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    facebook = models.CharField(max_length=300, blank=True, null=True)
    instagram = models.CharField(max_length=300, blank=True, null=True)
    linkedin = models.CharField(max_length=300, blank=True, null=True)
    phone_no = models.CharField(max_length=15, blank=True, null=True)
    def __str__(self):
        return str(self.user)
    
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

 
STATUS = (
    (0,"Draft"),
    (1,"Publish")
)



class BlogPost(models.Model):
    title=models.CharField(max_length=255)
    author= models.ForeignKey(User, on_delete=models.CASCADE)
    # slug=models.CharField(max_length=130)
    content=models.TextField()
    image = models.ImageField(upload_to="profile_pics", blank=True, null=True)
    dateTime=models.DateTimeField(auto_now_add=True)
    created_on = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True) 
    status = models.IntegerField(choices=STATUS, default=0)
    slug = models.SlugField(unique=True)  # Unique slug

    def __str__(self):
        return str(self.author) +  " Blog Title: " + self.title
    
    def get_absolute_url(self):
        return reverse('blogs')
    
    
    def save(self, *args, **kwargs):
        if not self.slug:
            # Generate the slug from the title (or any other field)
            self.slug = slugify(self.title)

        super(BlogPost, self).save(*args, **kwargs)

    def get_absolute_url(self):
     return reverse('edit_blog_post', kwargs={'slug': self.slug})

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    blog = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)   
    dateTime=models.DateTimeField(default=now)
    approved = models.BooleanField(default=False) 
 
    def __str__(self):
        return f"Comment by {self.user.username} on {self.blog.title}"

