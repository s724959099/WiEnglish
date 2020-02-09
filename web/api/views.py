from rest_framework import viewsets
from functools import partial
from functools import wraps
from django.db import transaction
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.mixins import \
    (CreateModelMixin, ListModelMixin, DestroyModelMixin, RetrieveModelMixin)
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_nested import routers
from rest_framework.parsers import MultiPartParser, FormParser
from . import permissions
from . import serializers
# todo 之後要加入回來
from rest_framework.permissions import IsAuthenticated
from .viewlib import (List2RetrieveMixin, NestedViewSetBase)
from collections import OrderedDict
import datetime
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from django.http import QueryDict
from django.db.models import Q
from rest_framework.compat import coreapi, coreschema, distinct
from rest_framework import exceptions
from rest_framework.pagination import LimitOffsetPagination
import datetime
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from django.http import HttpResponseRedirect
from . import docs
from . import filters
from django.db.models import Prefetch
from . import permissions
import json

router = routers.DefaultRouter()
nested_routers = []
orderdct = OrderedDict()


class UpdateModelMixin:
    """
    客製化Update 不要有partial_update
    """

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()


class MyMixin(CreateModelMixin, UpdateModelMixin, ListModelMixin, RetrieveModelMixin, DestroyModelMixin,
              viewsets.GenericViewSet):
    pass


def router_url(url, prefix=None, *args, **kwargs):
    def decorator(cls):
        if not prefix:
            router.register(url, cls, *args, **kwargs)
        else:
            prefix_router = orderdct.get(prefix, router)
            nested_router = routers.NestedDefaultRouter(prefix_router, prefix, lookup=prefix)
            nested_router.register(url, cls, *args, **kwargs)
            orderdct[url] = nested_router
            nested_routers.append(nested_router)

        @wraps(cls)
        def warp(*args, **kwargs):
            return cls(*args, **kwargs)

        return warp

    return decorator


def get_urls():
    urls = router.get_urls()
    for nested_router in nested_routers:
        urls += nested_router.get_urls()
    return urls
