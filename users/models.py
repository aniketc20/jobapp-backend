from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _

from .managers import CustomUserManager

class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(max_length=100, default='')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class Job(models.Model):
    posted_by = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE, default="", related_name="posted_by")
    desc = models.CharField(max_length=100, default='')
    accepted_candidate = models.ManyToManyField(CustomUser, blank=True, related_name="accepted_candidates")
    rejected_candidate = models.ManyToManyField(CustomUser, blank=True, related_name="rejected_candidates")
    applied_by = models.ManyToManyField(CustomUser, blank=True)

    def __str__(self):
        return self.desc

class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, null=True)
    applied_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, default='Applied')
    resume = models.FileField(null=True)

    def __str__(self):
        return "Posted by:" + self.job.posted_by.name + " Applied by:" + self.applied_by.name
    
    class Meta:
        unique_together = ('job', 'applied_by',)