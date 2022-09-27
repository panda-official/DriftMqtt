""" Test Mqtt client
"""
from pathlib import Path

import pytest
from paho.mqtt.client import MQTTMessage

from drift_mqtt import Client

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


@pytest.fixture(name="last_message")
def _make_last_message():
    last_message = [None]
    return last_message


@pytest.fixture(name="handler")
def _make_handler(last_message):
    def handler(message: MQTTMessage):
        """Simple handler just to keep a received message"""
        last_message[0] = message

    return handler


@pytest.mark.parametrize(
    "topic, received_topic",
    [
        ("drift/topic1", b"drift/topic1"),
        ("drift/#", b"drift/topic1"),
        ("drft/#/subpath", b"drft/topic/subpath"),
    ],
)
def test__handle_subscriptions(
    paho_client, topic, received_topic, handler, last_message
):
    """Should parse topic and call handlers"""
    client = Client(uri="tcp://0.0.0.0:1883")

    client.subscribe(topic, handler)
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
def test__skip_subscriptions(paho_client, topic, received_topic, handler, last_message):
    """Should parse topic and skip"""
    client = Client(uri="tcp://0.0.0.0:1883")

    client.subscribe(topic, handler)
    paho_client.on_message(None, None, message=MQTTMessage(topic=received_topic))
    assert last_message[0] is None
