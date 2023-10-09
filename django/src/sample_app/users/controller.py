import json
import logging

from django.forms.models import model_to_dict

from rest_framework import (generics,
                            exceptions, response)

from sample_app.users.entity import *
from sample_app.users.usecase import *

logger = logging.getLogger("app")


class GetUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    # GenericApiView member
    serializer_class = UserSerializer
    lookup_field = "user_id"

    def get_queryset(self):
        return UserEntity.objects.all().order_by(self.lookup_field)

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def delete(self, request, user_id, **kwargs):
        '''ユーザーを削除するAPI
        Args:
            user_id: url.pyにあるuser_idが入ってくる。
            引数に明示しなければ、kwargsに内包される。
        '''
        logger.info("view receive a request of user deletion")
        user_data = {"user_id": user_id}
        try:
            interactor = UserDeleteInteractor(UserRepository(UserEntity))
            interactor(user_data)
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
            interactor = UserDeleteInteractor(UserRepository(UserEntity))
            res = interactor(req_body)
        except exceptions.APIException as e:
            logger.error("rest_framework exception", extra={
                         "exception": e.get_full_details()}, exc_info=True)
            raise e  # rethrow
        except Exception as e:
            logger.error(f"unexpected exception",
                         exc_info=True, stack_info=True)
            raise exceptions.APIException  # translate unexpected exception into 500
        return response.Response(status=201, data=res)
