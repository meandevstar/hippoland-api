from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from products.models import Product
from products.serializers import ProductSerializer


class ProductListCreateAPIView(RetrieveAPIView):
    serializer_class = ProductSerializer

    def retrieve(self, request, *args, **kwargs):
        limit = self.request.query_params.get("limit", 10)
        page_no = int(self.request.query_params.get("pageNo", 0)) + 1
        order = self.request.query_params.get("order")
        order_by = self.request.query_params.get("orderBy")

        products = Product.objects.all()

        if order is not None and order_by is not None:
            products = products.order_by(order_by)

            if order == "desc":
                products = products.reverse()


        paginator = Paginator(products, limit)
        try:
            data = paginator.page(page_no)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)

        serialized = []
        for v in data:
            serialized.append(ProductSerializer(v).data)

        result = {
            "data": serialized,
            "total": products.count()
        }
        return Response(data=result, status=status.HTTP_200_OK)


class ProductDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = []


