from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Book, Rating
from django.core.files.uploadedfile import SimpleUploadedFile


class RatingFlowTests(TestCase):
	def setUp(self):
		# create a test user
		self.username = 'tester'
		self.password = 'pass12345'
		self.user = User.objects.create_user(username=self.username, password=self.password)

		# create a minimal book (file field requires a file-like object)
		img = SimpleUploadedFile('test.jpg', b'filecontent', content_type='image/jpeg')
		self.book = Book.objects.create(name='Test Book', web='http://example.com', price='9.99', picture=img)

		self.client = Client()

	def test_user_can_submit_rating_and_average_updates(self):
		# login
		logged = self.client.login(username=self.username, password=self.password)
		self.assertTrue(logged)

		# post a rating of 4
		url = reverse('book_rating', args=[self.book.id])
		response = self.client.post(url, {'value': 4}, follow=True)
		self.assertEqual(response.status_code, 200)

		# rating saved
		rating_qs = Rating.objects.filter(book=self.book, user=self.user)
		self.assertTrue(rating_qs.exists())
		self.assertEqual(rating_qs.first().value, 4)

		# post another rating as a different user to change average
		other = User.objects.create_user(username='other', password='pw')
		self.client.logout()
		self.client.login(username='other', password='pw')
		self.client.post(url, {'value': 2}, follow=True)

		# compute average from DB
		ratings = list(Rating.objects.filter(book=self.book).values_list('value', flat=True))
		avg = sum(ratings) / len(ratings)

		# fetch annotated book
		from django.db.models import Avg
		annotated = Book.objects.filter(id=self.book.id).annotate(avg_rating=Avg('rating__value')).first()
		self.assertIsNotNone(annotated.avg_rating)
		self.assertAlmostEqual(float(annotated.avg_rating), avg)
