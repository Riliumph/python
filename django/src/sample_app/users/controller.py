import json
import logging

from django.db.utils import IntegrityError
from rest_framework import exceptions, generics, response

from sample_app.users.entity import *
from sample_app.users.repository import UserRepository
from sample_app.users.usecase.interactor.creator import *
from sample_app.users.usecase.interactor.deleter import *
from sample_app.users.usecase.interactor.reader import *
from sample_app.users.usecase.interactor.updater import *

logger = logging.getLogger("app")


class GetUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    '''ユーザーの取得・更新・削除API
    '''
    # GenericApiView member
    serializer_class = UserSerializer
    lookup_field = "user_id"

    def get_queryset(self):
        return UserEntity.objects.all().order_by(self.lookup_field)

    def get(self, request, user_id, *args, **kwargs):
        '''ユーザー情報を取得するAPI
        Djangoに頼れば難の実装も必要ない
        Args:
            request (_type_): _description_

        Returns:
            _type_: _description_
        '''
        # return super().get(request, *args, **kwargs)
        logger.info("controller receive a get user request")
        res = {}
        try:
            interactor = UserReader(UserRepository(UserEntity))
            res = interactor.ReadUserById(user_id)
        except UserEntity.DoesNotExist as e:
            logger.error("not found", extra={"exception": e}, exc_info=True)
            raise exceptions.NotFound
        except Exception as e:
            logger.error(f"unexpected exception",
                         exc_info=True, stack_info=True)
            raise exceptions.APIException
        return response.Response(status=201, data=res)

    def update(self, request, user_id, *args, **kwargs):
        '''ユーザー情報を更新するAPI

        Args:
            request (): 
            user_id (int): パスパラメータで指定されるユーザーID
        '''
        logger.info("view receive a update user request")
        res = {}
        try:
            req_body = json.loads(request.body.decode("utf-8"))
            interactor = UserUpdater(UserRepository(UserEntity))
            res = interactor.UpdateUser(user_id, req_body)
        except exceptions.APIException as e:
            logger.error("rest_framework exception", extra={
                         "exception": e.get_full_details()}, exc_info=True)
            raise e
        except UserEntity.DoesNotExist as e:
            logger.error("not found", extra={"exception": e}, exc_info=True)
            raise exceptions.NotFound
        except Exception as e:
            logger.error(f"unexpected exception",
                         exc_info=True, stack_info=True)
            raise exceptions.APIException
        return response.Response(status=200, data=res)

    def delete(self, request, user_id, **kwargs):
        '''ユーザーを削除するAPI
        Args:
            user_id: url.pyにあるuser_idが入ってくる。
            引数に明示しなければ、kwargsに内包される。
        '''
        logger.info("view receive user delete request")
        try:
            interactor = UserDeleter(UserRepository(UserEntity))
            interactor.DeleteUser(user_id)
        except exceptions.APIException as e:
            logger.error("rest_framework exception", extra={
                         "exception": e.get_full_details()}, exc_info=True)
            raise e
        except UserEntity.DoesNotExist as e:
            logger.error("not found", extra={"exception": e}, exc_info=True)
            raise exceptions.NotFound
        except IntegrityError as e:
            logger.error("user be in in use", extra={
                         "exception": e}, exc_info=True)
            raise e
        except Exception as e:
            logger.error(f"unexpected exception",
                         exc_info=True, stack_info=True)
            raise exceptions.APIException
        return response.Response(status=200)


class GetAllCreate(generics.ListCreateAPIView):
    # GenericApiView member
    serializer_class = UserSerializer
    lookup_field = "user_id"

    def get_queryset(self):
        return UserEntity.objects.all().order_by(self.lookup_field)

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        res = {}
        try:
            req_body = json.loads(request.body.decode("utf-8"))
            interactor = UserCreator(UserRepository(UserEntity))
            res = interactor.CreateUser(req_body)
        except exceptions.APIException as e:
            logger.error("rest_framework exception", extra={
                         "exception": e.get_full_details()}, exc_info=True)
            raise e  # rethrow
        except Exception as e:
            logger.error(f"unexpected exception",
                         exc_info=True, stack_info=True)
            raise exceptions.APIException  # translate unexpected exception into 500
        return response.Response(status=201, data=res)


class BulkDelete(generics.CreateAPIView):
    '''一括削除API
    DestroyAPIはrequest bodyを使えないためCreateAPIを代用する。

    Args:
        generics (_type_): _description_
    '''

    serializer_class = UserSerializer
    lookup_field = "user_id"

    def get_queryset(self):
        return UserEntity.objects.all().order_by(self.lookup_field)

    def post(self, request, *args, **kwargs):
        res = {}
        try:
            req_body = json.loads(request.body.decode("utf-8"))
            interactor = UserDeleter(UserRepository(UserEntity))
            interactor.DeleteUsers(req_body["user_ids"])
        except exceptions.APIException as e:
            logger.error("rest_framework exception", extra={
                         "exception": e.get_full_details()}, exc_info=True)
            raise e  # rethrow
        except IntegrityError as e:
            logger.error("user be in in use", extra={
                         "exception": e}, exc_info=True)
            raise e  # TODO: エラーページに行くので考える
        except Exception as e:
            logger.error(f"unexpected exception",
                         exc_info=True, stack_info=True)
            raise exceptions.APIException  # translate unexpected exception into 500
        return response.Response(status=201, data=res)
