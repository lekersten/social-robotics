from autobahn.twisted.component import Component, run
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.util import sleep

@inlineCallbacks
def main(session, details):
    
    yield session.call("rie.dialogue.config.language", lang="en")
    yield session.call("rom.optional.behavior.play", name="BlocklyStand")
    
    yield session.call("rom.actuator.motor.write",
                    frames=[{"time": 400, "data": {"body.arms.right.lower.roll": -1.5, "body.arms.left.upper.pitch": .3}},
                            ],
                            force=True
                            )

    yield session.call("rom.actuator.motor.write",
                    frames=[{"time": 600, "data": {"body.arms.right.upper.pitch": -0.9, "body.arms.right.lower.roll": -.95}},
                            {"time": 1200, "data": {"body.arms.right.upper.pitch": .2, "body.arms.right.lower.roll": -1}},
                            {"time": 1800, "data": {"body.arms.right.upper.pitch": -0.9, "body.arms.right.lower.roll": -.85}},
                            {"time": 2400, "data": {"body.arms.right.upper.pitch": .2, "body.arms.right.lower.roll": -1}},
                            {"time": 3000, "data": {"body.arms.right.upper.pitch": -0.9, "body.arms.right.lower.roll": -.85}},
                            ],
                    force=True
                    )

    yield session.call("rom.actuator.motor.write",
                        frames=[{"time": 600, "data": {"body.arms.left.upper.pitch": -1.5, "body.arms.right.upper.pitch": -1.5,
                                                        "body.arms.left.lower.roll": -1.5, "body.arms.right.lower.roll": -1.5}},
                                {"time": 1200, "data": {"body.arms.left.upper.pitch": -1.75, "body.arms.right.upper.pitch": -1.75,
                                                        "body.arms.left.lower.roll": -.5, "body.arms.right.lower.roll": -.5}},
                                {"time": 2000, "data": {"body.arms.left.upper.pitch": 0, "body.arms.right.upper.pitch": 0,
                                                        "body.arms.left.lower.roll": -1, "body.arms.right.lower.roll": -1}}
                                ],
                                force=True
                                )
    
    session.leave()
    


wamp = Component(
    transports=[{
        "url": "ws://wamp.robotsindeklas.nl",
        "serializers": ["msgpack"],
        "max_retries": 0
    }],
    realm="rie.65eed9c4d9eb6cfb396e7432",
)

wamp.on_join(main)

if __name__ == "__main__":
    run([wamp])
