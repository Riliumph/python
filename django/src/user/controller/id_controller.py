import json
import logging

from django.db.utils import IntegrityError
from rest_framework import exceptions, generics, request, response

from user.entity.model import *
from user.entity.validator import *
from user.gateway.repository import UserRepository as UserRepo
from user.usecase.creator.interactor import *
from user.usecase.deleter.interactor import *
from user.usecase.reader.interactor import *
from user.usecase.updater.interactor import *

logger = logging.getLogger("app")


class GetAllCreate(generics.ListCreateAPIView):
    '''ユーザーの全取得・作成のAPI
    '''
    serializer_class = UserSerializer
    lookup_field = User._meta.pk.name

    def get_queryset(self):
        return User.objects.all().order_by(self.lookup_field)

    def get_serializer(self, *args, **kwargs):
        # []ではkeyError例外が発生するため、例外発生しないget()を使う
        if isinstance(kwargs.get('data'), list):
            kwargs['many'] = True
        return super().get_serializer(*args, **kwargs)

    def get(self, request: request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        '''ユーザーを作成するAPI
        単複両方が同じURL（users#POST）であるため、仮にフロントエンドを単一用のデータを作成するように作ったとしても、
        ユーザーにPOST前のrequest bodyをハックされれば、膨大なユーザーを作成させられる攻撃が成立するAPIになっている。
        本番では必ずそれぞれのURLを用意して別APIとし、controllerにてユーザーの権限チェックを行う方がよい。

        Args:
            request (rest_framework.request.Request): Body部に作成するユーザー情報を格納する
        '''
        presenter = None
        try:
            logger.info(type(request))
            req_body = json.loads(request.body.decode("utf-8"))
            user_id = req_body
            interactor = UserCreator(
                UserRepo(self.get_serializer(data=user_id)))
            presenter = interactor.CreateUser(user_id)
        except exceptions.APIException as e:
            logger.error("rest_framework exception", extra={
                         "exception": e.get_full_details()}, exc_info=True)
            raise e  # rethrow
        except Exception as e:
            logger.error(f"unexpected exception",
                         exc_info=True, stack_info=True)
            raise exceptions.APIException  # translate unexpected exception into 500
        return response.Response(status=201, data=presenter.ToJson())
