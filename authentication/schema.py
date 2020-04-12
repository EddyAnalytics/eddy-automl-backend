import graphene
from graphene_django import DjangoObjectType

from authentication.models import User


# User
class UserType(DjangoObjectType):
    class Meta:
        model = User


class CreateUser(graphene.Mutation):
    """
    A normal user can not create users.
    A super user can create users.
    """

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        is_superuser = graphene.Boolean(required=True)

    user = graphene.Field(UserType)

    @classmethod
    def mutate(cls, root, info, **kwargs):
        user = User()

        create_kwargs = dict(kwargs)

        del create_kwargs['password']

        for key, value in create_kwargs.items():
            setattr(user, key, value)

        user.set_password(kwargs.get('password'))

        user.save()

        return CreateUser(user=user)


class UserMutation(object):
    create_user = CreateUser.Field()


query_list = []
mutation_list = [UserMutation]
