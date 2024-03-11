from autobahn.twisted.component import Component, run
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.util import sleep

head_patted = False


def touched(frame):
    global head_patted
    if (("body.head.front" in frame["data"] and frame["data"]["body.head.front"]) or
            ("body.head.middle" in frame["data"] and frame["data"]["body.head.middle"]) or
            ("body.head.rear" in frame["data"] and frame["data"]["body.head.rear"])):
        print("The head was touched!")
        head_patted = True

@inlineCallbacks
def say_upset_sentence(session, details):
    yield session.call("rom.optional.behavior.play", name="BlocklyStand")

    t_0 = 1  # wait before start preparation
    t_1 = 1500  # preparation duration
    t_2 = 2000 / 5  # stroke duration
    t_3 = 1000  # retraction duration

    session.call("rie.dialogue.say", text="It makes me very upset that you don't want to hear my story.")

    sleep(t_0)

    # preparation
    session.call("rom.actuator.motor.write",
                 frames=[
                     {"time": t_1, "data": {"body.arms.right.upper.pitch": -1.5, "body.arms.left.upper.pitch": -1.5,
                                                "body.arms.right.lower.roll": -1.5, "body.arms.left.lower.roll": -1.5,
                                                "body.legs.right.upper.pitch": -0.5,
                                                "body.legs.left.upper.pitch": -0.5}}],
                 force=True
                 )

    # during stroke
    session.call("rom.actuator.motor.write",
                 frames=[{"time": t_2, "data": {"body.head.pitch": 0.17}}],
                 force=True
                 )

    session.call("rom.actuator.motor.write",
                 frames=[{"time": t_2, "data": {"body.head.yaw": 0.5}},
                         {"time": t_2 * 2, "data": {"body.head.yaw": -0.5}},
                         {"time": t_2 * 3, "data": {"body.head.yaw": 0.5}},
                         {"time": t_2 * 4, "data": {"body.head.yaw": -0.5}},
                         {"time": t_2 * 5, "data": {"body.head.yaw": 0}}],
                 force=True
                 )

    # First wait for user to touch its head
    yield session.subscribe(touched, "rom.sensor.touch.stream")
    yield session.call("rom.sensor.touch.stream")

    while not head_patted:
        yield sleep(0.5)

    # retraction
    session.call("rom.actuator.motor.write",
                 frames=[{"time": t_3,
                          "data": {"body.legs.right.upper.pitch": 0, "body.legs.left.upper.pitch": 0,
                                   "body.arms.right.lower.roll": 0, "body.arms.left.lower.roll": 0,
                                   "body.arms.right.upper.pitch": 0, "body.arms.left.upper.pitch": 0}}],
                 force=True
                 )

    yield session.call("rie.dialogue.say_animated", text="Thank you!")

    yield session.call("rom.optional.behavior.play", name="BlocklyStand")


@inlineCallbacks
def say_big_sentence(session, details):
    # After preparation (have arms close to chest, maybe lower body somehow?)
    session.call("rom.actuator.motor.write",
                 frames=[
                     {"time": 1000, "data": {"body.arms.right.upper.pitch": -1.0, "body.arms.left.upper.pitch": -1.0,
                                             "body.arms.right.lower.roll": -1.7, "body.arms.left.lower.roll": -1.7}}],
                 force=True
                 )
    # During stroke (move arms away from body slightly and up, then move arms outward)
    yield session.call("rom.actuator.motor.write",
                       frames=[
                           {"time": 1000,
                            "data": {"body.arms.right.upper.pitch": -1.5, "body.arms.left.upper.pitch": -1.5,
                                     "body.arms.right.lower.roll": -1.0, "body.arms.left.lower.roll": -1.0}},
                           {"time": 2000,
                            "data": {"body.arms.right.upper.pitch": -2.5, "body.arms.left.upper.pitch": -2.5,
                                     "body.arms.right.lower.roll": 2.0, "body.arms.left.lower.roll": 3.0}}
                       ],
                       force=True
                       )
    # After stroke (lower arms down and move back to robot's sides)
    yield session.call("rom.actuator.motor.write",
                       frames=[
                           {"time": 1000, "data": {"body.arms.right.upper.pitch": 0, "body.arms.left.upper.pitch": 0,
                                                   "body.arms.right.lower.roll": 0, "body.arms.left.lower.roll": 0}},
                           {"time": 1500, "data": {"body.arms.right.upper.pitch": 0, "body.arms.left.upper.pitch": 0,
                                                   "body.arms.right.lower.roll": -1, "body.arms.left.lower.roll": -1}}],
                       force=True
                       )


@inlineCallbacks
def basketball(session, details):
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

@inlineCallbacks
def greeting(session, details):
    prep_1 = 400  # start preparation for greeting
    target_1 = 1200  # target time for greeting
    duration_1 = 3600 / 9  # duration of greeting (400ms increments)

    retract = 4000  # retraction

    session.call("rie.dialogue.say", text="Hey you, over there!")

    yield session.call("rom.actuator.motor.write",
                       frames=[{"time": 600, "data": {"body.arms.right.upper.pitch": -2.5}}],
                       force=True
                       )

    yield session.call("rom.actuator.motor.write",
                       frames=[{"time": 800, "data": {"body.arms.right.lower.roll": 1.5}},
                               {"time": 1200, "data": {"body.arms.right.lower.roll": -1}},
                               {"time": 1600, "data": {"body.arms.right.lower.roll": 1.5}},
                               {"time": 2000, "data": {"body.arms.right.lower.roll": -1}},
                               {"time": 2400, "data": {"body.arms.right.lower.roll": 1.5}}],
                       force=True
                       )

    session.call("rie.dialogue.say", text="Come closer, I want to ask you something")

    # beckoning wave
    session.call("rom.actuator.motor.write",
                 frames=[{"time": 400, "data": {"body.arms.left.upper.pitch": -1}}],
                 force=True
                 )

    session.call("rom.actuator.motor.write",
                 frames=[{"time": 800, "data": {"body.arms.left.lower.roll": -1.7}},
                         {"time": 1200, "data": {"body.arms.left.lower.roll": -1}},
                         {"time": 1600, "data": {"body.arms.left.lower.roll": -1.7}},
                         {"time": 2000, "data": {"body.arms.left.lower.roll": -1}},
                         {"time": 2400, "data": {"body.arms.left.lower.roll": -1.7}},
                         {"time": 2800, "data": {"body.arms.left.lower.roll": -1}}],
                 force=True
                 )


@inlineCallbacks
def main(session, details):
    yield session.call("rie.dialogue.config.language", lang="en")
    yield session.call("rom.optional.behavior.play", name="BlocklyStand")

    yield greeting(session, details)

    yield sleep(2)
    yield session.call("rom.optional.behavior.play", name="BlocklyStand")
    session.call("rie.dialogue.say", text="Would you like to hear a story?")

    card = yield session.call("rie.vision.card.read")
    card_id = card[-1]['data']['body'][0][-1]
    print(card_id, type(card_id))

    if card_id == 0:
        # Tell story
        yield basketball(session, details)
        yield say_big_sentence(session, details)

    elif card_id == 1:
        # upset robot
        yield say_upset_sentence(session, details)

    yield session.leave()


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
