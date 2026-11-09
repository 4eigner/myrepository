import uuid

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from main.models import Experience

User = get_user_model()

PASSWORD = "pass12345"

VALID_PAYLOAD = {
    "title": "New experience",
    "description": "Some description",
    "category": "freelance",
    "started_at": "2026-01-01T00:00:00Z",
}


class ExperienceAPITestBase(APITestCase):
    """Creates the four roles and one experience shared by all tests."""

    def setUp(self):
        self.owner = User.objects.create_superuser("owner", password=PASSWORD)

        self.editor = User.objects.create_user("editor", password=PASSWORD)
        self.editor.user_permissions.add(
            Permission.objects.get(codename="change_experience")
        )

        self.regular = User.objects.create_user("regular", password=PASSWORD)

        self.experience = Experience.objects.create(
            title="Original",
            description="Original description",
            category="volunteer",
            started_at="2026-01-01T00:00:00Z",
        )

        self.list_url = reverse("api:experience-list")
        self.detail_url = reverse(
            "api:experience-detail", kwargs={"experience_id": self.experience.id}
        )
        self.star_url = reverse(
            "api:experience-star", kwargs={"experience_id": self.experience.id}
        )

    def assert_database_unchanged(self, expected_count=1):
        self.assertEqual(Experience.objects.count(), expected_count)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Original")
        self.assertEqual(self.experience.description, "Original description")


class VisitorTests(ExperienceAPITestBase):
    def test_visitor_can_read_list_and_detail(self):
        self.assertEqual(self.client.get(self.list_url).status_code, 200)
        self.assertEqual(self.client.get(self.detail_url).status_code, 200)

    def test_visitor_cannot_create(self):
        response = self.client.post(self.list_url, VALID_PAYLOAD, format="json")
        self.assertEqual(response.status_code, 403)
        self.assert_database_unchanged()

    def test_visitor_cannot_patch(self):
        response = self.client.patch(self.detail_url, {"title": "Hacked"}, format="json")
        self.assertEqual(response.status_code, 403)
        self.assert_database_unchanged()

    def test_visitor_cannot_put(self):
        response = self.client.put(self.detail_url, VALID_PAYLOAD, format="json")
        self.assertEqual(response.status_code, 403)
        self.assert_database_unchanged()

    def test_visitor_cannot_delete(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, 403)
        self.assert_database_unchanged()

    def test_visitor_cannot_star(self):
        response = self.client.post(self.star_url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(self.experience.starred_by.count(), 0)


class RegularUserTests(ExperienceAPITestBase):
    def setUp(self):
        super().setUp()
        self.client.force_login(self.regular)

    def test_regular_user_can_read(self):
        self.assertEqual(self.client.get(self.list_url).status_code, 200)
        self.assertEqual(self.client.get(self.detail_url).status_code, 200)

    def test_regular_user_cannot_create(self):
        response = self.client.post(self.list_url, VALID_PAYLOAD, format="json")
        self.assertEqual(response.status_code, 403)
        self.assert_database_unchanged()

    def test_regular_user_cannot_patch(self):
        response = self.client.patch(self.detail_url, {"title": "Hacked"}, format="json")
        self.assertEqual(response.status_code, 403)
        self.assert_database_unchanged()

    def test_regular_user_cannot_delete(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, 403)
        self.assert_database_unchanged()

    def test_regular_user_can_toggle_star(self):
        response = self.client.post(self.star_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["star_count"], 1)
        self.assertTrue(response.data["is_starred"])
        self.assertTrue(self.experience.starred_by.filter(pk=self.regular.pk).exists())

        response = self.client.post(self.star_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(self.experience.starred_by.count(), 0)

    def test_star_unknown_experience_returns_404(self):
        url = reverse("api:experience-star", kwargs={"experience_id": uuid.uuid4()})
        self.assertEqual(self.client.post(url).status_code, 404)


class EditorTests(ExperienceAPITestBase):
    def setUp(self):
        super().setUp()
        self.client.force_login(self.editor)

    def test_editor_can_patch(self):
        response = self.client.patch(self.detail_url, {"title": "Edited"}, format="json")
        self.assertEqual(response.status_code, 200)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Edited")
        # PATCH only changes the field that was sent
        self.assertEqual(self.experience.description, "Original description")

    def test_editor_can_put(self):
        response = self.client.put(self.detail_url, VALID_PAYLOAD, format="json")
        self.assertEqual(response.status_code, 200)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "New experience")

    def test_editor_cannot_create(self):
        response = self.client.post(self.list_url, VALID_PAYLOAD, format="json")
        self.assertEqual(response.status_code, 403)
        self.assert_database_unchanged()
        self.assertFalse(Experience.objects.filter(title="New experience").exists())

    def test_editor_cannot_delete(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Experience.objects.filter(pk=self.experience.pk).exists())
        self.assert_database_unchanged()

    def test_editor_can_star(self):
        response = self.client.post(self.star_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["star_count"], 1)


class OwnerTests(ExperienceAPITestBase):
    def setUp(self):
        super().setUp()
        self.client.force_login(self.owner)

    def test_owner_can_create(self):
        response = self.client.post(self.list_url, VALID_PAYLOAD, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Experience.objects.filter(title="New experience").exists())
        self.assertEqual(Experience.objects.count(), 2)

    def test_owner_can_patch(self):
        response = self.client.patch(self.detail_url, {"title": "Owner edit"}, format="json")
        self.assertEqual(response.status_code, 200)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Owner edit")

    def test_owner_can_delete(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Experience.objects.filter(pk=self.experience.pk).exists())
        self.assertEqual(self.client.get(self.detail_url).status_code, 404)

    def test_owner_can_star(self):
        response = self.client.post(self.star_url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["is_starred"])


class ValidationTests(ExperienceAPITestBase):
    def setUp(self):
        super().setUp()
        self.client.force_login(self.owner)

    def test_blank_title_returns_400(self):
        payload = {**VALID_PAYLOAD, "title": "   "}
        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("title", response.data)
        self.assertEqual(Experience.objects.count(), 1)

    def test_missing_required_fields_returns_400(self):
        response = self.client.post(self.list_url, {"title": "Only title"}, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("description", response.data)
        self.assertIn("started_at", response.data)
        self.assertEqual(Experience.objects.count(), 1)

    def test_invalid_category_returns_400(self):
        payload = {**VALID_PAYLOAD, "category": "not-a-category"}
        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("category", response.data)

    def test_end_before_start_returns_400(self):
        payload = {**VALID_PAYLOAD, "ended_at": "2025-01-01T00:00:00Z"}
        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("ended_at", response.data)
        self.assertEqual(Experience.objects.count(), 1)

    def test_html_tags_are_stripped_from_text(self):
        payload = {
            **VALID_PAYLOAD,
            "title": "<b>Bold</b> title",
            "description": "<script>alert(1)</script>Safe text",
        }
        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, 201)
        created = Experience.objects.get(pk=response.data["id"])
        self.assertEqual(created.title, "Bold title")
        self.assertNotIn("<", created.description)
        self.assertNotIn(">", created.description)

    def test_patch_with_blank_title_returns_400(self):
        response = self.client.patch(self.detail_url, {"title": "  "}, format="json")
        self.assertEqual(response.status_code, 400)
        self.assert_database_unchanged()

    def test_unknown_experience_returns_404(self):
        url = reverse("api:experience-detail", kwargs={"experience_id": uuid.uuid4()})
        self.assertEqual(self.client.get(url).status_code, 404)
        self.assertEqual(self.client.patch(url, {"title": "x"}, format="json").status_code, 404)
        self.assertEqual(self.client.delete(url).status_code, 404)


class SearchAndSerializerTests(ExperienceAPITestBase):
    def test_search_by_title(self):
        Experience.objects.create(
            title="Other thing", description="x", started_at="2026-02-01T00:00:00Z"
        )
        response = self.client.get(self.list_url, {"title": "Orig"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual([item["title"] for item in response.data], ["Original"])

    def test_search_without_match_returns_empty_list(self):
        response = self.client.get(self.list_url, {"title": "zzzz-no-match"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

    def test_response_contains_star_fields(self):
        self.experience.starred_by.add(self.regular)
        self.client.force_login(self.regular)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.data["star_count"], 1)
        self.assertTrue(response.data["is_starred"])
        self.assertIn("regular", response.data["starred_by_names"])

    def test_is_starred_false_for_visitor(self):
        self.experience.starred_by.add(self.regular)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.data["star_count"], 1)
        self.assertFalse(response.data["is_starred"])

    def test_response_has_no_sensitive_fields(self):
        self.regular.email = "regular@example.com"
        self.regular.save()
        self.experience.starred_by.add(self.regular)
        response = self.client.get(self.detail_url)
        body = str(response.data)
        self.assertNotIn("regular@example.com", body)
        self.assertNotIn("password", body)


class CSRFTests(ExperienceAPITestBase):
    def setUp(self):
        super().setUp()
        self.csrf_client = APIClient(enforce_csrf_checks=True)

    def test_write_without_csrf_token_is_rejected(self):
        self.assertTrue(self.csrf_client.login(username="owner", password=PASSWORD))
        response = self.csrf_client.post(self.list_url, VALID_PAYLOAD, format="json")
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Experience.objects.count(), 1)

    def test_patch_without_csrf_token_is_rejected(self):
        self.assertTrue(self.csrf_client.login(username="editor", password=PASSWORD))
        response = self.csrf_client.patch(self.detail_url, {"title": "Hacked"}, format="json")
        self.assertEqual(response.status_code, 403)
        self.assert_database_unchanged()

    def test_star_without_csrf_token_is_rejected(self):
        self.assertTrue(self.csrf_client.login(username="regular", password=PASSWORD))
        response = self.csrf_client.post(self.star_url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(self.experience.starred_by.count(), 0)