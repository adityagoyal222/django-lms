from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views import generic
from resources.forms import CreateResourceForm
from resources.models import Resource

# Create your views here.


class CreateResource(LoginRequiredMixin, generic.CreateView):
    form_class = CreateResourceForm
    template_name = 'resources/create_resource_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


@login_required
def delete_view(request, pk):
    obj = get_object_or_404(Resource, pk=pk)
    context = {'resource': obj}
    if request.method == "POST":
        obj.delete()
        return HttpResponseRedirect(reverse("courses:list"))
    return render(request, "resources/resource_confirm_delete.html", context)


