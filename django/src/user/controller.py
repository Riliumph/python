import json
import logging

from django.db.utils import IntegrityError
from rest_framework import exceptions, generics, request, response

from user.entity.user import *
from user.gateway.user_repository import UserRepository as UserRepo
from user.usecase.interactor.creator import *
from user.usecase.interactor.deleter import *
from user.usecase.interactor.reader import *
from user.usecase.interactor.updater import *

logger = logging.getLogger("app")


class GetUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    '''ユーザーの取得・更新・削除API
    '''
    # GenericApiView member
    serializer_class = UserSerializer
    lookup_field = UserEntity._meta.pk.name

    def get_queryset(self):
        return UserEntity.objects.all().order_by(self.lookup_field)

    def get(self, request: request, user_id, *args, **kwargs):
        '''ユーザー情報を取得するAPI
        Args:
            request (rest_framework.request.Request): 使用しない
            user_id (int): usersテーブルのPK
        '''
        logger.info("controller receive a get user request")
        presenter = None
        try:
            interactor = UserReader(UserRepository(UserEntity))
            presenter = interactor.ReadUserById(user_id)
        except UserEntity.DoesNotExist as e:
            logger.error("not found", extra={"exception": e}, exc_info=True)
            raise exceptions.NotFound
        except Exception as e:
            logger.error(f"unexpected exception",
                         exc_info=True, stack_info=True)
            raise exceptions.APIException
        return response.Response(status=201, data=presenter.ToJson())

    def update(self, request: request, user_id, *args, **kwargs):
        '''ユーザー情報を更新するAPI

        Args:
            request (http): ユーザーの更新用データ
            user_id (int): 対象のユーザーID（パスパラメータで指定）
        '''
        logger.info("controller receive an update user request")
        presenter = None
        try:
            req_body = json.loads(request.body.decode("utf-8"))
            interactor = UserUpdater(UserRepo(UserEntity))
            presenter = interactor.UpdateUser(user_id, req_body)
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
        return response.Response(status=200, data=presenter.ToJson())

    def delete(self, request: request, user_id, **kwargs):
        '''ユーザーを削除するAPI
        Args:
            request (rest_framework.request.Request): 使用しない
            user_id: url.pyにあるuser_idが入ってくる。
            引数に明示しなければ、kwargsに内包される。
        '''
        logger.info("view receive user delete request")
        try:
            interactor = UserDeleter(UserRepo(UserEntity))
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
    '''ユーザーの全取得・作成のAPI
    '''
    serializer_class = UserSerializer
    lookup_field = UserEntity._meta.pk.name

    def get_queryset(self):
        return UserEntity.objects.all().order_by(self.lookup_field)

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


class BulkDelete(generics.CreateAPIView):
    '''一括削除API
    DestroyAPIはrequest bodyを使えないためCreateAPIを代用する。
    '''

    serializer_class = UserSerializer
    lookup_field = "user_id"

    def get_queryset(self):
        return UserEntity.objects.all().order_by(self.lookup_field)

    def post(self, request: request, *args, **kwargs):
        try:
            req_body = json.loads(request.body.decode("utf-8"))
            user_ids = req_body["user_ids"]
            interactor = UserDeleter(UserRepo(UserEntity))
            interactor.DeleteUsers(user_ids)
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
        return response.Response(status=200)
