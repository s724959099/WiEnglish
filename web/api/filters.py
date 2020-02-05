from django.db.models import Q
from rest_framework import filters
from rest_framework.compat import coreapi, coreschema
from django.utils import timezone

or_q = lambda q, other_fn: other_fn if q is None else q | other_fn
and_q = lambda q, other_fn: other_fn if q is None else q & other_fn
