from django.test import TestCase
from .models import Neighbourhood,Profile,Business,Post
from django.contrib.auth.models import User


# Create your tests here.
class TestProfile(TestCase):
    def setUp(self):
        self.user = User(username='betty',
                         email='betty@gmail.com', password='3ryt5')
        self.user.save()

        self.neighbourhood = Neigbourhood(
            name='Covid', description='Room of Dawn', police_number=99, healthcenter_number=70)
        self.neighbourhood.save()

        self.profile = Profile(user=self.user, name='betty', status='my bio',
                               profile_image='image.png', location='There')

    def test_instance(self):
        self.assertTrue(isinstance(self.profile, Profile))

    def test_save_profile(self):
        profiles = Profile.objects.all()
        self.assertTrue(len(profiles) > 0)

    def test_delete_profile(self):
        profile = Profile.objects.all().delete()
        self.assertTrue(len(profile) > 0)

    def tearDown(self):
        Profile.objects.all().delete()

class TestNeigbourhood(TestCase):
    def setUp(self):
        self.neighbourhood = Neigbourhood(name='Kendu', description='My neighbourhood', location='Bomet',
                                          admin='andy', police_number=0, healthcenter_number=0, occupants_count='4')
        self.neighbourhood.save()

    def test_instance(self):
        self.assertTrue(isinstance(self.neighbourhood, Neigbourhood))

    def test_save_neighbourhood(self):
        hood = Neigbourhood.objects.all()
        self.assertTrue(len(hood) > 0)

    def test_delete_neighbourhood(self):
        hoods = Neigbourhood.objects.all().delete()
        self.assertTrue(len(hoods) > 0)

class TestBusiness(TestCase):
    def setUp(self):
        self.user = User(username='Ian',
                         email='ian@gmail.com', password='123')
        self.user.save()

        self.neighbourhood = Neigbourhood(
            name='Thika', description='My neighbourhood', police_number=0, health_number=0)
        self.hood.save()

        self.busins = Business(name='Cyber', email='cyberfree@gmail.com',
                               description='all computer things', neighbourhood=self.hood, user=self.user)

    def test_instance(self):
        self.assertTrue(isinstance(self.busins, Business))

    def test_save_hood(self):
        business = Business.objects.all()
        self.assertTrue(len(business) > 0)

    def test_delete_hood(self):
        business = Business.objects.all().delete()
        self.assertTrue(len(business) > 0)