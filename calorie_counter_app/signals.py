from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import FoodItem, Activity

@receiver(post_save, sender=FoodItem)
def set_global_and_approved_by_admin(sender, instance, created, **kwargs):
    if created:
        if instance.added_by.is_staff:
            instance.is_global = True
            instance.approved_by_admin = True
            instance.save()
        else:
            instance.is_global = False
            instance.approved_by_admin = False
            instance.save()

@receiver(post_save, sender=Activity)
def set_global_and_approved_by_admin(sender, instance, created, **kwargs):
    if created:
        if instance.added_by.is_staff:
            instance.is_global = True
            instance.approved_by_admin = True
            instance.save()
        else:
            instance.is_global = False
            instance.approved_by_admin = False
            instance.save()
