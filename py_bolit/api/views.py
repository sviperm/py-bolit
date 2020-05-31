from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from .bayes_network import get_model, convert_prediction_to_dict
from .models import Node, NodeType
from .serializers import (NodeCodeRequestSerializer, NodeNameRequestSerializer,
                          NodeSerializer, NodeTypeSerializer)


class NodeTypeListViewSet(mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    queryset = NodeType.objects.all()
    serializer_class = NodeTypeSerializer


class NodeListViewSet(mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    # TODO change HTML form
    queryset = Node.objects.all()
    serializer_class = NodeSerializer

    # TODO GET method

    def create(self, request, *args, **kwargs):
        node_type = request.data.get('type')
        queryset = self.queryset
        if type(node_type) is str:
            queryset = queryset.filter(node_type__name=node_type)
        elif type(node_type) is list:
            queryset = queryset.filter(node_type__name__in=node_type)

        if queryset:
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

        # TODO explain error
        return Response(status=status.HTTP_404_NOT_FOUND)


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
        data = request.data
        model = get_model()
        # TODO error handler
        prediction = model.predict_proba(data)
        result = convert_prediction_to_dict(model, data, prediction)
        return Response(result)
