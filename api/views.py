from django.shortcuts import render
from django.http import JsonResponse
from books.models import BookReview


from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from .serializers import BookReviewSerializer

# Create your views here.

class BookReviewDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request,pk):
        book_review = BookReview.objects.get(pk=pk)
        
        # json_response = {
        #     "id": book_review.id,
        #     "stars_given": book_review.stars_given,
        #     "comment": book_review.comment,
            
        #     "book": {
        #         "id": book_review.book.id,
        #         "title": book_review.book.title,
        #         "description": book_review.book.description,
        #         "isbn": book_review.book.isbn,
        #     },
            
        #     "user": {
        #         "id": book_review.user.id,
        #         "username": book_review.user.username,
        #         "email": book_review.user.email,
        #     }
        # }
        # return JsonResponse(json_response)
        
        
        serializer = BookReviewSerializer(book_review)
        return Response(data=serializer.data)
    
    
class BookReviewListAPIView(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        book_reviews = BookReview.objects.all()
        
        paginator = PageNumberPagination()
        page_obj = paginator.paginate_queryset(book_reviews,request)
        serializer = BookReviewSerializer(page_obj,many=True)
        
        return paginator.get_paginated_response(serializer.data)
    
    
