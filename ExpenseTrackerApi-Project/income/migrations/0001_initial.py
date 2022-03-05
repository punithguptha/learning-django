# Generated by Django 3.2 on 2022-03-05 17:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Income',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.CharField(choices=[('SALARY', 'SALARY_HUMAN_READABLE_FIELD'), ('BUSINESS', 'BUSINESS_HUMAN_READABLE_FIELD'), ('SIDE_HUSTLES', 'SIDE_HUSTLES_HUMAN_READABLE_FIELD'), ('OTHERS', 'OTHERS_HUMAN_READABLE_FIELD')], max_length=255)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField()),
                ('date', models.DateField()),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
