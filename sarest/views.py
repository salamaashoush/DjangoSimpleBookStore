from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import list_route, detail_route
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from sarest.models import Book, Category, Author
from sarest.serializers import UserSerializer, BookSerializer, CategorySerializer, AuthorSerializer, ReaderSerializer


# Create your views here.
# ViewSets define the view behavior.

# class UserViewSet(viewsets.ModelViewSet):
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @list_route(methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        # Everything's valid, so send it to the UserSerializer
        model_serializer = UserSerializer(data=request.data)
        if model_serializer.is_valid():
            model_serializer.save()
            return Response(model_serializer.data)
        return Response(model_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @list_route(methods=['get'])
    def info(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def list(self, request):
        user = request.user
        if not user or not user.is_superuser:
            return HttpResponseForbidden()
        return super(UserViewSet, self).list(request)

    def update(self, request, pk=None):
        user = User.objects.filter(id=pk).first()
        if not user or request.user != user:
            return HttpResponseForbidden()
        return super(UserViewSet, self).update(request)


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @detail_route(methods=['post'])
    def subscribe(self, request, pk=None):
        pass


class AuthorViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    @detail_route(methods=['post'])
    def follow(self, request, pk=None):
        pass


class BookViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    @detail_route(methods=['post'])
    def rate(self, request, pk=None):
        book = self.get_object()
        value = request.data['value']
        data = {"user": request.user.pk, "book": book.pk, "value": value}
        model_serializer = ReaderSerializer(data=data)
        if model_serializer.is_valid():
            model_serializer.save()
            return Response(model_serializer.data, status=status.HTTP_201_CREATED)
        return Response(model_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['post'])
    def read(self, request, pk=None):
        pass

# class UserBooksViewSet(viewsets.ModelViewSet):
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
#     queryset = UserBooks.objects.all()
#     serializer_class = UserBooksSerializer
