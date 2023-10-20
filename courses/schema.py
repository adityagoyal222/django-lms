import graphene
from graphene_django.types import DjangoObjectType, ObjectType
from courses.models import Course, Chapter, Lesson
from users.models import User
from users import schema as user_schema

class CourseType(DjangoObjectType):
    class Meta:
        model = Course

class ChapterType(DjangoObjectType):
    class Meta:
        model = Chapter
    course = graphene.Field(CourseType)


class LessonType(DjangoObjectType):
    class Meta:
        model = Lesson
    chapter = graphene.Field(ChapterType)

class Query(ObjectType):
    course = graphene.Field(CourseType, id=graphene.Int())
    courses = graphene.List(CourseType)
    
    chapter = graphene.Field(ChapterType, id=graphene.Int())
    all_chapters = graphene.List(ChapterType)   
    
    lesson = graphene.Field(LessonType, id=graphene.Int())
    all_lessons = graphene.List(LessonType)
    
    def resolve_course(root, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Course.objects.get(pk=id)
        
        return None
    
    def resolve_courses(root, info, **kwargs):
        return Course.objects.all()
    
    def resolve_chapter(root, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Chapter.objects.get(pk=id)
        
        return None
    
    def resolve_all_chapters(root, info, **kwargs):
        return Chapter.objects.all()
    
    def resolve_lesson(root, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Lesson.objects.get(pk=id)
        
        return None
    
    def resolve_all_lessons(self, info, **kwargs):
        return Lesson.objects.all()
    

class CourseInput(graphene.InputObjectType):
    id = graphene.ID()
    course_name = graphene.String()
    course_description = graphene.String()
    teacher = graphene.Field(user_schema.UserInput)
    students = graphene.List(user_schema.UserInput)

class ChapterInput(graphene.InputObjectType):
    id = graphene.ID()
    chapter_name = graphene.String()
    chapter_description = graphene.String()
    course = graphene.ID()

class LessonInput(graphene.InputObjectType):
    id = graphene.ID()
    lesson_name = graphene.String()
    lesson_content = graphene.String()
    chapter = graphene.ID()
    
class CreateCourse(graphene.Mutation):
    class Arguments:
        input = CourseInput(required = True)

    ok = graphene.Boolean()
    course = graphene.Field(CourseType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        students = []
        teacher = User.objects.get(pk=input.teacher.id)
        for student_input in input.students:
            student = User.objects.get(pk=student_input.id)
            if student is None:
                return CreateCourse(ok=False, course=None)
            students.append(student)
        course_instance = Course(
            course_name = input.course_name,
            course_description = input.course_description,
            teacher = teacher
        )
        course_instance.save()
        course_instance.students.set(students)
        return CreateCourse(ok=ok, course=course_instance)

class CreateChapter(graphene.Mutation):
    class Arguments:
        chapter_input = ChapterInput()
        course_id = graphene.ID(required=True)
    
    chapter = graphene.Field(ChapterType)
    
    @staticmethod
    def mutate(root, info, chapter_input=None, course_id=None):
        course = Course.objects.get(pk=course_id)
        if course is None:
            return CreateChapter(chapter=None)
        
        chapter = Chapter(
            chapter_name = chapter_input.chapter_name,
            chapter_description = chapter_input.chapter_description,
            course = course
        )
        chapter.save()
        return CreateChapter(chapter=chapter)
    
class CreateLesson(graphene.Mutation):
    class Arguments:
        lesson_input= LessonInput()
        chapter_id = graphene.ID(required=True)
        
    lesson = graphene.Field(LessonType)
    
    @staticmethod
    def mutate(root, info, lesson_input=None, chapter_id=None):
        chapter = Chapter.objects.get(pk=chapter_id)
        
        if chapter is None:
            return CreateLesson(lesson=None)
        
        lesson = Lesson(
            lesson_name = lesson_input.lesson_name,
            lesson_content = lesson_input.lesson_content,
            chapter = chapter)
        lesson.save()
        return CreateLesson(lesson=lesson)
        
    
class UpdateCourse(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = CourseInput(required=True)

    ok = graphene.Boolean()
    course = graphene.Field(CourseType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        course_instance = Course.objects.get(pk=id)
        teacher = User.objects.get(pk=input.teacher.id)
        if course_instance:
            ok = True
            students = []
            for student_input in input.students:
                student = User.objects.get(pk=student_input.id)
                if student is None:
                    return UpdateCourse(ok=False, course=None)
                students.append(student)
            course_instance.course_name = input.course_name
            course_instance.course_description = input.course_description
            course_instance.teacher = teacher
            course_instance.save()
            course_instance.students.set(students)
            return UpdateCourse(ok=ok, course=course_instance)
        return UpdateCourse(ok=ok, course=None)

class UpdateChapter(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        chapter_input = ChapterInput(required=True)
        
    ok = graphene.Boolean()
    chapter = graphene.Field(ChapterType)
    
    @staticmethod
    def mutate(root, info, id, chapter_input=None):
        ok = False
        chapter_instance = Chapter.objects.get(pk=id)
        if chapter_instance:
            ok = True
            chapter_instance.chapter_name = chapter_input.chapter_name
            chapter_instance.chapter_description = chapter_input.chapter_description
            chapter_instance.save()
            return UpdateChapter(ok=ok, chapter=chapter_instance)
        return UpdateChapter(ok=ok, chapter=None)
class UpdateLesson(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        lesson_input = LessonInput(required = True)
        
    ok = graphene.Boolean()
    lesson = graphene.Field(LessonType)
    
    @staticmethod
    def mutate(root, info, id, lesson_input=None):
        ok = False
        lesson_instance = Lesson.objects.get(pk=id)
        
        if lesson_instance:
            ok = True
            lesson_instance.lesson_name = lesson_input.lesson_name
            lesson_instance.lesson_content = lesson_input.lesson_content
            lesson_instance.save()
            return UpdateLesson(ok=ok, lesson=lesson_instance)
        return UpdateLesson(ok=ok, lesson=None)
    
class Mutation(graphene.ObjectType):
    create_course = CreateCourse.Field()
    update_course = UpdateCourse.Field()
    create_chapter = CreateChapter.Field()
    update_chapter = UpdateChapter.Field()
    create_lesson = CreateLesson.Field()
    update_lesson = UpdateLesson.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
