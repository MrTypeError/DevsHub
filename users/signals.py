from django.db.models.signals import post_save , post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile


# @receiver(post_save, sender=Profile)
def createProfile(sender , instance , created , **kwargs):
    print('Profile Signal Triggered')
    if created:
        user = instance
        profile = Profile.objects.create(
            user = user,
            username = user.username,
            email = user.email,
            name = user.first_name,
        )

def updateUser(sender , instance , created , **kwargs):
    profile = instance
    user = profile.user

    if created == False:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()

def deleteProfile(sender , instance , **kwargs):
    user = instance.user
    user.delete()


post_save.connect(createProfile , sender=User)
post_save.connect(updateUser , sender=Profile)
post_delete.connect(deleteProfile , sender=Profile)

