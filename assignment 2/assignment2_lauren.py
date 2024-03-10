from autobahn.twisted.component import Component, run
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.util import sleep

@inlineCallbacks
def main(session, details):
    
    yield session.call("rie.dialogue.config.language", lang="en")
    yield session.call("rom.optional.behavior.play", name="BlocklyStand")

    prep_1 = 400  # start preparation for greeting
    target_1 = 1200  # target time for greeting
    duration_1 = 3600 / 9  # duration of greeting (400ms increments)
    
    retract = 4000  # retraction 

    session.call("rie.dialogue.say", text="Hey you, over there!")

    # yield sleep(5)
    session.call("rie.dialogue.say", text="Come closer, I want to ask you something")

    # combine greeting and beckoning
    yield session.call("rom.actuator.motor.write",
                       frames=[{"time": prep_1, "data": {"body.arms.right.upper.pitch": -2.5}},
                               {"time": duration_1, "data": {"body.arms.right.lower.roll": 1.5}},
                               {"time": target_1, "data": {"body.arms.right.lower.roll": -1, "body.arms.left.upper.pitch": -0.75}},
                               {"time": duration_1*3, "data": {"body.arms.right.lower.roll": 1.5, "body.arms.left.lower.roll": -1.7}},
                               {"time": duration_1*4, "data": {"body.arms.right.lower.roll": -1, "body.arms.left.lower.roll": -1.25}},
                               {"time": duration_1*5, "data": {"body.arms.right.lower.roll": 1.5, "body.arms.left.lower.roll": -1.7}},
                               {"time": duration_1*6, "data": {"body.arms.right.lower.roll": -1, "body.arms.left.lower.roll": -1.25}},
                               {"time": duration_1*7, "data": {"body.arms.right.upper.pitch": 0, "body.arms.right.lower.roll": 0, "body.arms.left.lower.roll": -1.7}},
                               {"time": duration_1*8, "data": {"body.arms.left.lower.roll": -1.25}},
                               {"time": retract, "data": {"body.arms.left.upper.pitch": 0, "body.arms.left.lower.roll": 0}}],
                       force=True
                       )


    session.call("rie.dialogue.say", text="Would you like to hear a story?")

    frames = yield session.call("rie.vision.card.read")
    print(frames[0]) 

    if frames[0] == 1:
        # Tell story
        yield sleep(5)  

    elif frames[0] == 2:
        # upset robot
        yield sleep(5)


    
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




# # greeting wave
# yield session.call("rom.actuator.motor.write", 
#                    frames = [{"time": 400, "data": {"body.arms.right.upper.pitch": -2.5}}],
#                       force=True
#                       )

# yield session.call("rom.actuator.motor.write",
#                    frames=[{"time": 800, "data": {"body.arms.right.lower.roll": 1.5}},
#                            {"time": 1200, "data": {"body.arms.right.lower.roll": -1}},
#                            {"time": 1600, "data": {"body.arms.right.lower.roll": 1.5}},
#                            {"time": 2000, "data": {"body.arms.right.lower.roll": -1}},
#                            {"time": 2400, "data": {"body.arms.right.lower.roll": 1.5}},
#                            {"time": 2800, "data": {"body.arms.right.lower.roll": -1}}],
#                    force=True
#                    )

# # beckoning wave
# session.call("rom.actuator.motor.write", 
#                    frames = [{"time": 200, "data": {"body.arms.left.upper.pitch": -0.75}}],
#                       force=True
#                       )

# session.call("rom.actuator.motor.write",
#                 frames=[{"time": 800, "data": {"body.arms.left.lower.roll": -1.7}},
#                         {"time": 1100, "data": {"body.arms.left.lower.roll": -1.25}},
#                         {"time": 1400, "data": {"body.arms.left.lower.roll": -1.7}},
#                         {"time": 1700, "data": {"body.arms.left.lower.roll": -1.25}},
#                         {"time": 2000, "data": {"body.arms.left.lower.roll": -1.7}},
#                         {"time": 2300, "data": {"body.arms.left.lower.roll": -1.25}}],
#                 force=True
#                 )