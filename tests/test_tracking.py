async def test_create_tracking(client_with_token):
    response = await client_with_token.post("/tracking", json={
        "coin_id": "bitcoin"
    })
    assert response.status_code == 201
    
async def test_get_all_users_tracking(client_with_token):
    response = await client_with_token.get(url="/tracking")
    assert response.status_code == 200
    
async def test_get_tracking_by_id(client_with_token):
    response = await client_with_token.get(url="/tracking/1")
    assert response.status_code == 200
    
async def test_get_unreal_tracking(client_with_token):
    response = await client_with_token.get(url="/tracking/999")
    assert response.status_code == 404
    
async def test_deleting_tracking(client_with_token):
    response = await client_with_token.delete(url="/tracking/1")
    assert response.status_code == 200
    