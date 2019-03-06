
from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    """User authentication"""

    is_regular = models.BooleanField(default=False)
    is_practitioner = models.BooleanField(default=False)

class RegularProfile(models.Model):
    """Regular Profile model"""

    choices = (("YES", 'Yes'), ("NO", 'No'))
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='pictures')

    malaria = models.CharField(max_length=5, choices=choices)
    typhoid = models.CharField(max_length=5, choices=choices)
    cholera = models.CharField(max_length=5, choices=choices)
    fever = models.CharField(max_length=5, choices=choices)
    small_pox = models.CharField(max_length=5, choices=choices)
    apollo = models.CharField(max_length=5, choices=choices)
    measles = models.CharField(max_length=5, choices=choices)


    def __str__(self):
        return f'{self.user.username} RegularProfile'

    def create_user_profile(sender, instance, created, **kwargs):
        """Creates a profile for each registered regular user"""

        if created and instance.is_regular:
            RegularProfile.objects.create(user=instance)

    post_save.connect(create_user_profile, sender=User)

    def save(self, *args, **kwargs):
        """Save profile and resize profile image"""

        super(RegularProfile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)
        if img.height>300 or img.width>300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class PractitionerProfile(models.Model):
    """Practitioner Profile Model"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default1.jpg', upload_to='pictures')

    def __str__(self):
        return f'{self.user.username} PractitionerProfile'

    def create_user_profile(sender, instance, created, **kwargs):
        """Creates a profile for each registered practitioner user"""

        if created and instance.is_practitioner:
            PractitionerProfile.objects.create(user=instance)

    post_save.connect(create_user_profile, sender=User)

    def save(self, *args, **kwargs):
        """Save profile and resize profile image"""

        super(PractitionerProfile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)
        if img.height>300 or img.width>300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)