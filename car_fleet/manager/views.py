from typing import Any
from django.contrib.auth import authenticate, login
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.shortcuts import render
from django.views.generic import ListView
from vehicle.models import Vehicle
from enterprise.models import Enterprise
from manager.models import Manager


class LoginManager(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'manager/login.html', context={'username': ''})

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            r = HttpResponseRedirect(reverse('menu'))
            r.set_cookie(key="offset", value=request.POST.get('offset'))
            return r
        else:
            return render(request, 'manager/login.html', context={'username': username})


class Menu(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'manager/menu.html')


class IndexEnterprises(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        if isinstance(getattr(user, 'manager', None), Manager):
            user = request.user
            enterprises = Enterprise.objects.filter(manager=user)
            return render(request,
                          'manager/index_enterprise.html',
                          context={'enterprises': list(enterprises),
                                   'manager': user})

        return HttpResponseForbidden('Необходима аутентификация в качестве \
менеджера\n')


class ViewEnterprise(ListView):
    paginate_by = 5
    model = Vehicle
    template_name = 'manager/enterprise.html'
    enterprise = None

    def get(self, request, *args, **kwargs):
        v = Vehicle.objects.all()[0]
        response = super().get(request, *args, **kwargs)
        ViewEnterprise.enterprise = kwargs['name']
        response.context_data['enterprise'] = ViewEnterprise.enterprise
        return response

    def get_queryset(self):
        return Vehicle.objects.filter(enterprise__name=ViewEnterprise.enterprise)
