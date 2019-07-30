import os
from django.conf import settings
from django.test import TestCase
from .. import rating_builder, models


class PersonRatingBuilderTestCase(TestCase):
    fixtures = [
        os.path.join(settings.BASE_DIR, 'core/tests/fixtures/snapshots.json')
    ]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.expected_rating = [
            # h-index documents citations
            (10, 4, 30),
            (8, 5, 12),
            (7, 7, 20),
            (5, 5, 12),
            (5, 4, 45),
            (3, 2, 100),
            (2, 10, 122),
            (0, 2034, 456),
            (0, 78, 20)
        ]

    def setUp(self):
        self.builder = rating_builder.PersonRatingBuilder(models.ScopusSnapshot.get_options()) \
            .set_revision(1) \
            .set_university(1)

    def test_default_ordering(self):
        result = self.builder.build()
        self.assertEqual(9, len(result.objects))
        for person, params in zip(result.objects, self.expected_rating):
            self.assertEqual(params[0], person.scopussnapshot_h_index)
            self.assertEqual(params[1], person.scopussnapshot_documents)
            self.assertEqual(params[2], person.scopussnapshot_citations)

    def test_pagination(self):
        for pagination in (rating_builder.Pagination(1, 3), rating_builder.Pagination(2, 3)):

            self.builder.set_pagination(pagination)
            result = self.builder.build()

            self.assertEqual(pagination.limit, len(result.objects))
            self.assertEqual(pagination.page, result.page)
            self.assertEqual(pagination.limit, result.limit)
            self.assertEqual(9, result.total)

            left, _ = pagination.range

            for person, params in zip(result.objects, self.expected_rating[left:]):
                self.assertEqual(params[0], person.scopussnapshot_h_index)
                self.assertEqual(params[1], person.scopussnapshot_documents)
                self.assertEqual(params[2], person.scopussnapshot_citations)

        self.builder.set_pagination(rating_builder.Pagination(2, 9))
        with self.assertRaises(rating_builder.PageDoesNotExist):
            self.builder.build()

    def test_custom_ordering(self):
        expected_rating = sorted(self.expected_rating, key=lambda item: item[1], reverse=True)
        self.builder.set_ordering(('-documents',))
        result = self.builder.build()
        self.assertEqual(9, len(result.objects))
        for person, params in zip(result.objects, expected_rating):
            self.assertEqual(params[1], person.scopussnapshot_documents)

    def test_person_types(self):
        self.builder.set_person_types([2])
        result = self.builder.build()
        self.assertEqual(2, len(result.objects))
        expected_rating = [
            # h-index documents citations
            (3, 2, 100),
            (2, 10, 122)
        ]
        for person, params in zip(result.objects, expected_rating):
            self.assertEqual(params[0], person.scopussnapshot_h_index)
            self.assertEqual(params[1], person.scopussnapshot_documents)
            self.assertEqual(params[2], person.scopussnapshot_citations)

    def test_search(self):
        self.builder.set_term('P')
        result = self.builder.build()
        self.assertEqual(9, len(result.objects))
        for person, params in zip(result.objects, self.expected_rating):
            self.assertEqual(params[0], person.scopussnapshot_h_index)
            self.assertEqual(params[1], person.scopussnapshot_documents)
            self.assertEqual(params[2], person.scopussnapshot_citations)

        self.builder.set_term('P10')
        result = self.builder.build()
        self.assertEqual(1, len(result.objects))
        person = result.objects[0]
        self.assertEqual(5, person.scopussnapshot_h_index)
        self.assertEqual(5, person.scopussnapshot_documents)
        self.assertEqual(12, person.scopussnapshot_citations)


class FacultyRatingBuilderTestCase(TestCase):
    fixtures = [
        os.path.join(settings.BASE_DIR, 'core/tests/fixtures/snapshots.json')
    ]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.expected_rating = [
            # h-index documents citations
            (10, 7, 30),
            (8, 2034, 456),
            (5, 10, 122)
        ]

    def setUp(self):
        self.builder = rating_builder.FacultyRatingBuilder(models.ScopusSnapshot.get_options()) \
            .set_revision(1) \
            .set_university(1)

    def test_default_ordering(self):
        result = self.builder.build()
        self.assertEqual(3, len(result.objects))
        for faculty, params in zip(result.objects, self.expected_rating):
            self.assertEqual(params[0], faculty.scopussnapshot_h_index)
            self.assertEqual(params[1], faculty.scopussnapshot_documents)
            self.assertEqual(params[2], faculty.scopussnapshot_citations)


class DepartmentRatingBuilderTestCase(TestCase):
    fixtures = [
        os.path.join(settings.BASE_DIR, 'core/tests/fixtures/snapshots.json')
    ]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.expected_rating = [
            # h-index documents citations
            (5, 4, 45),
            (3, 2, 100),
            (2, 10, 122)
        ]

    def setUp(self):
        self.builder = rating_builder.DepartmentRatingBuilder(models.ScopusSnapshot.get_options()) \
            .set_revision(1) \
            .set_faculty(1)

    def test_default_ordering(self):
        result = self.builder.build()
        self.assertEqual(3, len(result.objects))
        for department, params in zip(result.objects, self.expected_rating):
            self.assertEqual(params[0], department.scopussnapshot_h_index)
            self.assertEqual(params[1], department.scopussnapshot_documents)
            self.assertEqual(params[2], department.scopussnapshot_citations)
