from django.test import TestCase
from Main.models import ImageBloodTest

class ModelTest(TestCase):

    def create_some_data(self, information="Hi sir", image_path='Downloads/IMG_20230705_183301_870.jpg'):
        return ImageBloodTest.objects.create(information=information, image=image_path)

    def test_ImageBloodTest_creation(self):
        blood_test = self.create_some_data()
        self.assertTrue(isinstance(blood_test, ImageBloodTest))
        self.assertEqual(blood_test.__unicode__(), blood_test.information)


