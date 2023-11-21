import json
import logging

from django.db.utils import IntegrityError
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


class BulkDelete(CreateAPIView):
    '''一括削除API
    DestroyAPIはrequest bodyを使えないためCreateAPIを代用する。
    '''

    serializer_class = UserSerializer
    lookup_field = "user_id"

    def get_queryset(self):
        return User.objects.all().order_by(self.lookup_field)

    def post(self, request: Request, *args, **kwargs):
        try:
            req_body = json.loads(request.body.decode("utf-8"))
            user_ids = req_body["user_ids"]
            interactor = UserDeleter(UserRepo(User()))
            interactor.DeleteUsers(user_ids)
        except APIException as e:
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
            raise APIException  # translate unexpected exception into 500
        return Response(status=200)
