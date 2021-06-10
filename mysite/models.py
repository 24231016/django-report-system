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

    def __str__(self):
        return self.name

class ExploitReport(models.Model):
    user = models.CharField(max_length=20)
    excute_date = models.CharField(max_length=50, blank=True, null=True)
    target_name = models.CharField(max_length=50, blank=True)
    target_url = models.CharField(max_length=1000, blank=True, null=True)
    target_ip = models.CharField(max_length=50, blank=True)
    target_port = models.CharField(max_length=10, blank=True)    
    target_version = models.CharField(max_length=50, blank=True)
    weakness = models.CharField(max_length=20, blank=True)    
    search_time = models.CharField(max_length=20, blank=True)
    source = models.CharField(max_length=50, blank=True)
    IC_type = models.CharField(max_length=50, blank=True)
    excute_location = models.CharField(max_length=50, blank=True)
    vpn_ip = models.CharField(max_length=20, blank=True)
    content = models.CharField(max_length=100000, blank=True)
    use = models.CharField(max_length=50, blank=True)
    admin = models.CharField(max_length=50, blank=True)
    people = models.CharField(max_length=50, blank=True)
    expected = models.CharField(max_length=1000, blank=True)
    follow_up = models.CharField(max_length=1000, blank=True)
    status = models.CharField(default="待審核",max_length=10, null=False, blank=True)
    upload_date = models.DateField(default=timezone.now)
    
    def __str__(self):
        return self.target_name

# class InforCollectReport(models.Model):
#     user = models.CharField(max_length=20, null=False)
#     excute_date = models.CharField(max_length=50)
#     target_name = models.CharField(max_length=50)
#     target_url = models.CharField(max_length=1000)
#     target_location = models.CharField(max_length=50)
#     target_ip = models.CharField(max_length=50)
#     target_port = models.CharField(max_length=10)    
#     target_warzone = models.CharField(max_length=10)
#     weakness = models.CharField(max_length=20)    
#     search_time = models.CharField(max_length=20)
#     vpn_ip = models.CharField(max_length=20)
#     content = models.CharField(max_length=100000)
#     # image = models.ImageField(upload_to='image/')
#     follow_up = models.CharField(max_length=1000)
#     status = models.CharField(default="待審核",max_length=10, null=False)
#     upload_date = models.DateField(default=timezone.now)
    

#     def __str__(self):
#         return self.target_name

class Images(models.Model):
    ex_post = models.ForeignKey(ExploitReport, default=None, on_delete=models.CASCADE,null=True)
    # ic_post = models.ForeignKey(InforCollectReport, default=None, on_delete=models.CASCADE,null=True)
    content = models.CharField(max_length=10)
    content_id = models.CharField(max_length=2)
    image = models.ImageField(upload_to='img/')





    


    
