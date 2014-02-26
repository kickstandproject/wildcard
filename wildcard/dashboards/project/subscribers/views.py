# vim: tabstop=4 shiftwidth=4 softtabstop=4

#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.debug import sensitive_post_parameters

from horizon import exceptions
from horizon import forms
from horizon import tables

from wildcard import api

from wildcard.dashboards.project.subscribers \
    import forms as project_forms
from wildcard.dashboards.project.subscribers \
    import tables as project_tables


INDEX_URL = reverse_lazy('horizon:project:subscribers:index')


class IndexView(tables.DataTableView):
    table_class = project_tables.SubscribersTable
    template_name = 'project/subscribers/index.html'

    def get_data(self):
        try:
            return api.ripcord.subscriber_list(self.request)
        except Exception:
            exceptions.handle(
                self.request, _('Unable to retrieve subscriber list.')
            )


class CreateView(forms.ModalFormView):
    form_class = project_forms.CreateSubscriberForm
    template_name = 'project/subscribers/create.html'
    success_url = INDEX_URL

    @method_decorator(sensitive_post_parameters('password',))
    def dispatch(self, *args, **kwargs):
        return super(CreateView, self).dispatch(*args, **kwargs)


class UpdateView(forms.ModalFormView):
    form_class = project_forms.UpdateSubscriberForm
    template_name = 'project/subscribers/update.html'
    success_url = INDEX_URL

    @method_decorator(sensitive_post_parameters('password',))
    def dispatch(self, *args, **kwargs):
        return super(UpdateView, self).dispatch(*args, **kwargs)

    def get_object(self):
        if not hasattr(self, "_object"):
            try:
                self._object = api.ripcord.subscriber_get(
                    self.request, self.kwargs['subscriber_id'])
            except Exception:
                exceptions.handle(
                    self.request,
                    _('Unable to update subscriber.'),
                    redirect=self.success_url
                )
        return self._object

    def get_context_data(self, **kwargs):
        context = super(UpdateView, self).get_context_data(**kwargs)
        context['subscriber'] = self.get_object()
        return context

    def get_initial(self):
        subscriber = self.get_object()
        fields = ['uuid', 'username', 'domain', 'email_address', 'rpid']
        return {f: getattr(subscriber, f) for f in fields}
