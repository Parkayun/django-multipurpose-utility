from django.test import TestCase

from dmu import auto_create_objects


class DmuTests(TestCase):
    def test_auto_create_objects(self):
        to_make_model_count = 10
    
        from base.models import SampleModel
        self.assertEqual(len(SampleModel.objects.all()), 0)

        for x in xrange(to_make_model_count):
            auto_create_objects(SampleModel)

        self.assertEqual(len(SampleModel.objects.all()), 10)
