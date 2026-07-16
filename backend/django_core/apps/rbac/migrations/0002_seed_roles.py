from django.db import migrations


def seed_roles(apps, schema_editor):
    Role = apps.get_model("rbac", "Role")
    roles = [
        ("admin", "Full platform access — user management, all catalog/order operations"),
        ("manager", "Manages catalog, inventory, and orders — no user/role management"),
        ("seller", "Manages own product listings and views own orders"),
        ("customer", "Can browse, purchase, and manage own account"),
    ]
    for name, description in roles:
        Role.objects.get_or_create(name=name, defaults={"description": description})


def remove_roles(apps, schema_editor):
    Role = apps.get_model("rbac", "Role")
    Role.objects.filter(name__in=["admin", "manager", "seller", "customer"]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("rbac", "0001_initial"),
    ]
    operations = [
        migrations.RunPython(seed_roles, reverse_code=remove_roles),
    ]