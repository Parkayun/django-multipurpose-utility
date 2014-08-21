from django.test import TestCase

from dmu import auto_create_objects


class DmuTests(TestCase):
    def test_auto_create_objects(self):
        object_count = 10

        from base.models import SampleModel
        self.assertNotEqual(len(SampleModel.objects.all()), object_count)

        for x in xrange(object_count):
            auto_create_objects(SampleModel)

        self.assertEqual(len(SampleModel.objects.all()), object_count)
