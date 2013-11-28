# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2012 NEC Corporation
#
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


from django.core.urlresolvers import reverse, reverse_lazy  # noqa
from django.utils.translation import ugettext_lazy as _  # noqa

from horizon import exceptions
from horizon import forms
from horizon import tables

from wildcard import api

from wildcard.dashboards.project.queues \
    import forms as project_forms
from wildcard.dashboards.project.queues \
    import tables as project_tables


class IndexView(tables.DataTableView):
    table_class = project_tables.QueuesTable
    template_name = 'project/queues/index.html'

    def get_data(self):
        try:
            return api.payload.queue_list(self.request)
        except Exception:
            exceptions.handle(
                self.request, _('Unable to retrieve queue list.')
            )


class CreateView(forms.ModalFormView):
    form_class = project_forms.CreateQueueForm
    template_name = 'project/queues/create.html'
    success_url = reverse_lazy('horizon:project:queues:index')


class UpdateView(forms.ModalFormView):
    form_class = project_forms.UpdateQueueForm
    template_name = 'project/queues/update.html'
    success_url = reverse_lazy('horizon:project:queues:index')

    def get_object(self):
        if not hasattr(self, "_object"):
            try:
                self._object = api.payload.queue_get(
                    self.request, self.kwargs['queue_id'])
            except Exception:
                redirect = reverse("horizon:project:queues:index")
                exceptions.handle(
                    self.request,
                    _('Unable to update queue.'),
                    redirect=redirect
                )
        return self._object

    def get_context_data(self, **kwargs):
        context = super(UpdateView, self).get_context_data(**kwargs)
        context['queue'] = self.get_object()
        return context

    def get_initial(self):
        queue = self.get_object()
        return {
            'uuid': queue.uuid,
            'name': queue.name,
            'description': queue.description,
        }
