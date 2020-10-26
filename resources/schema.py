import graphene
from graphene_django.types import DjangoObjectType, ObjectType
from graphene_file_upload.scalars import Upload
from resources.models import Resource
from courses.models import Course
from courses import schema as course_schema


class ResourceType(DjangoObjectType):
    class Meta:
        model = Resource


class Query(ObjectType):
    resource = graphene.Field(ResourceType, id=graphene.Int())
    resources = graphene.List(ResourceType)

    def resolve_resource(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Resource.objects.get(pk=id)

        return None

    def resolve_resources(self, info, **kwargs):
        return Resource.objects.all()


class ResourceInput(graphene.InputObjectType):
    id = graphene.ID()
    resource_name = graphene.String()
    resource_file = Upload()
    course = graphene.Field(course_schema.CourseInput)


class CreateResource(graphene.Mutation):
    class Arguments:
        input = ResourceInput(required=True)

    ok = graphene.Boolean()
    resource = graphene.Field(ResourceType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        resource_instance = Resource(
            resource_name=input.resource_name,
            resource_file=input.resource_file,
            course=input.course,
        )
        resource_instance.save()
        return CreateResource(ok=ok, resource=resource_instance)


class UpdateResource(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = ResourceInput(required=True)

    ok = graphene.Boolean()
    resource = graphene.Field(ResourceType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        resource_instance = Resource.objects.get(pk=id)
        if resource_instance:
            ok = True
            resource_instance.resource_name = input.resource_name
            resource_instance.resource_file = input.resource_file
            resource_instance.course = input.course
            resource_instance.save()
            return UpdateResource(ok=ok, resource=resource_instance)
        return UpdateResource(ok=ok, resource=None)


class Mutation(graphene.ObjectType):
    create_resource = CreateResource.Field()
    update_resource = UpdateResource.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
