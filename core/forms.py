# -*- coding: utf-8 -*-

from django import forms
# from django.core.urlresolvers import reverse_lazy

from django.core.exceptions import ValidationError
from django.forms.fields import FileField

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit, Div, Field


class LoginForm(forms.Form):

    username = forms.CharField(
        label="Usuario",
        max_length=254,
        required=True,
    )

    password = forms.CharField(
        label="Contraseña",
        max_length=4096,
        required=True,
        widget=forms.PasswordInput,
    )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-4'
        self.helper.field_class = 'col-sm-8'
        self.helper.form_method = 'post'
        self.helper.form_action = ''
        self.helper.form_show_labels = True
        self.helper.layout = Layout(
            Div(
                Field('username'),
                Field('password'),
                ButtonHolder(
                    Submit('submit', 'Ingresar', css_class='btn-primary'),
                ),
                css_class="col-sm-6 col-sm-offset-3",
            ),
        )
        super(LoginForm, self).__init__(*args, **kwargs)


class FormWithUneditableMixin(object):
    """
    Avoid cleaning and reading uneditablefields.
    UneditableFields are set in the Set type attribute: form.uneditablefields.
    """
    uneditablefields = set()

    def _clean_fields(self):
        for name, field in self.fields.items():
            # value_from_datadict() gets the data from the data dictionaries.
            # Each widget type knows how to retrieve its own data, because some
            # widgets split data over several HTML fields.

            # begin avoid cleaning disabled fields self.uneditablefields
            if name in self.uneditablefields:
                self.cleaned_data[name] = getattr(self.instance, name)
                continue
            # end avoid...

            value = field.widget.value_from_datadict(
                self.data, self.files, self.add_prefix(name)
            )
            try:
                if isinstance(field, FileField):
                    initial = self.initial.get(name, field.initial)
                    value = field.clean(value, initial)
                else:
                    value = field.clean(value)
                self.cleaned_data[name] = value
                if hasattr(self, 'clean_%s' % name):
                    value = getattr(self, 'clean_%s' % name)()
                    self.cleaned_data[name] = value
            except ValidationError as e:
                self._errors[name] = self.error_class(e.messages)
                if name in self.cleaned_data:
                    del self.cleaned_data[name]
