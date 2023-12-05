from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views import generic
from resources.forms import CreateResourceForm
from resources.models import Resource
from resources.models import VideoLesson, VideoProgress
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
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

def video_lesson_view(request):


    video = VideoLesson.objects.get(pk=1)
    video_id = video.video_lesson_id   # '9bZkp7q19f0'
    context = {
        'video_id': video_id,
    }
    
    # Render the template and pass the context data
    return render(request, 'resources/resource_base.html', context)

@csrf_protect
def update_video_progress(request):
    if request.method == 'POST':
        video_id = request.POST.get('video_id')
        progress = request.POST.get('progress')
        video_lesson = VideoLesson.objects.get(video_lesson_id=video_id)    
        # Find the VideoProgress object for the specified video_id and update the progress
        video_progress, created = VideoProgress.objects.get_or_create(video_lesson=video_lesson, user=request.user)
        video_progress.progress = progress
        if float(progress) == 75:
            video_progress.status = True
        video_progress.save()
        
        return JsonResponse({'message': 'Video progress updated successfully.'})

    return JsonResponse({'message': 'Invalid request method.'}, status=400)



