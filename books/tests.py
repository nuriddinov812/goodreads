from django.test import TestCase
from django.urls import reverse
from .models import Book
from users.models import CustomUser

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

    def test_pagination_is_ten(self):
        for i in range(15):
            Book.objects.create(
                title=f"Book {i+1}",
                description=f"Description {i+1}",
                isbn=f"12345678901{i+1:02d}",
            )

        response = self.client.get("/books/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEqual(len(response.context["books"]), 10)
        
        
        
    def test_search_books(self):
        Book.objects.create(
            title="Django for Beginners",
            description="A comprehensive guide to Django.",
            isbn="1111111111111",
        )
        Book.objects.create(
            title="Learning Python",
            description="An in-depth look at Python programming.",
            isbn="2222222222222",
        )
        Book.objects.create(
            title="Advanced Django",
            description="Take your Django skills to the next level.",
            isbn="3333333333333",
        )

        response = self.client.get("/books/?q=Django")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Django for Beginners")
        self.assertContains(response, "Advanced Django")
        self.assertNotContains(response, "Learning Python")
        
        
class BookReviewTests(TestCase):
    def test_add_book_review(self):
        user = CustomUser.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.client.login(username="testuser", password="testpass123")
        
        book = Book.objects.create(
            title="Test Book", description="Test Description", isbn="1234567890127"
        )
        response = self.client.post(
            reverse("add_book_review", kwargs={"pk": book.pk}),
            data={
                "comment": "Great book!",
                "stars_given": 5,
            },
        )

        self.assertEqual(response.status_code, 302)  # Should redirect after saving
        self.assertTrue(book.bookreview_set.filter(comment="Great book!", user=user).exists())



class LandingPageTests(TestCase):
    def test_landing_page_statistics(self):
        response = self.client.get(reverse("landing_page"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("total_books", response.context)
        self.assertIn("total_reviews", response.context)
        self.assertIn("total_users", response.context)
        self.assertIn("top_rated_books", response.context)
        self.assertIn("most_reviewed_books", response.context)
        self.assertIn("new_releases", response.context)
        self.assertIn("recent_reviews", response.context)
        self.assertIn("top_reviewers", response.context)
        self.assertIn("five_star_books", response.context)   
        
    def test_featured_book_in_context(self):
        response = self.client.get(reverse("landing_page"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("featured_book", response.context)
        self.assertIsNone(response.context["featured_book"])  # No books yet

    def test_featured_book_selection(self):
        # Create books with high ratings to be candidates for featured book
        for i in range(15):
            book = Book.objects.create(
                title=f"Top Book {i+1}",
                description="Highly rated book",
                isbn=f"99999999999{i+1:02d}",
            )
            for j in range(5):
                book.bookreview_set.create(
                    user=CustomUser.objects.create_user(
                        username=f"user{i}{j}", email=f"user{i}{j}@example.com", password="testpass123"
                    ),
                    comment="Great book!",
                    stars_given=5,
                )   
        response = self.client.get(reverse("landing_page"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("featured_book", response.context)
        self.assertIsNotNone(response.context["featured_book"])  # Featured book should be selected now             