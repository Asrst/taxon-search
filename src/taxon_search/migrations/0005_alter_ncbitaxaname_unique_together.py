# Generated by Django 4.2.1 on 2023-06-11 18:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taxon_search', '0004_alter_ncbitaxanode_parent_id'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='ncbitaxaname',
            unique_together={('taxon_id', 'name', 'name_class')},
        ),
    ]