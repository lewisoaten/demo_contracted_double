from fastapi.testclient import TestClient

from demo_contracted_double.api1 import app
import atexit

from pact import Consumer, Provider, Term

pact = Consumer('api1').has_pact_with(Provider('api2'), port=8001, pact_dir="./demo_contracted_double/tests/")
pact.start_service()
atexit.register(pact.stop_service)

client = TestClient(app)


def test_add():
    expected = {
        "time": Term(r"\d+-\d+-\d+T\d+:\d+:\d+\.\d+", "2021-02-06T10:11:27.919516"),
        "first": 10,
        "second": 20,
        "result": 30,
    }

    (pact
     .upon_receiving('a request to sum 10 and 20')
     .with_request('get', '/sum/10/and/20')
     .will_respond_with(200, body=expected))

    with pact:
        response = client.get("/add_ten/20")

    assert response.text == "30"
