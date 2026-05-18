

async def test_register(async_client):
    response = await async_client.post("/register", json={
        "email": "test@test.com",
        "password": "password123"
    })
    assert response.status_code == 201
    
async def test_second_email_registration(async_client):
    response = await async_client.post("/register", json={
        "email": "test@test.com",
        "password": "password123"
    })
    assert response.status_code == 400
    
async def test_login(async_client):
    response = await async_client.post("/login", json={
        "email": "test@test.com",
        "password": "password123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
    
async def test_login_wrong_password(async_client):
    response = await async_client.post("/login", json={
        "email": "test@test.com",
        "password": "wrong_password"
    })
    assert response.status_code == 401