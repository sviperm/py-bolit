from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from .bayes_network import BayesNetwork
from .models import Node, NodeType
from .serializers import (NodeCodeRequestSerializer, NodeNameRequestSerializer,
                          NodeSerializer, NodeTypeSerializer)


class NodeTypeListViewSet(mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    queryset = NodeType.objects.all()
    serializer_class = NodeTypeSerializer


class NodeListViewSet(viewsets.ViewSet):
    # TODO change HTML form
    queryset = Node.objects.all()
    serializer = NodeSerializer

    @classmethod
    def get_response(cls, data):
        node_type = data.get('type')
        queryset = cls.queryset
        if type(node_type) is str:
            queryset = queryset.filter(type__name=node_type)
        elif type(node_type) is list:
            queryset = queryset.filter(type__name__in=node_type)

        if queryset:
            serializer = cls.serializer(queryset, many=True)
            return Response(serializer.data)

        # TODO explain error
        return Response(status=status.HTTP_404_NOT_FOUND)

    def list(self, request, *args, **kwargs):
        data = {key: ''.join(value) for key, value in request.query_params.items()}
        return self.get_response(data)

    def create(self, request, *args, **kwargs):
        data = request.data
        return self.get_response(data)


class NodeViewSet(viewsets.ViewSet):
    queryset = Node.objects
    serializer = NodeSerializer
    code_serializer = NodeCodeRequestSerializer
    name_serializer = NodeNameRequestSerializer

    @classmethod
    def get_response(cls, data):
        is_code = cls.code_serializer(data=data).is_valid()
        is_name = cls.name_serializer(data=data).is_valid()
        if (is_code and is_name) or not (is_code or is_name):
            # TODO explain error
            return Response(status=status.HTTP_404_NOT_FOUND)
        elif is_code:
            filter = {"code": data['code']}
        elif is_name:
            filter = {"name": data['name']}

        queryset = cls.queryset.filter(**filter).first()
        if queryset:
            serializer = cls.serializer(queryset, many=False)
            return Response(serializer.data)

        return Response(status=status.HTTP_404_NOT_FOUND)

    def list(self, request, *args, **kwargs):
        data = {key: ''.join(value) for key, value in request.query_params.items()}
        return self.get_response(data)

    def create(self, request, *args, **kwargs):
        data = request.data
        return self.get_response(data)


class PredictViewSet(viewsets.ViewSet):
    def create(self, request, format=None):
        # TODO validate request.data
        model = BayesNetwork()
        # TODO error handler
        prediction = model.predict(request.data)
        return Response(prediction)
