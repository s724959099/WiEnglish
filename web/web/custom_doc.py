from rest_framework.renderers import DocumentationRenderer
from django.template import loader


class MyDocumentationRenderer(DocumentationRenderer):
    template = 'custom_docs/index.html'


api_doc_header = {}


def update_schema(schema):
    return schema
