import json

from django.forms.models import model_to_dict

from rest_framework import generics
from rest_framework import exceptions
from rest_framework import response

from sample_app.users.model import *


class UsersGetAllOrPost(generics.ListCreateAPIView):
    # GenericApiView member
    serializer_class = UserSerializer
    lookup_field = "user_id"

    def get_queryset(self):
        return UserModel.objects.all().order_by("user_id")

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
        except KeyError:
            print("not found key in json")
            raise exceptions.ParseError
        except json.JSONDecodeError:
            print("broken json format")
            raise exceptions.ParseError
        except Exception as e:
            print(f"Exception: {e}")
            raise exceptions.APIException
        return response.Response(status=201, data=res_body)
