""" Test Mqtt client
"""

from pathlib import Path

import pytest
from drift_mqtt import Client

HERE = Path(__file__).parent.resolve()


def test_connection_refused():
    client = Client(uri="tcp://0.0.0.0:1883", client_id="some_test_client_id")
    with pytest.raises(ConnectionRefusedError):
        client.connect()
