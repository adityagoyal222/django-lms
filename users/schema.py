import graphene
from graphene_django.types import DjangoObjectType, ObjectType
from users.models import User, Profile

class UserType(DjangoObjectType):
    class Meta:
        model = User

class ProfileType(DjangoObjectType):
    class Meta:
        model = Profile

class Query(ObjectType):
    user = graphene.Field(UserType, id=graphene.Int())
    users = graphene.List(UserType)

    def resolve_user(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return User.objects.get(pk=id)

        return None

    def resolve_users(self, info, **kwargs):
        return User.objects.all()

class UserInput(graphene.InputObjectType):
    username = graphene.String()
    first_name = graphene.String()
    last_name = graphene.String()
    email = graphene.String()
    password = graphene.String()
    user_type = graphene.Int()

class CreateUser(graphene.Mutation):
    class Arguments:
        input = UserInput(required=True)
    
    ok = graphene.Boolean()
    user = graphene.Field(UserType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        user_instance = User(
            username=input.username,
            first_name=input.first_name,
            last_name=input.last_name,
            email=input.email,
            user_type=input.user_type
        )
        user_instance.set_password(input.password)  # Securely set the password
        user_instance.save()
        return CreateUser(ok=ok, user=user_instance)

class UpdateUser(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = UserInput(required=True)

    ok = graphene.Boolean()
    user = graphene.Field(UserType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        user_instance = User.objects.get(pk=id)
        if user_instance:
            ok = True
            user_instance.username = input.username
            user_instance.first_name = input.first_name
            user_instance.last_name = input.last_name
            user_instance.email = input.email
            user_instance.user_type = input.user_type
            if input.password:
                user_instance.set_password(input.password)  # Securely set the password
            user_instance.save()
            return UpdateUser(ok=ok, user=user_instance)
        return UpdateUser(ok=ok, user=None)

class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
