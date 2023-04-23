
def test_root(client):
    res = client.get('/')
    assert (res.json().get('message')) == "Welcome to DMS APP by Mujahid"
    assert res.status_code == 200


def test_create_customer(test_user, client):
    res = client.post(
        "/authenticate/", data={"username": test_user['email'], "password": test_user['password']})
    token = res.json()['access_token']
    headers = {"Accept": "application/json", "Authorization": "Bearer " + token}
    customer = {"name": "Dummy User", "company": "Architrave"}
    res_customer = client.post("/customers/", headers=headers, json=customer)
    assert res_customer.status_code == 201
    res_customer = res_customer.json()
    assert  res_customer['name'] == customer["name"]
