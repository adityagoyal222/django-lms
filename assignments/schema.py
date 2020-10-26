import graphene
from graphene_django.types import DjangoObjectType, ObjectType
from graphene_file_upload.scalars import Upload
from assignments.models import Assignment, SubmitAssignment
from courses.models import Course
from courses import schema as course_schema
from users import schema as user_schema


class AssignmentType(DjangoObjectType):
    class Meta:
        model = Assignment

class SubmissionType(DjangoObjectType):
    class Meta:
        model = SubmitAssignment

class Query(ObjectType):
    assignment = graphene.Field(AssignmentType, id=graphene.Int())
    submission = graphene.Field(SubmissionType, id=graphene.Int())
    assignments = graphene.List(AssignmentType)
    submissions = graphene.List(SubmissionType)

    def resolve_assignment(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Assignment.objects.get(pk=id)
        
        return None
    
    def resolve_submission(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return SubmitAssignment.objects.get(pk=id)
        
        return None
    
    def resolve_assignments(self, info, **kwargs):
        return Assignment.objects.all()
    
    def resolve_submissions(self, info, **kwargs):
        return SubmitAssignment.objects.all()

class AssignmentInput(graphene.InputObjectType):
    id = graphene.ID()
    assignment_name = graphene.String()
    assignment_description = graphene.String()
    start_date = graphene.DateTime()
    due_date = graphene.Date()
    due_time = graphene.Time()
    course = graphene.Field(course_schema.CourseInput)

class SubmissionInput(graphene.InputObjectType):
    id = graphene.ID()
    author = graphene.Field(user_schema.UserInput)
    topic = graphene.String()
    description = graphene.String()
    assignment_file = Upload()
    submitted_date = graphene.DateTime()
    assignment_ques = graphene.Field(AssignmentInput)
    graded = graphene.Boolean()
    grade = graphene.Int()

class CreateAssignment(graphene.Mutation):
    class Arguments:
        input = AssignmentInput(required=True)
    
    ok = graphene.Boolean()
    assignment = graphene.Field(AssignmentType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        assignment_instance = Assignment(
            assignment_name=input.assignment_name,
            assignment_description=input.assignment_description,
            start_date=input.start_date,
            due_date=input.due_date,
            due_time=input.due_time,
            course=input.course,
        )
        assignment_instance.save()
        return CreateAssignment(ok=ok, assignment=assignment_instance)

class UpdateAssignment(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = AssignmentInput(required=True)

    ok = graphene.Boolean()
    assignment = graphene.Field(AssignmentType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        assignment_instance = Assignment.objects.get(pk=id)
        if assignment_instance:
            ok = True
            assignment_instance.assignment_name = input.assignment_name
            assignment_instance.assignment_description = input.assignment_description
            assignment_instance.start_date = input.start_date
            assignment_instance.due_date = input.due_date
            assignment_instance.due_time = input.due_time
            assignment_instance.course = input.course
            assignment_instance.save()
            return UpdateAssignment(ok=ok, assignment=assignment_instance)
        return UpdateAssignment(ok=ok, assignment=None)

class CreateSubmission(graphene.Mutation):
    class Arguments:
        input = SubmissionInput(required=True)

    ok = graphene.Boolean()
    submission = graphene.Field(SubmissionType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        submission_instance = SubmitAssignment(
            author=input.author,
            topic=input.topic,
            description=input.description,
            assignment_file=input.assignment_file,
            submitted_date=input.submitted_date,
            assignment_ques=input.assignment_ques,
            graded=input.graded,
            grade=input.grade,
        )
        submission_instance.save()
        return CreateSubmission(ok=ok, submission=submission_instance)

class UpdateSubmission(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=False)
        input = SubmissionInput(required=True)

    ok = graphene.Boolean()
    submission = graphene.Field(SubmissionType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        submission_instance = SubmitAssignment.objects.get(pk=id)
        if submission_instance:
            ok = True
            submission_instance.author=input.author,
            submission_instance.topic=input.topic,
            submission_instance.description=input.description,
            submission_instance.assignment_file=input.assignment_file
            submission_instance.submitted_date=input.submitted_date
            submission_instance.assignment_ques=input.assignment_ques
            submission_instance.graded=input.graded
            submission_instance.grade=input.grade
            submission_instance.save()
            return UpdateSubmission(ok=ok, submission=submission_instance)
        return UpdateSubmission(ok=ok, submission=None)

class Mutation(graphene.ObjectType):
    create_assignment = CreateSubmission.Field()
    update_assignment = UpdateAssignment.Field()
    create_submission = CreateSubmission.Field()
    update_submission = UpdateSubmission.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
        