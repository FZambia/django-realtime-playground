# coding: utf-8
from django.views import generic
from django.core.urlresolvers import reverse
from realtime import models
from django.utils import simplejson as json
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.conf import settings


class MessageListView(generic.ListView):
    queryset = models.Message.objects.all()[:10]

    def get_context_data(self, *args, **kwargs):
        context = super(MessageListView, self).get_context_data(*args, **kwargs)
        context['async_url'] = settings.ASYNC_BACKEND_URL
        return context

class MessageCreateView(generic.CreateView):
    model = models.Message
    template_name = "realtime/message_create.html"
    success_url = reverse_lazy("realtime_message_list")

    def form_valid(self, form):
        self.object = form.save()
        if self.request.is_ajax():
            context = {'status': 'ok', 'message': self.object.as_dict()}
            return HttpResponse(json.dumps(context), mimetype="application/json")
        else:
            return HttpResponseRedirect(self.get_success_url())


class MessageDeleteView(generic.DeleteView):
    model = models.Message

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        if self.request.is_ajax():
            return HttpResponse(json.dumps({'status': 'ok'}), mimetype="application/json")
        else:
            return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
    	return reverse("realtime_message_list")
