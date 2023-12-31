import json
import logging

from django.db.utils import IntegrityError
from rest_framework.exceptions import *
from rest_framework.generics import *
from rest_framework.request import Request
from rest_framework.response import Response

from user_mng_app.entity.model import User
from user_mng_app.entity.validator import *
from user_mng_app.gateway.repository import UserRepository as UserRepo
from user_mng_app.usecase.create.interactor import *
from user_mng_app.usecase.delete.interactor import *
from user_mng_app.usecase.read.interactor import *
from user_mng_app.usecase.update.interactor import *

logger = logging.getLogger("app")


class GetUpdateDestroy(RetrieveUpdateDestroyAPIView):
    '''ユーザーの取得・更新・削除API
        なぜかテキストボックスに表示されない
    '''
    # GenericApiView member
    serializer_class = UserSerializer
    lookup_field = User._meta.pk.name

    def get_queryset(self):
        return User.objects.all().order_by(self.lookup_field)

    def get(self, request: Request, user_id, *args, **kwargs):
        '''ユーザー情報を取得するAPI
        Args:
            request (rest_framework.request.Request): 使用しない
            user_id (int): usersテーブルのPK
        '''
        logger.info("controller receive a get user request")
        presenter = None
        try:
            interactor = UserReader(UserRepo(User()))
            presenter = interactor.ReadUserById(user_id)
        except User.DoesNotExist as e:
            logger.error("not found", extra={"exception": e}, exc_info=True)
            raise NotFound
        except Exception as e:
            logger.error(f"unexpected exception",
                         exc_info=True, stack_info=True)
            raise APIException
        return Response(status=200, data=presenter.ToJson())

    def update(self, request: Request, user_id, *args, **kwargs):
        '''ユーザー情報を更新するAPI

        Args:
            request (http): ユーザーの更新用データ
            user_id (int): 対象のユーザーID（パスパラメータで指定）
        '''
        logger.info("controller receive an update user request")
        presenter = None
        try:
            req_body = request.body.decode("utf-8")
            req_body = json.loads(req_body)
            interactor = UserUpdater(UserRepo(User()))
            presenter = interactor.UpdateUser(user_id, req_body)
        except APIException as e:
            logger.error("rest_framework exception", extra={
                         "exception": e.get_full_details()}, exc_info=True)
            raise e
        except User.DoesNotExist as e:
            logger.error("not found", extra={"exception": e}, exc_info=True)
            raise NotFound
        except Exception as e:
            logger.error(f"unexpected exception",
                         exc_info=True, stack_info=True)
            raise APIException
        return Response(status=200, data=presenter.ToJson())

    def delete(self, request: Request, user_id, **kwargs):
        '''ユーザーを削除するAPI
        Args:
            request (rest_framework.request.Request): 使用しない
            user_id: url.pyにあるuser_idが入ってくる。
            引数に明示しなければ、kwargsに内包される。
        '''
        logger.info("view receive user delete request")
        try:
            interactor = UserDeleter(UserRepo(User()))
            interactor.DeleteUser(user_id)
        except APIException as e:
            logger.error("rest_framework exception", extra={
                         "exception": e.get_full_details()}, exc_info=True)
            raise e
        except User.DoesNotExist as e:
            logger.error("not found", extra={"exception": e}, exc_info=True)
            raise NotFound
        except IntegrityError as e:
            logger.error("user be in in use", extra={
                         "exception": e}, exc_info=True)
            raise e
        except Exception as e:
            logger.error(f"unexpected exception",
                         exc_info=True, stack_info=True)
            raise APIException
        return Response(status=200)
