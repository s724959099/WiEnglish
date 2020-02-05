import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.settings')
django.setup()
from django.contrib.auth.models import User
from api import serializers
from django.utils import timezone
import datetime
import random

fmt = '%Y-%m-%d %H:%M:%S'


def main():
    pass


if __name__ == '__main__':
    main()
