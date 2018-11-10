from django.test import TestCase
from .models import *
from .views import *
from django.contrib.auth.models import User

# Create your tests here.
from MyCenterAPP.models import PersonalDetails


class modelTestCase(TestCase):
    user1 = None
    user2 = None
    user3 = None
    user4 = None

    def setUp(self):
        self.user1 = User.objects.create(username="lang22",password="youbadbad")
        self.user2 = User.objects.create(username="lang23",password="youbadbadbaed")
        userDetail1 = PersonalDetails(user=self.user1,id=self.user1.id)
        userDetail1.save()
        userDetail2 = PersonalDetails(user=self.user2, id=self.user2.id)
        userDetail2.save()
        self.user3 = User.objects.create(username="saokai",password="fighting")
        userDetail3 = PersonalDetails(user=self.user3, id=self.user3.id)
        userDetail3.save()
        self.user4 = User.objects.create(username="saokaifating",password="fighting")
        userDetail4 = PersonalDetails(user=self.user4, id=self.user4.id)
        userDetail4.save()

    def test_model_1(self):
        follow(self.user1,self.user2)
        follow(self.user3,self.user2)
        follow(self.user4,self.user2)

        myFollowing = self.user1.personaldetails.following_set.all()[0].follower.user.username
        print(myFollowing)


        myFollower = self.user2.personaldetails.followers_set.all()
        followers = [f.following.user.username for f in myFollower]
        print(followers)

    def test_model_2(self):
        print('ok2')