from rest_framework.test import APITestCase
from books.models import Book, BookReview
from users.models import CustomUser

# Create your tests here.

class BookReviewAPITests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="testuser@gmail.com",)
        self.user.set_password("testpassword")
        self.user.save()
    
    def test_book_review_detail(self):
        book = Book.objects.create(
            title="API Testing Book",
            description="A book to test API endpoints.",
            isbn="1234567890123"
        )
        
        review = BookReview.objects.create(
            book=book,
            user=self.user,
            comment="This is a test review.",
            stars_given=4
        )

        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(f"/api/reviews/{review.pk}/")
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["comment"], "This is a test review.")
        self.assertEqual(response.data["stars_given"], 4)
        self.assertEqual(response.data["user"]["id"], self.user.pk)
        self.assertEqual(response.data["book"]["id"], book.pk)

class BookListAPITests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="listuser",
            email="listuser@gmail.com",)
        self.user.set_password("listpassword")
        self.user.save()
    def test_book_review_list(self):
        book1 = Book.objects.create(
            title="List Book 1",
            description="First book for list testing.",
            isbn="1111111111111"
        )
        book2 = Book.objects.create(
            title="List Book 2",
            description="Second book for list testing.",
            isbn="2222222222222"
        )
        
        review1 = BookReview.objects.create(
            book=book1,
            user=self.user,
            comment="First review.",
            stars_given=5
        )
        review2 = BookReview.objects.create(
            book=book2,
            user=self.user,
            comment="Second review.",
            stars_given=3
        )

        self.client.login(username="listuser", password="listpassword")
        response = self.client.get("/api/reviews/")
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 2)
        comments = [review["comment"] for review in response.data["results"]]
        self.assertIn("First review.", comments)
        self.assertIn("Second review.", comments)