import json
import logging

from rest_framework.exceptions import *
from rest_framework.generics import *
from rest_framework.request import Request
from rest_framework.response import Response

from user_mng_app.entity.model import *
from user_mng_app.entity.validator import *
from user_mng_app.gateway.repository import UserRepository as UserRepo
from user_mng_app.usecase.create.interactor import *
from user_mng_app.usecase.delete.interactor import *
from user_mng_app.usecase.read.interactor import *
from user_mng_app.usecase.update.interactor import *

logger = logging.getLogger("app")


class ListCreate(ListCreateAPIView):
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

    def get(self, request: Request, *args, **kwargs):
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
            req_body = json.loads(request.body.decode("utf-8"))
            user_id = req_body
            data = self.get_serializer(data=user_id)
            interactor = UserCreator(UserRepo(data))
            presenter = interactor.CreateUser(user_id)
        except APIException as e:
            logger.error("rest_framework exception", extra={
                         "exception": e.get_full_details()}, exc_info=True)
            raise e  # rethrow
        except Exception as e:
            logger.error(f"unexpected exception",
                         exc_info=True, stack_info=True)
            raise APIException  # translate unexpected exception into 500
        return Response(status=201, data=presenter.ToJson())
