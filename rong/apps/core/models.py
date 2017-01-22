from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from mptt.models import MPTTModel, TreeForeignKey

class Attribute(models.Model):
    name = models.CharField(max_length=30, unique=True)
    def __str__(self):
        return self.name

class Foo(MPTTModel):
    name = models.CharField(max_length=30, unique=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
    text = models.TextField(max_length=500, blank=True)
    attribute = models.ManyToManyField(Attribute, through='fooattribute')
    
    class MPTTMeta:
        order_insertion_by = ['name']
    def __str__(self):
        return self.name

class FooAnswer(MPTTModel):
    text = models.TextField(max_length=500, blank=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
    foo = models.ForeignKey(Foo, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    #class MPTTMeta:
    #    order_insertion_by = ['name']
    def __str__(self):
        return self.user.username

class fooattribute(models.Model):
    foo = models.ForeignKey(Foo, on_delete=models.CASCADE)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    value = models.CharField(max_length=128)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
#    field = models.ManyToManyField(Field, through='ProfileFieldView')

    def __str__(self):
        return self.user.username

class FieldType(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name

class Field(models.Model):
    name = models.CharField(max_length=30)
    profile = models.ManyToManyField(Profile, through='profilefieldview')
    ftype = models.ForeignKey(FieldType, on_delete=models.CASCADE)

    def __str__(self):
        return self.ftype.name +" "+ self.name

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class profilefieldview(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    field = models.ForeignKey(Field, on_delete=models.CASCADE)
    value = models.CharField(max_length=128)

