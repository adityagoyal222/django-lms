from courses.models import Course

def courses_processor(request):
    course = Course.objects.all()
    return {'list_courses': course}
