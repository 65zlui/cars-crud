def test_post_car_returns_201_and_json(client):
    payload = {
    "make": "Ford",
    "model": "Fiesta",
    "year": 2018,
    "color": "Black",
    }
    response = client.post("/api/cars", json=payload)
    assert response.status_code == 201
    # assert response.statuscode == 200
    car = response.json()
    assert car["id"] > 0
    assert car["make"] == "Ford"
    assert car["model"] == "Fiesta"
    assert response.headers["location"] == f"/api/cars/{car['id']}"

def test_invalid_year_is_not_saved(client):
    # 1. 发送一个 year=1800 的 POST 请求，其余字段合法
    response = client.post(
        "/api/cars",
        json={
            "make": "Toyota",
            "model": "Corolla",
            "year": 1800,
            "price": 20000,
        },
    )

    # 2. 断言状态码是 422（校验失败）
    assert response.status_code == 422

    # 3. 再 GET 一次，确认没有任何数据被保存
    get_response = client.get("/api/cars")
    assert get_response.status_code == 200
    assert get_response.json() == []