from autobahn.twisted.component import Component, run
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.util import sleep

@inlineCallbacks
def main(session, details):
    
    yield session.call("rie.dialogue.config.language", lang="en")
    yield session.call("rom.optional.behavior.play", name="BlocklyStand")

    prep_2 = 600  # start preparation for greeting
    target_2 = 1200  # target time for greeting
    duration_2 = 1800 / 3  # duration of greeting (400ms increments)
    
    retract_2 = 2400  # retraction 

    session.call("rie.dialogue.say", text="And I kicked the ball so hard and it flew straight into the goal!")

    # combine greeting and beckonings
    yield session.call("rom.actuator.motor.write",
                       frames=[{"time": prep_2, "data": {"body.arms.left.upper.pitch": -2.5, "body.legs.right.upper.pitch":-1.25, "body.torso.yaw": -0.3}},
                               {"time": target_2, "data": {"body.arms.left.upper.pitch": 0, "body.legs.right.upper.pitch":1.25, "body.torso.yaw": 0.3}},
                            #    {"time": duration_2*3, "data": {"body.arms.right.upper.pitch": 0, "body.arms.right.lower.roll": 0, "body.arms.left.lower.roll": -1.7}},
                               {"time": retract_2, "data": {"body.legs.right.upper.pitch":0, "body.torso.yaw": 0}}],
                       force=True
                       )
    
    session.leave()
    


wamp = Component(
    transports=[{
        "url": "ws://wamp.robotsindeklas.nl",
        "serializers": ["msgpack"],
        "max_retries": 0
    }],
    realm="rie.65e888a2d9eb6cfb396e55ad",
)

wamp.on_join(main)

if __name__ == "__main__":
    run([wamp])
