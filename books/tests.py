from django.test import TestCase
from django.urls import reverse
from .models import Book

# Create your tests here.


class BookTests(TestCase):
    def test_no_books(self):
        response = self.client.get("/books/")
        self.assertContains(response, "No books are available.")

    def test_books_list(self):

        Book.objects.create(
            title="Book 1", description="Description 1", isbn="1234567890123"
        )
        Book.objects.create(
            title="Book 2", description="Description 2", isbn="1234567890124"
        )
        Book.objects.create(
            title="Book 3", description="Description 3", isbn="1234567890125"
        )

        response = self.client.get("/books/")
        books = Book.objects.all()

        for book in books:
            self.assertContains(response, book.title)

    def test_book_detail(self):
        book = Book.objects.create(
            title="Book Detail", description="Detail Description", isbn="1234567890126"
        )
        response = self.client.get(reverse("book_detail", kwargs={"pk": book.pk}))

        self.assertContains(response, book.title)
        self.assertContains(response, book.description)
