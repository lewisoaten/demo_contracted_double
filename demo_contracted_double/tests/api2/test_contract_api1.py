import uvicorn
from multiprocessing import Process
import pytest
from pact import Verifier

from demo_contracted_double.api2 import app


def run_server():
    uvicorn.run(app, host="127.0.0.1", port=40123, log_level="info")


@pytest.fixture
def server():
    proc = Process(target=run_server, args=(), daemon=True)
    proc.start()
    yield
    proc.kill()  # Cleanup after test


def test_read_main(server):
    verifier = Verifier(provider='api2', provider_base_url="http://127.0.0.1:40123")
    output, _ = verifier.verify_pacts('./demo_contracted_double/tests/api1-api2.json', verbose=False)

    assert (output == 0)
