import unittest
from app import app
from base64 import b64encode
import json
from models import User, Audience, engine, Base, Session, Reservation


class TestingBase(unittest.TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app

    tester = app.test_client()
    session = Session()

    def setUp(self):
        delete()

    def tearDown(self):
        self.close_session()

    def close_session(self):
        self.session.close()


class ApiTest(TestingBase):
    user = {
        "name": "Orest",
        "surname": "Chukla",
        "username": "Oliver",
        "password": "123456"
    }

    user_2 = {
        "name": "Orest",
        "surname": "Chukla",
        "username": "Oliver",
        "password": "12345"
    }

    def test_User_Creation(self):
        delete()
        response = self.tester.post("/api/v1/auth/register", data=json.dumps(self.user),
                                    content_type="application/json")
        code = response.status_code
        self.assertEqual(200, code)

    def test_User_Creation_wrong_1(self):
        delete()
        response = self.tester.post("/api/v1/auth/register", data=json.dumps(self.user_2),
                                    content_type="application/json")
        code = response.status_code
        self.assertEqual(401, code)

    def test_Get_User_By_UserName(self):
        delete()
        user = User(id=1, name="Orest", surname="Chukla", username="Oliver", password="123456")
        self.session.add(user)
        self.session.commit()
        creds = b64encode(b"Oliver:123456").decode("utf-8")
        response = self.tester.get('/api/v1/user/Oliver', headers={"Authorization": f"Basic {creds}"})
        # code = response.status_code
        # self.assertEqual(200, code)
        self.assertEqual({"user": {"id": 1, "name": "Orest", "surname": "Chukla", "username": "Oliver"}}, response.json)

    def test_Get_User_By_UserName_wrong_1(self):
        delete()
        user = User(name="Orest", surname="Chukla", username="Oliver", password="123456")
        self.session.add(user)
        self.session.commit()
        creds = b64encode(b"Oliver:123456").decode("utf-8")
        response = self.tester.get('/api/v1/user/Oliver2', headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.assertEqual(404, code)

    def test_Get_User_By_UserName_wrong_2(self):
        delete()
        user = User(name="Orest", surname="Chukla", username="Oliver", password="123456")
        user2 = User(name="batman23", surname="Peter", username="Parker", password="12345678")
        self.session.add(user)
        self.session.add(user2)
        self.session.commit()
        creds = b64encode(b"Oliver:123456").decode("utf-8")
        response = self.tester.get('/api/v1/user/Parker', headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.assertEqual(406, code)

    def test_Update_User(self):
        delete()
        user = User(name="Orest", surname="Chukla", username="Oliver", password="123456")
        self.session.add(user)
        self.session.commit()
        creds = b64encode(b"Oliver:123456").decode("utf-8")
        response = self.tester.put('/api/v1/user/Oliver',
                                   data=json.dumps({"username": "Oliver1", "name": "Orest1", "surname": "Chukla1",
                                                    "password": "12345678"}),
                                   content_type='application/json', headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.assertEqual(200, code)

    def test_Update_User_1(self):
        delete()
        user = User(name="Orest", surname="Chukla", username="Oliver", password="123456")
        user2 = User(name="Orest2", surname="Chukla2", username="Oliver2", password="12345678")
        self.session.add(user)
        self.session.add(user2)
        self.session.commit()
        creds = b64encode(b"Oliver:123456").decode("utf-8")
        response = self.tester.put('/api/v1/user/Oliver',
                                   data=json.dumps({"username": "Oliver2", "name": "Orest1", "surname": "Chukla1",
                                                    "password": "12345678"}),
                                   content_type='application/json', headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.assertEqual(400, code)

    def test_Delete_User_by_Id(self):
        delete()
        user = User(name="Orest", surname="Chukla", username="Oliver", password="123456")
        self.session.add(user)
        self.session.commit()
        creds = b64encode(b"Oliver:123456").decode("utf-8")
        response = self.tester.delete('/api/v1/user/Oliver', headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.assertEqual(200, code)

    def test_Delete_User_by_Id_1(self):
        delete()
        user = User(name="Orest", surname="Chukla", username="Oliver", password="123456")
        self.session.add(user)
        self.session.commit()
        creds = b64encode(b"Oliver:123456").decode("utf-8")
        response = self.tester.delete('/api/v1/user/Oliver2', headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.assertEqual(404, code)

    def test_Delete_User_by_Id_2(self):
        delete()
        user = User(name="Orest", surname="Chukla", username="Oliver", password="123456")
        user2 = User(name="Orest2", surname="Chukla2", username="Oliver2", password="12345678")
        self.session.add(user)
        self.session.add(user2)
        self.session.commit()
        creds = b64encode(b"Oliver:123456").decode("utf-8")
        response = self.tester.delete('/api/v1/user/Oliver2', headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.assertEqual(406, code)

    audience = {
        "number": 101,
        "amount_of_places": 100,
        "status": 1
    }

    audience_2 = {
        "id": "2",
        "number": 101,
        "amount_of_places": 100,
        "status": 1
    }

    def test_Create_New_Audience(self):
        delete()
        user = User(name="Orest", surname="Chukla", username="Oliver", password="123456")
        self.session.add(user)
        self.session.commit()
        creds = b64encode(b"Oliver:123456").decode("utf-8")
        response = self.tester.post("/api/v1/audience", data=json.dumps(self.audience),
                                    content_type="application/json", headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.assertEqual(200, code)

    def test_Create_New_Audience_wrong_1(self):
        delete()
        user = User(name="Orest", surname="Chukla", username="Oliver", password="123456")
        audience = Audience(number=101, amount_of_places=100, status=1)
        self.session.add(user)
        self.session.add(audience)
        self.session.commit()
        creds = b64encode(b"Oliver:123456").decode("utf-8")
        response = self.tester.post("/api/v1/audience", data=json.dumps(self.audience),
                                    content_type="application/json", headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.assertEqual(404, code)

    def test_Create_New_Audience_wrong_2(self):
        delete()
        user = User(name="Orest", surname="Chukla", username="Oliver", password="123456")
        self.session.add(user)
        self.session.commit()
        creds = b64encode(b"Oliver:123456").decode("utf-8")
        response = self.tester.post("/api/v1/audience", data=json.dumps(self.audience_2),
                                    content_type="application/json", headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.assertEqual(400, code)

    def test_Get_All_Audiences(self):
        delete()
        user = User(name="Orest", surname="Chukla", username="Oliver", password="123456")
        audience = Audience(number=101, amount_of_places=100, status=1)
        self.session.add(user)
        self.session.add(audience)
        self.session.commit()
        creds = b64encode(b"Oliver:123456").decode("utf-8")
        response = self.tester.get("/api/v1/audience", headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.assertEqual(200, code)

    def test_Get_Audience_By_Id(self):
        delete()
        user = User(name="Orest", surname="Chukla", username="Oliver", password="123456")
        audience = Audience(number=101, amount_of_places=100, status=1)
        self.session.add(user)
        self.session.add(audience)
        self.session.commit()
        creds = b64encode(b"Oliver:123456").decode("utf-8")
        response = self.tester.get("/api/v1/audience/1", headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.assertEqual(200, code)

    def test_Get_Audience_By_Id_worng_1(self):
        delete()
        user = User(name="Orest", surname="Chukla", username="Oliver", password="123456")
        audience = Audience(number=101, amount_of_places=100, status=1)
        self.session.add(user)
        self.session.add(audience)
        self.session.commit()
        creds = b64encode(b"Oliver:123456").decode("utf-8")
        response = self.tester.get("/api/v1/audience/2", headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.assertEqual(404, code)

    def test_Update_Audience_By_Id(self):
        delete()
        user = User(name="Orest", surname="Chukla", username="Oliver", password="123456")
        audience = Audience(number=101, amount_of_places=100, status=1)
        self.session.add(user)
        self.session.add(audience)
        self.session.commit()
        creds = b64encode(b"Oliver:123456").decode("utf-8")
        response = self.tester.put('/api/v1/audience/1',
                                   data=json.dumps({"number": 103, "amount_of_places": 200, "status": 0}),
                                   content_type='application/json', headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.assertEqual(200, code)

    def test_Update_Audience_By_Id_wrong_1(self):
        delete()
        user = User(name="Orest", surname="Chukla", username="Oliver", password="123456")
        audience = Audience(number=101, amount_of_places=100, status=1)
        self.session.add(user)
        self.session.add(audience)
        self.session.commit()
        creds = b64encode(b"Oliver:123456").decode("utf-8")
        response = self.tester.put('/api/v1/audience/2',
                                   data=json.dumps({"number": 103, "amount_of_places": 200, "status": 0}),
                                   content_type='application/json', headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.assertEqual(404, code)

    def test_Update_Audience_By_Id_wrong_2(self):
        delete()
        user = User(name="Orest", surname="Chukla", username="Oliver", password="123456")
        audience = Audience(number=101, amount_of_places=100, status=1)
        self.session.add(user)
        self.session.add(audience)
        self.session.commit()
        creds = b64encode(b"Oliver:123456").decode("utf-8")
        response = self.tester.put('/api/v1/audience/2',
                                   data=json.dumps({"number": 103, "amount_of_places": 300, "status": "free"}),
                                   content_type='application/json', headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.assertEqual(400, code)

    def test_Update_Audience_By_Id_wrong_3(self):
        delete()
        user = User(name="Orest", surname="Chukla", username="Oliver", password="123456")
        audience = Audience(number=101, amount_of_places=100, status=1)
        audience2 = Audience(number=102, amount_of_places=100, status=1)
        self.session.add(user)
        self.session.add(audience)
        self.session.add(audience2)
        self.session.commit()
        creds = b64encode(b"Oliver:123456").decode("utf-8")
        response = self.tester.put('/api/v1/audience/2',
                                   data=json.dumps({"number": 102, "amount_of_places": 200, "status": 0}),
                                   content_type='application/json', headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.assertEqual(400, code)

    def test_Delete_Audience_By_Id(self):
        delete()
        user = User(name="Orest", surname="Chukla", username="Oliver", password="123456")
        audience = Audience(number=101, amount_of_places=100, status=1)
        self.session.add(user)
        self.session.add(audience)
        self.session.commit()
        creds = b64encode(b"Oliver:123456").decode("utf-8")
        response = self.tester.delete('/api/v1/audience/1', headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.assertEqual(200, code)

    def test_Delete_Audience_By_Id_wrong_1(self):
        delete()
        user = User(name="Orest", surname="Chukla", username="Oliver", password="123456")
        audience = Audience(number=101, amount_of_places=100, status=1)
        self.session.add(user)
        self.session.add(audience)
        self.session.commit()
        creds = b64encode(b"Oliver:123456").decode("utf-8")
        response = self.tester.delete('/api/v1/audience/2', headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.assertEqual(404, code)

    reservation = {
        "user_id": 1,
        "audience_id": 1,
        "title": "for project",
        "from_date": "2021-10-21 00:00:00",
        "to_date": "2021-10-22 23:59:59"
    }

    reservation2 = {
        "user_id": 2,
        "audience_id": 1,
        "title": "for project",
        "from_date": "2021-10-21 00:00:00",
        "to_date": "2021-10-22 23:59:59"
    }

    reservation3 = {
        "user_id": 3,
        "audience_id": 1,
        "title": "for project",
        "from_date": "2021-10-21 00:00:00",
        "to_date": "2021-10-22 23:59:59"
    }

    reservation4 = {
        "user_id": 1,
        "audience_id": "hello",
        "title": "for project",
        "from_date": "2021-10-21",
        "to_date": "2021-10-22"
    }

    reservation5 = {
        "user_id": 1,
        "audience_id": 2,
        "title": "for project",
        "from_date": "2021-10-21 00:00:00",
        "to_date": "2021-10-22 23:59:59"
    }

    reservation6 = {
        "user_id": 1,
        "audience_id": 1,
        "title": "for project",
        "from_date": "2021-10-22 23:59:59",
        "to_date": "2021-10-21 00:00:00"
    }

    reservation7 = {
        "user_id": 1,
        "audience_id": 1,
        "title": "for project",
        "from_date": "2021-10-21 00:00:00",
        "to_date": "2021-11-22 23:59:59"
    }


    def test_Create_New_Reservation(self):
        delete()
        user = User(name="Orest", surname="Chukla", username="Oliver", password="123456")
        audience = Audience(number=101, amount_of_places=100, status=1)
        self.session.add(user)
        self.session.add(audience)
        self.session.commit()
        creds = b64encode(b"Oliver:123456").decode("utf-8")
        response = self.tester.post("/api/v1/reservation", data=json.dumps(self.reservation),
                                    content_type="application/json", headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.assertEqual(200, code)

    def test_Create_New_Reservation_wrong_1(self):
        delete()
        user = User(name="Orest", surname="Chukla", username="Oliver", password="123456")
        user2 = User(name="Orest", surname="Chukla", username="Oliver2", password="123456")
        audience = Audience(number=101, amount_of_places=100, status=1)
        self.session.add(user)
        self.session.add(user2)
        self.session.add(audience)
        self.session.commit()
        creds = b64encode(b"Oliver:123456").decode("utf-8")
        response = self.tester.post("/api/v1/reservation", data=json.dumps(self.reservation2),
                                    content_type="application/json", headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.assertEqual(404, code)

    def test_Create_New_Reservation_wrong_2(self):
        delete()
        user = User(name="Orest", surname="Chukla", username="Oliver", password="123456")
        audience = Audience(number=101, amount_of_places=100, status=1)
        self.session.add(user)
        self.session.add(audience)
        self.session.commit()
        creds = b64encode(b"Oliver:123456").decode("utf-8")
        response = self.tester.post("/api/v1/reservation", data=json.dumps(self.reservation3),
                                    content_type="application/json", headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.assertEqual(404, code)

    def test_Create_New_Reservation_wrong_3(self):
        delete()
        user = User(name="Orest", surname="Chukla", username="Oliver", password="123456")
        audience = Audience(number=101, amount_of_places=100, status=1)
        self.session.add(user)
        self.session.add(audience)
        self.session.commit()
        creds = b64encode(b"Oliver:123456").decode("utf-8")
        response = self.tester.post("/api/v1/reservation", data=json.dumps(self.reservation4),
                                    content_type="application/json", headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.assertEqual(400, code)

    def test_Create_New_Reservation_wrong_4(self):
        delete()
        user = User(name="Orest", surname="Chukla", username="Oliver", password="123456")
        audience = Audience(number=101, amount_of_places=100, status=1)
        self.session.add(user)
        self.session.add(audience)
        self.session.commit()
        creds = b64encode(b"Oliver:123456").decode("utf-8")
        response = self.tester.post("/api/v1/reservation", data=json.dumps(self.reservation5),
                                    content_type="application/json", headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.assertEqual(404, code)

    def test_Create_New_Reservation_wrong_5(self):
        delete()
        user = User(name="Orest", surname="Chukla", username="Oliver", password="123456")
        audience = Audience(number=101, amount_of_places=100, status=1)
        self.session.add(user)
        self.session.add(audience)
        self.session.commit()
        creds = b64encode(b"Oliver:123456").decode("utf-8")
        response = self.tester.post("/api/v1/reservation", data=json.dumps(self.reservation6),
                                    content_type="application/json", headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.assertEqual(400, code)

    def test_Create_New_Reservation_wrong_6(self):
        delete()
        user = User(name="Orest", surname="Chukla", username="Oliver", password="123456")
        audience = Audience(number=101, amount_of_places=100, status=1)
        self.session.add(user)
        self.session.add(audience)
        self.session.commit()
        creds = b64encode(b"Oliver:123456").decode("utf-8")
        response = self.tester.post("/api/v1/reservation", data=json.dumps(self.reservation7),
                                    content_type="application/json", headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.assertEqual(400, code)

    def test_Get_Reservations(self):
        delete()
        user = User(name="Orest", surname="Chukla", username="Oliver", password="123456")
        audience = Audience(number=101, amount_of_places=100, status=1)
        self.session.add(user)
        self.session.add(audience)
        self.session.commit()
        creds = b64encode(b"Oliver:123456").decode("utf-8")
        response = self.tester.get("/api/v1/reservation", headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.assertEqual(200, code)

    def test_Get_Reservation_By_Id(self):
        delete()
        user = User(name="Orest", surname="Chukla", username="Oliver", password="123456")
        audience = Audience(number=101, amount_of_places=100, status=1)
        reservation = Reservation(user_id= 1, audience_id=1, title="for project", from_date="2021-10-21 00:00:00", to_date="2021-10-22 23:59:59")
        self.session.add(user)
        self.session.add(audience)
        self.session.add(reservation)
        self.session.commit()
        creds = b64encode(b"Oliver:123456").decode("utf-8")
        response = self.tester.get("/api/v1/reservation/1", headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.assertEqual(200, code)

    def test_Get_Reservation_By_Id_wrong_1(self):
        delete()
        user = User(name="Orest", surname="Chukla", username="Oliver", password="123456")
        audience = Audience(number=101, amount_of_places=100, status=1)
        reservation = Reservation(user_id= 1, audience_id=1, title="for project", from_date="2021-10-21 00:00:00", to_date="2021-10-22 23:59:59")
        self.session.add(user)
        self.session.add(audience)
        self.session.add(reservation)
        self.session.commit()
        creds = b64encode(b"Oliver:123456").decode("utf-8")
        response = self.tester.get("/api/v1/reservation/2", headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.assertEqual(404, code)

    def test_Update_Reservation_By_Id(self):
        delete()
        user = User(name="Orest", surname="Chukla", username="Oliver", password="123456")
        audience = Audience(number=101, amount_of_places=100, status=1)
        audience2 = Audience(number=102, amount_of_places=100, status=1)
        reservation = Reservation(user_id=1, audience_id=1, title="for project", from_date="2021-10-21 00:00:00", to_date="2021-10-22 23:59:59")
        self.session.add(user)
        self.session.add(audience)
        self.session.add(audience2)
        self.session.add(reservation)
        self.session.commit()
        creds = b64encode(b"Oliver:123456").decode("utf-8")
        response = self.tester.put('/api/v1/reservation/1',
                                   data=json.dumps({"user_id": 1, "audience_id": 1, "title": "for project2", "from_date": "2021-10-22 00:00:00", "to_date": "2021-10-23 23:59:59"}),
                                   content_type='application/json', headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.assertEqual(200, code)

    def test_Delete_Reservation_By_Id(self):
        delete()
        user = User(name="Orest", surname="Chukla", username="Oliver", password="123456")
        audience = Audience(number=101, amount_of_places=100, status=1)
        reservation = Reservation(user_id= 1, audience_id=1, title="for project", from_date="2021-10-21 00:00:00", to_date="2021-10-22 23:59:59")
        self.session.add(user)
        self.session.add(audience)
        self.session.add(reservation)
        self.session.commit()
        creds = b64encode(b"Oliver:123456").decode("utf-8")
        response = self.tester.delete('/api/v1/reservation/1', headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.assertEqual(200, code)

    def test_Delete_Reservation_By_Id_wrong_1(self):
        delete()
        user = User(name="Orest", surname="Chukla", username="Oliver", password="123456")
        audience = Audience(number=101, amount_of_places=100, status=1)
        reservation = Reservation(user_id= 1, audience_id=1, title="for project", from_date="2021-10-21 00:00:00", to_date="2021-10-22 23:59:59")
        self.session.add(user)
        self.session.add(audience)
        self.session.add(reservation)
        self.session.commit()
        creds = b64encode(b"Oliver:123456").decode("utf-8")
        response = self.tester.delete('/api/v1/reservation/2', headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.assertEqual(404, code)

    def test_Delete_Reservation_By_Id_wrong_2(self):
        delete()
        user = User(name="Orest", surname="Chukla", username="Oliver", password="123456")
        user2 = User(name="Orest", surname="Chukla", username="Oliver2", password="123456")
        audience = Audience(number=101, amount_of_places=100, status=1)
        reservation = Reservation(user_id= 2, audience_id=1, title="for project", from_date="2021-10-21 00:00:00", to_date="2021-10-22 23:59:59")
        self.session.add(user)
        self.session.add(user2)
        self.session.add(audience)
        self.session.add(reservation)
        self.session.commit()
        creds = b64encode(b"Oliver:123456").decode("utf-8")
        response = self.tester.delete('/api/v1/reservation/1', headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.assertEqual(404, code)

    def test_Get_Reservations_For_User_Id(self):
        delete()
        user = User(name="Orest", surname="Chukla", username="Oliver", password="123456")
        audience = Audience(number=101, amount_of_places=100, status=1)
        reservation = Reservation(user_id= 1, audience_id=1, title="for project", from_date="2021-10-21 00:00:00", to_date="2021-10-22 23:59:59")
        reservation2 = Reservation(user_id= 1, audience_id=1, title="for project", from_date="2021-10-24 00:00:00", to_date="2021-10-26 23:59:59")
        self.session.add(user)
        self.session.add(audience)
        self.session.add(reservation)
        self.session.add(reservation2)
        self.session.commit()
        creds = b64encode(b"Oliver:123456").decode("utf-8")
        response = self.tester.get("/api/v1/reservation/user_id/1", headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.assertEqual(200, code)

    def test_Get_Reservations_For_User_Id_wrong_1(self):
        delete()
        user = User(name="Orest", surname="Chukla", username="Oliver", password="123456")
        user2 = User(name="Orest", surname="Chukla", username="Oliver2", password="123456")
        audience = Audience(number=101, amount_of_places=100, status=1)
        reservation = Reservation(user_id= 1, audience_id=1, title="for project", from_date="2021-10-21 00:00:00", to_date="2021-10-22 23:59:59")
        reservation2 = Reservation(user_id= 1, audience_id=1, title="for project", from_date="2021-10-24 00:00:00", to_date="2021-10-26 23:59:59")
        self.session.add(user)
        self.session.add(user2)
        self.session.add(audience)
        self.session.add(reservation)
        self.session.add(reservation2)
        self.session.commit()
        creds = b64encode(b"Oliver:123456").decode("utf-8")
        response = self.tester.get("/api/v1/reservation/user_id/2", headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.assertEqual(404, code)

    def test_Get_Reservations_For_User_UserName(self):
        delete()
        user = User(name="Orest", surname="Chukla", username="Oliver", password="123456")
        audience = Audience(number=101, amount_of_places=100, status=1)
        reservation = Reservation(user_id= 1, audience_id=1, title="for project", from_date="2021-10-21 00:00:00", to_date="2021-10-22 23:59:59")
        reservation2 = Reservation(user_id= 1, audience_id=1, title="for project", from_date="2021-10-24 00:00:00", to_date="2021-10-26 23:59:59")
        self.session.add(user)
        self.session.add(audience)
        self.session.add(reservation)
        self.session.add(reservation2)
        self.session.commit()
        creds = b64encode(b"Oliver:123456").decode("utf-8")
        response = self.tester.get("/api/v1/reservation/username/Oliver", headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.assertEqual(200, code)

    def test_Get_Reservations_For_User_UserName_wrong_1(self):
        delete()
        user = User(name="Orest", surname="Chukla", username="Oliver", password="123456")
        audience = Audience(number=101, amount_of_places=100, status=1)
        reservation = Reservation(user_id= 1, audience_id=1, title="for project", from_date="2021-10-21 00:00:00", to_date="2021-10-22 23:59:59")
        reservation2 = Reservation(user_id= 1, audience_id=1, title="for project", from_date="2021-10-24 00:00:00", to_date="2021-10-26 23:59:59")
        self.session.add(user)
        self.session.add(audience)
        self.session.add(reservation)
        self.session.add(reservation2)
        self.session.commit()
        creds = b64encode(b"Oliver:123456").decode("utf-8")
        response = self.tester.get("/api/v1/reservation/username/Olivers", headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.assertEqual(404, code)

    def test_Get_Reservations_For_User_UserName_wrong_2(self):
        delete()
        user = User(name="Orest", surname="Chukla", username="Oliver", password="123456")
        user2 = User(name="Orest", surname="Chukla", username="Oliver2", password="123456")
        audience = Audience(number=101, amount_of_places=100, status=1)
        reservation = Reservation(user_id= 1, audience_id=1, title="for project", from_date="2021-10-21 00:00:00", to_date="2021-10-22 23:59:59")
        reservation2 = Reservation(user_id= 1, audience_id=1, title="for project", from_date="2021-10-24 00:00:00", to_date="2021-10-26 23:59:59")
        self.session.add(user)
        self.session.add(user2)
        self.session.add(audience)
        self.session.add(reservation)
        self.session.add(reservation2)
        self.session.commit()
        creds = b64encode(b"Oliver:123456").decode("utf-8")
        response = self.tester.get("/api/v1/reservation/username/Oliver2", headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.assertEqual(404, code)

def delete():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    unittest.main()
