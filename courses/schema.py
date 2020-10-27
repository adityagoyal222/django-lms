import graphene
from graphene_django.types import DjangoObjectType, ObjectType
from courses.models import Course
from users.models import User
from users import schema as user_schema

class CourseType(DjangoObjectType):
    class Meta:
        model = Course

class Query(ObjectType):
    course = graphene.Field(CourseType, id=graphene.Int())
    courses = graphene.List(CourseType)
    
    def resolve_course(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Course.objects.get(pk=id)
        
        return None
    
    def resolve_courses(self, info, **kwargs):
        return Course.objects.all()

class CourseInput(graphene.InputObjectType):
    id = graphene.ID()
    course_name = graphene.String()
    course_description = graphene.String()
    teacher = graphene.List(user_schema.UserInput)
    students = graphene.List(user_schema.UserInput)

class CreateCourse(graphene.Mutation):
    class Arguments:
        input = CourseInput(required = True)

    ok = graphene.Boolean()
    course = graphene.Field(CourseType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        students = []
        
        teacher = []
        for student_input in input.students:
            student = User.objects.get(pk=student_input.id)
            if student is None:
                return CreateCourse(ok=False, course=None)
            students.append(student)
        # for teacher_input in input.teacher:
        #     teacher = User.objects.get(pk=teacher_input.id)
        #     if teacher is None:
        #         return CreateCourse(ok=False, course=None)
        #     teacher.append(teacher)
        course_instance = Course(
            course_name = input.course_name,
            course_description = input.course_description,
        )
        course_instance.save()
        course_instance.teacher.det(teacher)
        course_instance.students.set(students)
        return CreateCourse(ok=ok, course=course_instance)
    
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
            course_instance.teacher = input.teacher
            course_instance.save()
            course_instance.students.set(students)
            return UpdateCourse(ok=ok, course=course_instance)
        return UpdateCourse(ok=ok, course=None)

class Mutation(graphene.ObjectType):
    create_course = CreateCourse.Field()
    update_course = UpdateCourse.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
