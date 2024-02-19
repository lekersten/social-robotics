from autobahn.twisted.component import Component, run
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.util import sleep


@inlineCallbacks
def main(session, details):
    yield session.call("rom.actuator.audio.stream",
                       url="http://icecast-qmusicnl-cdp.triple-it.nl/Qmusic_nl_classics_96.mp3",
                       sync=False
                       )
    yield sleep(30)
    yield session.call("rom.actuator.audio.stop")
    session.leave()  # Close the connection with the robot


wamp = Component(
    transports=[{
        "url": "ws://wamp.robotsindeklas.nl",
        "serializers": ["msgpack"],
        "max_retries": 0
    }],
    realm="rie.65c375afc01d7b660046e90c",
)

wamp.on_join(main)

if __name__ == "__main__":
    run([wamp])
