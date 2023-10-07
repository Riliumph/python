import json
import logging

from django.forms.models import model_to_dict

from rest_framework import generics
from rest_framework import exceptions
from rest_framework import response

from sample_app.users.model import *

logger = logging.getLogger("app")

class GetUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    # GenericApiView member
    serializer_class = UserSerializer
    lookup_field = "user_id"

    def get_queryset(self):
        return UserModel.objects.all().order_by(self.lookup_field)

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        # 論理削除を行う
        return response.Response(status=200)


class GetAllCreate(generics.ListCreateAPIView):
    # GenericApiView member
    serializer_class = UserSerializer
    lookup_field = "user_id"

    def get_queryset(self):
        return UserModel.objects.all().order_by(self.lookup_field)

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        res_body = {}
        try:
            req_body = json.loads(request.body.decode("utf-8"))
            s = UserSerializer(data=req_body)
            s.is_valid(raise_exception=True)  # check
            committed = s.save()  # commit to DB
            res_body["users"] = model_to_dict(committed)
        except exceptions.APIException as e:
            logger.error("rest_framework exception", extra={"exception": e.get_full_details()}, exc_info=True)
            raise e # rethrow
        except Exception as e:
            logger.error(f"unexpected exception", exc_info=True, stack_info=True)
            raise exceptions.APIException # translate unexpected exception into 500
        return response.Response(status=201, data=res_body)
