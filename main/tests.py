import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from main.models import Education, Experience


def aware(year, month, day):
    """Timezone-aware datetime, avoids the naive datetime warnings."""
    return timezone.make_aware(datetime.datetime(year, month, day))


class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP",
            description="Membantu mahasiswa memahami pengembangan web.",
            category="part-time",
            started_at=aware(2026, 1, 1),
            ended_at=aware(2026, 6, 30),
        )

        self.education = Education.objects.create(
            degree="Undergraduate",
            institution="Universitas Indonesia",
            description="Learning about information systems in businesses",
            field_of_study="Information Systems",
            start_year=2025,
            end_year=None,
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(response, self.experience.title)
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")

        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        ongoing = Experience.objects.create(
            title="Ongoing",
            description="x",
            started_at=aware(2026, 1, 1),
        )

        self.assertEqual(str(self.experience), "Asisten Dosen PBP")
        self.assertEqual(self.experience.category, "part-time")
        self.assertFalse(self.experience.is_ongoing)
        self.assertTrue(ongoing.is_ongoing)

    def test_experience_page(self):
        # The page itself only renders the empty containers; JavaScript
        # fills the cards from the API, so the data is checked via the API.
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, 'id="grid"')
        self.assertContains(response, 'id="experience-search-form"')
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

        api_response = self.client.get(reverse("api:experience-list"))
        self.assertEqual(api_response.status_code, 200)
        self.assertContains(api_response, self.experience.title)
        self.assertContains(api_response, self.experience.description)
        self.assertEqual(api_response.data[0]["category"], "part-time")

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, "Belum ada pengalaman yang ditambahkan atau ditemukan."
        )

        api_response = self.client.get(reverse("api:experience-list"))
        self.assertEqual(api_response.data, [])

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()

        self.assertFalse(self.experience.is_ongoing)

        api_response = self.client.get(reverse("api:experience-list"))
        item = api_response.data[0]
        self.assertIsNotNone(item["ended_at"])
        self.assertFalse(item["is_ongoing"])

    def test_ongoing_experience(self):
        self.experience.ended_at = None
        self.experience.save()

        self.assertTrue(self.experience.is_ongoing)

        api_response = self.client.get(reverse("api:experience-list"))
        item = api_response.data[0]
        self.assertIsNone(item["ended_at"])
        self.assertTrue(item["is_ongoing"])

    def test_education_url_is_accessible(self):
        response = self.client.get(reverse("main:show_education"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "education.html")

    def test_education_page(self):
        response = self.client.get(reverse("main:show_education"))

        self.assertContains(response, self.education.institution)
        self.assertContains(response, self.education.degree)

    def test_empty_education_page(self):
        Education.objects.all().delete()
        response = self.client.get(reverse("main:show_education"))

        self.assertContains(response, "Belum ada riwayat pendidikan")