from rest_framework import serializers
from books.models import Book, BookReview
from users.models import CustomUser


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'description', 'isbn']
    
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class BookReviewSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    book_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = BookReview
        fields = ['id', 'stars_given', 'comment', 'book', 'user', 'book_id']
    
    def create(self, validated_data):
        book_id = validated_data.pop('book_id')
        validated_data['book'] = Book.objects.get(pk=book_id)
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    