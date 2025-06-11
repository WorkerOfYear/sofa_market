class TestAddUser:
    async def test_add_user(self, client):
        params = {
            "email": "test@mail.ru",
            "phone": "89993332211",
            "city": "krg",
            "password": "12345678"
        }
        response = client.post("/user/", params=params)
        assert response.status_code == 200
