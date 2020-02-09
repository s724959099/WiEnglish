import os
import django

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.settings')
django.setup()
from api import models
from crawler.crawler import Crawler
from api import models

cralwer = Crawler(models)
cralwer.run()
