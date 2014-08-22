from django.test import TestCase

from dmu import AutoCreator


class DmuTests(TestCase):
    def test_auto_creator(self):
        object_count = 10

        from base.models import SampleModel
        self.assertNotEqual(len(SampleModel.objects.all()), object_count)

        for x in xrange(object_count):
            AutoCreator().run(SampleModel)

        self.assertEqual(len(SampleModel.objects.all()), object_count)
