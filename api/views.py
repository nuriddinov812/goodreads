# from django.shortcuts import render
# from django.http import JsonResponse
from books.models import BookReview


# from rest_framework.response import Response
# from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
# from rest_framework.pagination import PageNumberPagination
# from rest_framework import status
from rest_framework import generics,viewsets
from .serializers import BookReviewSerializer

# Create your views here.
# All in one using ModelViewSet
class BookReviewViewSet(viewsets.ModelViewSet):
    queryset = BookReview.objects.all().order_by('-created_at')
    serializer_class = BookReviewSerializer
    lookup_field = 'pk'
    permission_classes = [IsAuthenticated]





# # class BookReviewDetailAPIView(APIView):
# class BookReviewDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = BookReview.objects.all()
#     serializer_class = BookReviewSerializer
#     lookup_field = 'pk'
#     permission_classes = [IsAuthenticated]
    
#     # def get(self,request,pk):
#     #     book_review = BookReview.objects.get(pk=pk)
        
#     #     # json_response = {
#     #     #     "id": book_review.id,
#     #     #     "stars_given": book_review.stars_given,
#     #     #     "comment": book_review.comment,
            
#     #     #     "book": {
#     #     #         "id": book_review.book.id,
#     #     #         "title": book_review.book.title,
#     #     #         "description": book_review.book.description,
#     #     #         "isbn": book_review.book.isbn,
#     #     #     },
            
#     #     #     "user": {
#     #     #         "id": book_review.user.id,
#     #     #         "username": book_review.user.username,
#     #     #         "email": book_review.user.email,
#     #     #     }
#     #     # }
#     #     # return JsonResponse(json_response)
        
        
#     #     serializer = BookReviewSerializer(book_review)
#     #     return Response(data=serializer.data)
    
    
#     # def delete(self,request,pk):
#     #     book_review = BookReview.objects.get(pk=pk)
#     #     book_review.delete()
        
#     #     return Response(status=status.HTTP_204_NO_CONTENT)
    
    
#     # def put(self,request,pk):
#     #     book_review = BookReview.objects.get(pk=pk)
        
#     #     serializer = BookReviewSerializer(instance=book_review,data=request.data)
        
#     #     if serializer.is_valid():
#     #         serializer.save()
#     #         return Response(data=serializer.data,status=status.HTTP_200_OK)
#     #     else:
#     #         return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
        
#     # def patch(self,request,pk):
#     #     book_review = BookReview.objects.get(pk=pk)
        
#     #     serializer = BookReviewSerializer(instance=book_review,data=request.data,partial=True)
        
#     #     if serializer.is_valid():
#     #         serializer.save()
#     #         return Response(data=serializer.data,status=status.HTTP_200_OK)
#     #     else:
#     #         return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    
    
# # class BookReviewListAPIView(APIView):
# class BookReviewListAPIView(generics.ListCreateAPIView):
#     serializer_class = BookReviewSerializer
#     queryset = BookReview.objects.all().order_by('created_at')
#     permission_classes = [IsAuthenticated]
    
#     # def get(self,request):
#     #     book_reviews = BookReview.objects.all()
        
#     #     paginator = PageNumberPagination()
#     #     page_obj = paginator.paginate_queryset(book_reviews,request)
#     #     serializer = BookReviewSerializer(page_obj,many=True)
        
#     #     return paginator.get_paginated_response(serializer.data)
    
#     # def post(self,request):
#     #     serializer = BookReviewSerializer(data=request.data, context={'request': request})
        
#     #     if serializer.is_valid():
#     #         serializer.save()
#     #         return Response(data=serializer.data,status=status.HTTP_201_CREATED)
#     #     else:
#     #         return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    
