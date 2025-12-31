from django.shortcuts import render
from django.views import View
from django.db.models import Count, Avg, Q
from books.models import Book, BookReview
from users.models import CustomUser
import random


class LandingPageView(View):
    def get(self, request):
        # Statistika
        total_books = Book.objects.count()
        total_reviews = BookReview.objects.count()
        total_users = CustomUser.objects.count()
        
        # Featured Book (Randomly selected from top rated)
        featured_book = None
        top_candidates = list(Book.objects.annotate(
            avg_rating=Avg('bookreview__stars_given'),
            review_count=Count('bookreview')
        ).filter(avg_rating__gte=4, review_count__gt=0).prefetch_related('bookauthor_set__author')[:10])
        
        if top_candidates:
            featured_book = random.choice(top_candidates)

        # Top rated kitoblar (eng yaxshi baholangan)
        top_rated_books = Book.objects.annotate(
            avg_rating=Avg('bookreview__stars_given'),
            review_count=Count('bookreview')
        ).filter(review_count__gt=0).prefetch_related('bookauthor_set__author').order_by('-avg_rating', '-review_count')[:6]
        
        # Eng ko'p o'qilgan (review bo'yicha)
        most_reviewed_books = Book.objects.annotate(
            review_count=Count('bookreview'),
            avg_rating=Avg('bookreview__stars_given')
        ).filter(review_count__gt=0).prefetch_related('bookauthor_set__author').order_by('-review_count')[:6]
        
        # So'nggi qo'shilgan kitoblar
        new_releases = Book.objects.annotate(
            review_count=Count('bookreview'),
            avg_rating=Avg('bookreview__stars_given')
        ).prefetch_related('bookauthor_set__author').order_by('-id')[:8]
        
        # So'nggi reviewlar
        recent_reviews = BookReview.objects.select_related('book', 'user').order_by('-created_at')[:8]
        
        # Top reviewerlar
        top_reviewers = CustomUser.objects.annotate(
            review_count=Count('bookreview'),
            avg_rating=Avg('bookreview__stars_given')
        ).filter(review_count__gt=0).order_by('-review_count')[:6]
        
        # 5 yulduzli kitoblar
        five_star_books = Book.objects.annotate(
            avg_rating=Avg('bookreview__stars_given'),
            review_count=Count('bookreview')
        ).filter(avg_rating__gte=4.5, review_count__gt=0).order_by('-avg_rating')[:4]
        
        context = {
            'total_books': total_books,
            'total_reviews': total_reviews,
            'total_users': total_users,
            'top_rated_books': top_rated_books,
            'most_reviewed_books': most_reviewed_books,
            'new_releases': new_releases,
            'recent_reviews': recent_reviews,
            'top_reviewers': top_reviewers,
            'five_star_books': five_star_books,
            'featured_book': featured_book,
        }
        return render(request, "index.html", context)
