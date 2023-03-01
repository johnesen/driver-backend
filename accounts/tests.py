from django.test import TestCase
from django.contrib.auth import get_user_model
import json


User = get_user_model()


class UserTestCase(TestCase):
    def setUp(self) -> None:
        user = User.objects.create(login="test", is_active=True, is_staff=True)
        user.set_password("test")
        user.save()

    def testUserCreate(self):
        data = {
            "login": "test1",
            "email": "test1@gmail.com",
            "phone": "+996555555555",
            "first_name": "test",
            "last_name": "user",
            "middle_name": "1",
            "is_active": True,
            "is_staff": True,
        }
        user = User(**data)
        user.set_password("test1")
        user.save()

        existUser = User.objects.filter(**data).exists()
        self.assertEqual(existUser, True)

    def testLoginEndpoint(self):
        response = self.client.post(
            "/api/v1/login/", {"login": "test", "password": "test"}
        )
        self.assertEqual(response.status_code, 200)

    def testRegisterEndpoint(self):
        data = {
            "client": {
                "login": "test2@gmail.com",
                "password": "test2test2",
                "confirm_password": "test2test2",
                "user_type": "client",
            },
            "driver": {
                "login": "test3@gmail.com",
                "password": "test3test3",
                "confirm_password": "test3test3",
                "user_type": "driver",
            },
        }

        response1 = self.client.post(
            "/api/v1/register/",
            data["client"],
        )
        response2 = self.client.post(
            "/api/v1/register/",
            data["driver"],
        )
        self.assertEqual(response1.status_code, 201)
        self.assertEqual(response2.status_code, 201)

        userClient = User.objects.filter(login="test2@gmail.com").first()
        self.assertEqual(userClient.is_client, True)
        userDriver = User.objects.filter(login="test3@gmail.com").first()
        self.assertEqual(userDriver.is_driver, True)

    def testRefreshingToken(self):
        login_response = self.client.post(
            "/api/v1/login/", {"login": "test", "password": "test"}
        )
        my_json = login_response.content.decode("utf8").replace("'", '"')
        data = json.loads(my_json)["data"]["refresh_token"]
        refresh_resnponse = self.client.post("/api/v1/refresh/", {"refresh": data})
        self.assertEqual(refresh_resnponse.status_code, 200)

    def testGetProfileData(self):
        login_response = self.client.post(
            "/api/v1/login/", {"login": "test", "password": "test"}
        )
        my_json = login_response.content.decode("utf8").replace("'", '"')
        data = json.loads(my_json)["data"]["access_token"]
        profile_resnponse = self.client.get(
            "/api/v1/profile/", **{"HTTP_AUTHORIZATION": f"Bearer {data}"}
        )
        self.assertEqual(profile_resnponse.status_code, 200)
