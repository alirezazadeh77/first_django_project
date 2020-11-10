# Generated by Django 3.1.1 on 2020-10-22 12:29

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('commenting', '0002_auto_20200917_1120'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentVote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='created time')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='updated time')),
                ('vote', models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(-1), django.core.validators.MaxValueValidator(1)], verbose_name='vote')),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='votes', to='commenting.productcomment', verbose_name='comment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='votes', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'Comment vote',
                'verbose_name_plural': 'Comment votes',
            },
        ),
        migrations.AddConstraint(
            model_name='commentvote',
            constraint=models.UniqueConstraint(fields=('user', 'comment'), name='unique_user_vote'),
        ),
    ]