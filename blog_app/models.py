from django.db import models

# Create your models here.
#blogcontent
class Blog(models.Model):
    name=models.CharField(max_length=100,default="")
    title=models.CharField(max_length=100,default="")
    short_desc=models.CharField(max_length=100,default="")
    content=models.TextField()
    thumbnail=models.ImageField(upload_to="blogimages")
    created_at=models.TimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
#comments under blog
    
class Comment(models.Model):
    blog=models.ForeignKey(Blog,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    comment=models.TextField()
    created_at=models.TimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
#reply of each comment
    
class Reply(models.Model):
    name=models.CharField(max_length=100,default="")
    reply=models.TextField()
    commentParent=models.ForeignKey(Comment,on_delete=models.CASCADE)
    created_at=models.TimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    

