from django.shortcuts import render, redirect
from django.db.models import Q
from django.views import View
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.core.paginator import Paginator
from books.models import Book, BookReview
from books.forms import BookReviewForm, BookForm
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_object_or_404

# Create your views here.


# class BooklistView(View):
#     def get(self, request):
#         books = Book.objects.all()

#         context = {
#             "books": books,
#         }
#         return render(request, "books/list.html", context)

class BookListView(ListView):
    
    template_name = "books/list.html"
    model = Book
    context_object_name = "books"
    paginate_by = 10
    ordering = ['-id']
    
    def get_queryset(self):
        queryset = Book.objects.all().order_by('-id')
        search = self.request.GET.get('q')
        
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(isbn__icontains=search)
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        return context
    


class BookDetailView(View):
    def get(self, request, pk):
        book = Book.objects.get(pk=pk)
        all_reviews = book.bookreview_set.all().order_by('-created_at')
        
        paginator = Paginator(all_reviews, 10)
        page_number = request.GET.get('page', 1)
        reviews = paginator.get_page(page_number)
        
        review_form = BookReviewForm()
        context = {
            "book": book,
            "reviews": reviews,
            "review_form": review_form,
        }
        return render(request, "books/detail.html", context)
    
class AddBookReviewView(View):
    def post(self, request, pk):
        book = Book.objects.get(pk=pk)
        review_form = BookReviewForm(request.POST)

        if review_form.is_valid():
            book_review = review_form.save(commit=False)
            book_review.user = request.user
            book_review.book = book
            book_review.save()
            messages.success(request, "Your review has been added successfully.")
        else:
            messages.error(request, "There was an error with your review. Please try again.")

        return redirect("book_detail", pk=pk)

# class BookDetailView(DetailView):
#     template_name = "books/detail.html"
#     pk_url_kwarg = "pk"
#     model = Book
    

class AddBookView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request):
        form = BookForm()
        return render(request, 'books/add_book.html', {'form': form})

    def post(self, request):
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book added successfully.')
            return redirect('book_list')
        return render(request, 'books/add_book.html', {'form': form})


class DeleteBookView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser

    def post(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        book.delete()
        messages.success(request, 'Book deleted successfully.')
        return redirect('book_list')


class EditBookReviewView(View):
    def get(self, request, pk):
        review = get_object_or_404(BookReview, pk=pk)
        if request.user != review.user and not request.user.is_superuser:
            messages.error(request, 'You can only edit your own reviews.')
            return redirect('book_detail', pk=review.book.pk)
        form = BookReviewForm(instance=review)
        return render(request, 'books/edit_review.html', {'form': form, 'review': review})

    def post(self, request, pk):
        review = get_object_or_404(BookReview, pk=pk)
        if request.user != review.user and not request.user.is_superuser:
            messages.error(request, 'You can only edit your own reviews.')
            return redirect('book_detail', pk=review.book.pk)
        form = BookReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Review updated successfully.')
            return redirect('book_detail', pk=review.book.pk)
        return render(request, 'books/edit_review.html', {'form': form, 'review': review})


class DeleteBookReviewView(View):
    def post(self, request, pk):
        review = get_object_or_404(BookReview, pk=pk)
        if request.user != review.user and not request.user.is_superuser:
            messages.error(request, 'You can only delete your own reviews.')
            return redirect('book_detail', pk=review.book.pk)
        review.delete()
        messages.success(request, 'Review deleted successfully.')
        return redirect('book_detail', pk=review.book.pk)    
    
