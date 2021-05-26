from django.db import models
from django.utils import timezone
#from jsonfield import JSONField
#from django.contrib.postgres.fields import JSONField
# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=20, unique= True)
    password = models.CharField(max_length=100)
    rank = models.CharField(max_length=10, null=False)
    name = models.CharField(max_length=10, null=False)
    enabled = models.BooleanField(default=False)
    ctime = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='userphoto/')
    content = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.name

class ExploitReport(models.Model):
    user = models.CharField(max_length=20, null=False)
    excute_date = models.CharField(max_length=50)
    target_name = models.CharField(max_length=50)
    target_url = models.CharField(max_length=1000)
    target_ip = models.CharField(max_length=50)
    target_port = models.CharField(max_length=10)    
    target_version = models.CharField(max_length=50)
    weakness = models.CharField(max_length=20)    
    search_time = models.CharField(max_length=20)
    source = models.CharField(max_length=50)
    IC_type = models.CharField(max_length=50)
    excute_location = models.CharField(max_length=50)
    vpn_ip = models.CharField(max_length=20)
    content = models.CharField(max_length=100000)
    use = models.CharField(max_length=50)
    admin = models.CharField(max_length=50)
    people = models.CharField(max_length=50)
    expected = models.CharField(max_length=1000)
    follow_up = models.CharField(max_length=1000)
    status = models.CharField(default="待審核",max_length=10, null=False)
    upload_date = models.DateField(default=timezone.now)
    
    def __str__(self):
        return self.target_name

class InforCollectReport(models.Model):
    user = models.CharField(max_length=20, null=False)
    excute_date = models.CharField(max_length=50)
    target_name = models.CharField(max_length=50)
    target_url = models.CharField(max_length=1000)
    target_location = models.CharField(max_length=50)
    target_ip = models.CharField(max_length=50)
    target_port = models.CharField(max_length=10)    
    target_warzone = models.CharField(max_length=10)
    weakness = models.CharField(max_length=20)    
    search_time = models.CharField(max_length=20)
    vpn_ip = models.CharField(max_length=20)
    content = models.CharField(max_length=100000)
    # image = models.ImageField(upload_to='image/')
    follow_up = models.CharField(max_length=1000)
    status = models.CharField(default="待審核",max_length=10, null=False)
    upload_date = models.DateField(default=timezone.now)
    

    def __str__(self):
        return self.target_name

class Images(models.Model):
    ex_post = models.ForeignKey(ExploitReport, default=None, on_delete=models.CASCADE,null=True)
    ic_post = models.ForeignKey(InforCollectReport, default=None, on_delete=models.CASCADE,null=True)
    content = models.CharField(max_length=10)
    content_id = models.CharField(max_length=2)
    image = models.ImageField(upload_to='img/')





    


    