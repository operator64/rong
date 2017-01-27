from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from mptt.models import MPTTModel, TreeForeignKey

from django.utils.translation import gettext_lazy as _


# Property
class Trait(models.Model):
    name = models.CharField(max_length=30, unique=True, verbose_name = _('Property'))
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Entry Property')
        verbose_name_plural = _('Entrie Properties')


class Node(MPTTModel):
    name = models.CharField(max_length=30, unique=True, verbose_name=_('Title'))
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
    text = models.TextField(max_length=500, blank=True)
    trait = models.ManyToManyField(Trait, through='NodeTrait')
    created = models.DateField(auto_now=False, auto_now_add=True)
    modified = models.DateField(auto_now=True, auto_now_add=False)
    
    class Meta:
        verbose_name = _('Entry')
        verbose_name_plural = _('Entries')

    class MPTTMeta:
        order_insertion_by = ['name']
    def __str__(self):
        return self.name

class NodeNote(MPTTModel):
    text = models.TextField(max_length=500, blank=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
    node = models.ForeignKey(Node, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateField(auto_now=False, auto_now_add=True)
    modified = models.DateField(auto_now=True, auto_now_add=False)
    
    #class MPTTMeta:
    #    order_insertion_by = ['name']
    def __str__(self):
        return self.text

class NodeTrait(models.Model):
    node = models.ForeignKey(Node, on_delete=models.CASCADE)
    trait = models.ForeignKey(Trait, on_delete=models.CASCADE, verbose_name=_('Property'))
    value = models.CharField(max_length=128)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
#    field = models.ManyToManyField(Field, through='ProfileFieldView')

    def __str__(self):
        return self.user.username

class EType(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Profile Field Type')
        verbose_name_plural = _('Profile Field Types')

class Expander(models.Model):
    name = models.CharField(max_length=30)
    profile = models.ManyToManyField(Profile, through='ProfileExpander')
    etype = models.ForeignKey(EType, on_delete=models.CASCADE)

    def __str__(self):
        return self.ftype.name +" "+ self.name

    class Meta:
        verbose_name = _('Additional Profile Field')
        verbose_name_plural = _('Additional Profile Fields')

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class ProfileExpander(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    expander = models.ForeignKey(Expander, on_delete=models.CASCADE, verbose_name=_('Profile Field'))
    value = models.CharField(max_length=128)

    class Meta:
        verbose_name = _('Profile Field')
        verbose_name_plural = _('Profile Fields')
