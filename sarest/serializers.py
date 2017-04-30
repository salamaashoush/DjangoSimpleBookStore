from django.contrib.auth.models import User
from rest_framework import serializers

# Serializers define the API representation.
from rest_framework.exceptions import ValidationError

from sarest.models import Book, Category, Author, Reader


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                header, data = data.split(';base64,')

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            # Generate file name:
            file_name = str(uuid.uuid4())[:12]  # 12 characters are more than enough.
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = "%s.%s" % (file_name, file_extension,)

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension


class ReaderSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    book = serializers.ReadOnlyField(source='book.title')

    class Meta:
        model = Reader
        fields = ('user', 'book', 'value', 'reed')


class BookSerializer(serializers.ModelSerializer):
    cover = Base64ImageField(max_length=None, use_url=False)

    class Meta:
        depth = 1
        model = Book
        fields = ('id', 'title', 'description', 'author', 'publish_date', 'category', 'cover','readers')


class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(allow_blank=False, write_only=True)

    # books = serializers.PrimaryKeyRelatedField(queryset=reader_set.,source='book_set')
    class Meta:
        depth = 1
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'confirm_password', 'is_staff', 'is_superuser',
                  ]
        write_only_fields = ['username', ]
        extra_kwargs = {"password": {"write_only": True},
                        "is_superuser": {"read_only": True}}

    def validate(self, data):
        # Making sure the username always matches the email
        email = data.get('email', None)
        if email:
            data['username'] = email
        return data

    def validate_confirm_password(self, value):
        data = self.get_initial()
        password = data.get('password')
        password_confirm = value
        if password != password_confirm:
            raise ValidationError("Password Must Match")
        return value

    def validate_email(self, value):
        data = self.get_initial()
        email = data.get('email')
        user_qs = User.objects.filter(email=email)
        if user_qs.exists():
            raise ValidationError("This user has already registered")
        return value

    def create(self, validated_data):
        username = validated_data['username']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        email = validated_data['email']
        password = validated_data['password']
        user_obj = User(username=username, first_name=first_name, last_name=last_name, email=email)
        user_obj.set_password(password)
        user_obj.save()
        return validated_data


class CategorySerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)
    subscribers = UserSerializer(read_only=True, many=True)

    class Meta:
        depth = 0
        model = Category
        fields = ('id', 'name', 'description', 'books', 'subscribers')


class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(read_only=True, many=True)
    followers = UserSerializer(read_only=True, many=True)
    image = Base64ImageField(max_length=None, use_url=False)

    class Meta:
        model = Author
        fields = ('id', 'name', 'born_at', 'died_at', 'bio', 'image', 'website', 'followers', 'books')
        extra_kwargs = {
            'books': {"read_only": True},
            'followers': {"read_only": True},
        }
