from django.test import TestCase
from .. import rating_builder, models


class PersonRatingBuilderTestCase(TestCase):
    fixtures = [
        'snapshots'
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
        for person, params in zip(result.objects, self.expected_rating):
            self.assertEqual(params[0], person.scopussnapshot_h_index)
            self.assertEqual(params[1], person.scopussnapshot_documents)
            self.assertEqual(params[2], person.scopussnapshot_citations)

    def test_pagination(self):
        self.builder.set_pagination(rating_builder.Pagination(1, 3))
        result = self.builder.build()

        self.assertEqual(1, result.page)
        self.assertEqual(3, result.limit)
        self.assertEqual(9, result.total)

        for person, params in zip(result.objects, self.expected_rating):
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
        for person, params in zip(result.objects, expected_rating):
            self.assertEqual(params[1], person.scopussnapshot_documents)


class FacultyRatingBuilderTestCase(TestCase):
    fixtures = [
        'snapshots'
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
        for faculty, params in zip(result.objects, self.expected_rating):
            self.assertEqual(params[0], faculty.scopussnapshot_h_index)
            self.assertEqual(params[1], faculty.scopussnapshot_documents)
            self.assertEqual(params[2], faculty.scopussnapshot_citations)


class DepartmentRatingBuilderTestCase(TestCase):
    fixtures = [
        'snapshots'
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
        for department, params in zip(result.objects, self.expected_rating):
            self.assertEqual(params[0], department.scopussnapshot_h_index)
            self.assertEqual(params[1], department.scopussnapshot_documents)
            self.assertEqual(params[2], department.scopussnapshot_citations)
