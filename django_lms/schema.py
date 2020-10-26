import graphene
from courses import schema as course_schema
from resources import schema as resource_schema
from users import schema as user_schema
from assignments import schema as assignment_schema


class Query(assignment_schema.Query, course_schema.Query, resource_schema.Query, user_schema.Query, graphene.ObjectType):
    pass


class Mutation(assignment_schema.Mutation, course_schema.Mutation, resource_schema.Mutation, user_schema.Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
