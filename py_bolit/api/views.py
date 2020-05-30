from rest_framework import mixins, viewsets
from rest_framework.response import Response
from rest_framework import status

from .models import Node, NodeType
from .serializers import NodeSerializer, NodeTypeSerializer


class NodeTypeListViewSet(mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    queryset = NodeType.objects.all()
    serializer_class = NodeTypeSerializer


class NodeListViewSet(mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    # TODO: Изменить HTML форму
    queryset = Node.objects.all()
    serializer_class = NodeSerializer

    # POST request
    def create(self, request, *args, **kwargs):
        node_type = request.data.get('type')
        # TODO: validate
        queryset = self.queryset
        if type(node_type) is str:
            queryset = queryset.filter(node_type__name=node_type)
        elif type(node_type) is list:
            queryset = queryset.filter(node_type__name__in=node_type)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


# Получить узел по коду или имени
class NodeViewSet(viewsets.GenericViewSet):
    queryset = Node.objects
    serializer_class = NodeSerializer

    # GET request
    def list(self, request, *args, **kwargs):
        params = (dict(request.query_params))
        code = params.get('code')
        name = params.get('name')
        if all([code, name]) or not any([code, name]):
            return Response(status=status.HTTP_404_NOT_FOUND)
        elif code:
            filter = dict(code=code[0])
        elif name:
            filter = dict(name=name[0])

        queryset = self.queryset.filter(**filter).first()
        if queryset:
            serializer = self.get_serializer(queryset, many=False)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    # TODO: POST request

    def create(self, request, *args, **kwargs):
        params = (dict(request.query_params))
        code = params.get('code')
        name = params.get('name')
        if all([code, name]) or not any([code, name]):
            return Response(status=status.HTTP_404_NOT_FOUND)
        elif code:
            filter = dict(code=code[0])
        elif name:
            filter = dict(name=name[0])

        queryset = self.queryset.filter(**filter).first()
        if queryset:
            serializer = self.get_serializer(queryset, many=False)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class PredictViewSet(viewsets.ViewSet):

    # queryset = ''

    def create(self, request, format=None):
        # validate
        # calculate
        # send Response
        return Response(request.data)
