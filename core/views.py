# -*- coding: utf-8 -*-

from django.contrib.auth import logout
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse_lazy
from django.core.paginator import InvalidPage
from django.shortcuts import render

from django.contrib.auth import authenticate, login

from forms import LoginForm


def login_user(request):
    errors = []
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    next_url = request.GET.get(
                        'next', reverse_lazy('dermatologia_index')
                    )
                    return HttpResponseRedirect(next_url)
                else:
                    error = {
                        'label': 'Error.',
                        'text': 'El usuario ' + str(username) +
                        ' se encuentra deshabilitado. ' +
                        'Consulte al administrador del sistema.',
                    }
                    errors.append(error)
            else:
                error = {
                    'label': 'Error.',
                    'text': 'El nombre de usuario o contraseña es inválido.' +
                    'Intente nuevamente.',
                }
                errors.append(error)
    else:
        form = LoginForm()
    return render(request, 'login.html', {
        'form': form,
        'errors': errors,
    })


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse_lazy('login_view'))


class PaginationOverflowMixin(object):

    """
    Mixin para que devuelva el contenido de la última
    página en el caso de pedir una fuera del rango.
    """

    def paginate_queryset(self, queryset, page_size):
        """
        Paginate the queryset, if needed.
        """
        paginator = self.get_paginator(
            queryset, page_size, allow_empty_first_page=self.get_allow_empty()
        )
        page_kwarg = self.page_kwarg
        page = self.kwargs.get(page_kwarg) or\
            self.request.GET.get(page_kwarg) or 1
        try:
            page_number = int(page)
        except ValueError:
            if page == 'last':
                page_number = paginator.num_pages
            else:
                raise Http404(
                    _("Page is not 'last', nor can it be converted to an int.")
                )
        try:
            page = paginator.page(page_number)
            return (paginator, page, page.object_list, page.has_other_pages())
        except InvalidPage as e:
            try:
                page = paginator.page(paginator.num_pages)
                return (
                    paginator, page, page.object_list, page.has_other_pages()
                )
            except:
                raise Http404(
                    _('Invalid page (%(page_number)s): %(message)s') % {
                        'page_number': page_number,
                        'message': str(e)
                    }
                )


class SessionMixin(object):

    """
    Mixin para el acceso a variables de session
    """

    session_prefix = ""

    def set_session(self, var_name, var_value):
        self.request.session[self.session_prefix + var_name] = var_value

    def get_session(self, var_name):
        return self.request.session.get(self.session_prefix + var_name, None)
