from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver

from Reading_Club.accounts.models import BaseUser


@receiver(post_migrate)
def create_user_groups(sender, **kwargs):
    if sender.name != "Reading_Club.accounts":
        return

    readers_group, _ = Group.objects.get_or_create(name="Readers")
    moderators_group, _ = Group.objects.get_or_create(name="Moderators")

    readers_permissions = Permission.objects.filter(
        content_type__app_label__in=["book", "collection", "review"],
        codename__in=[
            "add_book", "change_book",
            "add_collection", "change_collection",
            "add_review", "change_review",
        ],
    )

    moderators_permissions = Permission.objects.filter(
        content_type__app_label__in=["book", "collection", "review", "accounts"],
        codename__in=[
            "view_book", "add_book", "change_book", "delete_book",
            "view_collection", "add_collection", "change_collection", "delete_collection",
            "view_review", "add_review", "change_review", "delete_review",
            "view_baseuser", "change_baseuser",
        ],
    )

    readers_group.permissions.set(readers_permissions)
    moderators_group.permissions.set(moderators_permissions)


@receiver(post_save, sender=BaseUser)
def assign_readers_group(sender, instance, created, **kwargs):
    if not created:
        return

    readers_group, _ = Group.objects.get_or_create(name="Readers")
    instance.groups.add(readers_group)