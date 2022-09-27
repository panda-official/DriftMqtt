""" Test Mqtt client
"""
from pathlib import Path
from typing import List, Optional

import pytest

from drift_mqtt import Client
from drift_mqtt.client import MQTTMessage

HERE = Path(__file__).parent.resolve()


@pytest.fixture(name="paho_client")
def _make_client(mocker):
    client_klass = mocker.patch("drift_mqtt.client.PahoClient")
    client = mocker.Mock()
    client_klass.return_value = client
    return client


def test__connection_refused():
    """Should rise connection exception"""
    client = Client(uri="tcp://0.0.0.0:1883", client_id="some_test_client_id")
    with pytest.raises(ConnectionRefusedError):
        client.connect()


last_message: List[Optional[MQTTMessage]] = [None]


def hander(message: MQTTMessage):
    last_message[0] = message


@pytest.mark.parametrize(
    "topic, received_topic",
    [
        ("drift/topic1", b"drift/topic1"),
        ("drift/#", b"drift/topic1"),
        ("drft/#/subpath", b"drft/topic/subpath"),
    ],
)
def test__handle_subscriptions(paho_client, topic: str, received_topic: bytes):
    """Should parse topic and call handlers"""
    client = Client(uri="tcp://0.0.0.0:1883")

    client.subscribe(topic, hander)
    paho_client.on_message(None, None, message=MQTTMessage(topic=received_topic))
    assert last_message[0].topic == received_topic.decode("ascii")


@pytest.mark.parametrize(
    "topic, received_topic",
    [
        ("drift/topic1", b"drift/skip"),
        ("drift/#", b"skip/topic1"),
        ("drft/#/subpath", b"drft/topic/skip"),
    ],
)
def test__handle_subscriptions(paho_client, topic: str, received_topic: bytes):
    """Should parse topic and skip topics"""
    client = Client(uri="tcp://0.0.0.0:1883")

    client.subscribe(topic, hander)
    paho_client.on_message(None, None, message=MQTTMessage(topic=received_topic))
    assert last_message[0] is None
