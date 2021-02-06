from fastapi.testclient import TestClient

from demo_contracted_double.api2 import app
from demo_contracted_double.model.result import Result

client = TestClient(app)


def test_add():
    response = client.get("/sum/1/and/2")
    assert response.status_code == 200

    result = Result.parse_raw(response.text)
    assert result.result == 3

def test_invalid_input():
    response = client.get("/sum/three/and/2")
    assert response.status_code == 422
    assert response.json() == {'detail': [{'loc': ['path', 'first'], 'msg': 'value is not a valid integer', 'type': 'type_error.integer'}]}