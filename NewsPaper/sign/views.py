from django.contrib.auth.models import User
from django.core.mail import mail_admins
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.views.generic.edit import CreateView

from .models import BaseRegisterForm

from django.shortcuts import redirect, render
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'


@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/')
