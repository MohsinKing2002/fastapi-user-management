# Test user creation
def test_create_users(client):
    response = client.post(
        "/users/new",
        json={
            "name": "Moinul",
            "email": "moinul@example.com",
            "phone_number": "9876543210",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Moinul"
    assert data["email"] == "moinul@example.com"
    assert data["phone_number"] == "9876543210"
    assert "id" in data
    assert "created_at" in data


# Test duplicate email -> 409
def test_duplicate_email_returns_409(client):
    payload = {
        "name": "Moinul Ali",
        "email": "moinul@example.com",
        "phone_number": "9876543210",
    }

    first = client.post("/users/new", json=payload)
    second = client.post("/users/new", json=payload)

    assert first.status_code == 201
    assert second.status_code == 409


# Test missing name -> 422
def test_missing_name_returns_422(client):
    payload = {"email": "moinul@example.com"}

    response = client.post("/users/new", json=payload)

    assert response.status_code == 422


# Test get all users
def test_get_all_users(client):
    payload = {
        "name": "Moinul Ali",
        "email": "moinul@example.com",
        "phone_number": "9876543210",
    }

    create_response = client.post("/users/new", json=payload)
    assert create_response.status_code == 201

    response = client.get("/users/all")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert isinstance(response.json(), list)
    assert response.json()[0]["name"] == "Moinul Ali"
    assert response.json()[0]["phone_number"] == "9876543210"


# Test get missing user
def test_get_missing_user_returns_404(client):
    response = client.get("/users/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}
