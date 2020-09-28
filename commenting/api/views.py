from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from commenting.api.serializers import CommentingSerializer
from commenting.models import ProductComment


class CommetingVewsSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = CommentingSerializer
    queryset = ProductComment.approves.all()

    def list(self, request, *args, **kwargs):
        product_id = request.query_params.get('product')
        if product_id:
            try:
                product_id = int(product_id)
            except ValueError:
                pass
            else:
                related_comments = ProductComment.approves.filter(product_id=product_id)
                serializer = self.get_serializer(related_comments, many=True)
                return Response(serializer.data)
        return super().list(request, *args, **kwargs)
