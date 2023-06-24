from django.http import HttpResponseForbidden
from django.views import View
from django.shortcuts import render
from enterprise.models import Enterprise
from manager.models import Manager


class Companies(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        if isinstance(getattr(user, 'manager', None), Manager):
            user = request.user
            companies = Enterprise.objects.filter(manager=user)
            return render(request,
                          'manager/index_enterprise.html',
                          context={'companies' : list(companies),
                                   'manager' : user})

        return HttpResponseForbidden('Необходима аутентификация в качестве менеджера\n')
