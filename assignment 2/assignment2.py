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

    t_0 = 1.5  # wait (s) before start preparation
    t_1 = 1500  # preparation duration
    t_2 = 2000 / 5  # stroke duration
    t_3 = 1000  # retraction duration

    session.call("rie.dialogue.say", text="It makes me very upset that you don't want to hear my story.")

    sleep(t_0)

    # Preparation
    session.call("rom.actuator.motor.write",
                 frames=[
                     {"time": t_1, "data": {"body.arms.right.upper.pitch": -1.5, "body.arms.left.upper.pitch": -1.5,
                                            "body.arms.right.lower.roll": -1.5, "body.arms.left.lower.roll": -1.5,
                                            "body.legs.right.upper.pitch": -0.5,
                                            "body.legs.left.upper.pitch": -0.5}}],
                 force=True
                 )

    # During stroke
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

    # Retraction
    session.call("rom.actuator.motor.write",
                 frames=[{"time": t_3,
                          "data": {"body.legs.right.upper.pitch": 0, "body.legs.left.upper.pitch": 0,
                                   "body.arms.right.lower.roll": 0, "body.arms.left.lower.roll": 0,
                                   "body.arms.right.upper.pitch": 0, "body.arms.left.upper.pitch": 0}}],
                 force=True
                 )

    yield session.call("rie.dialogue.say_animated", text="Thank you!")

    session.call("rom.actuator.motor.write",
                 frames=[{"time": 200, "data": {"body.head.pitch": 0, "body.head.yaw": 0}}],
                 force=True
                 )
    yield session.call("rom.optional.behavior.play", name="BlocklyStand")


def big_gesture(session, details):
    sleep(0.5)

    # Preparation (have arms close to chest)
    session.call("rom.actuator.motor.write",
                 frames=[
                     {"time": 1000, "data": {"body.arms.right.upper.pitch": -0, "body.arms.left.upper.pitch": -0,
                                             "body.arms.right.lower.roll": -1.6, "body.arms.left.lower.roll": -1.6,
                                             "body.head.yaw": 0, "body.head.pitch": 0}}],
                 force=True
                 )
    # During stroke (move arms away from body slightly and up, then move arms outward)
    session.call("rom.actuator.motor.write",
                 frames=[
                     {"time": 1000,
                      "data": {"body.arms.right.upper.pitch": -1.5, "body.arms.left.upper.pitch": -1.5,
                               "body.arms.right.lower.roll": -1.0, "body.arms.left.lower.roll": -1.0}},
                     {"time": 1700,
                      "data": {"body.arms.right.upper.pitch": -2.5, "body.arms.left.upper.pitch": -2.5,
                               "body.arms.right.lower.roll": 2.0, "body.arms.left.lower.roll": 2.0}}
                 ],
                 force=True
                 )
    # Retract (lower arms down and move back to robot's sides)
    session.call("rom.actuator.motor.write",
                 frames=[
                     {"time": 1000, "data": {"body.arms.right.upper.pitch": 0, "body.arms.left.upper.pitch": 0,
                                             "body.arms.right.lower.roll": 0, "body.arms.left.lower.roll": 0}},
                     {"time": 1500, "data": {"body.arms.right.upper.pitch": 0, "body.arms.left.upper.pitch": 0,
                                             "body.arms.right.lower.roll": -1, "body.arms.left.lower.roll": -1}}],
                 force=True
                 )


def basketball_gesture(session, details):
    # Preparation
    session.call("rom.actuator.motor.write",
                 frames=[{"time": 650, "data": {"body.arms.right.lower.roll": -1.5, "body.arms.left.upper.pitch": .3,
                                                "body.head.yaw": 0, "body.head.pitch": 0}},
                         ],
                 force=True
                 )

    # During stroke (bouncing)
    rep_time = 2400 / 5
    session.call("rom.actuator.motor.write",
                 frames=[{"time": rep_time,
                          "data": {"body.arms.right.upper.pitch": -0.9, "body.arms.right.lower.roll": -.95}},
                         {"time": rep_time * 2,
                          "data": {"body.arms.right.upper.pitch": .2, "body.arms.right.lower.roll": -1}},
                         {"time": rep_time * 3,
                          "data": {"body.arms.right.upper.pitch": -0.9, "body.arms.right.lower.roll": -.85}},
                         {"time": rep_time * 4,
                          "data": {"body.arms.right.upper.pitch": .2, "body.arms.right.lower.roll": -1}},
                         {"time": rep_time * 5,
                          "data": {"body.arms.right.upper.pitch": -0.9, "body.arms.right.lower.roll": -.85}},
                         ],
                 force=True
                 )

    # During stroke (throwing) + Retract (at time: 2000)
    session.call("rom.actuator.motor.write",
                 frames=[{"time": 800, "data": {"body.arms.left.upper.pitch": -1.5, "body.arms.right.upper.pitch": -1.5,
                                                "body.arms.left.lower.roll": -1.5, "body.arms.right.lower.roll": -1.5}},
                         {"time": 1200,
                          "data": {"body.arms.left.upper.pitch": -1.75, "body.arms.right.upper.pitch": -1.75,
                                   "body.arms.left.lower.roll": -.5, "body.arms.right.lower.roll": -.5}},
                         {"time": 2000, "data": {"body.arms.left.upper.pitch": 0, "body.arms.right.upper.pitch": 0,
                                                 "body.arms.left.lower.roll": -1, "body.arms.right.lower.roll": -1}}
                         ],
                 force=True
                 )


@inlineCallbacks
def greeting(session, details):
    session.call("rie.dialogue.say", text="Hey you, over there!")

    # Prepare greeting wave
    yield session.call("rom.actuator.motor.write",
                       frames=[{"time": 600, "data": {"body.arms.right.upper.pitch": -2.5}}],
                       force=True
                       )

    # During greeting wave
    yield session.call("rom.actuator.motor.write",
                       frames=[{"time": 800, "data": {"body.arms.right.lower.roll": 1.5}},
                               {"time": 1200, "data": {"body.arms.right.lower.roll": -1}},
                               {"time": 1600, "data": {"body.arms.right.lower.roll": 1.5}},
                               {"time": 2000, "data": {"body.arms.right.lower.roll": -1}},
                               {"time": 2400, "data": {"body.arms.right.lower.roll": 1.5}}],
                       force=True
                       )

    session.call("rie.dialogue.say", text="Come closer, I want to ask you something")

    # Prepare beckoning wave
    session.call("rom.actuator.motor.write",
                 frames=[{"time": 400, "data": {"body.arms.left.upper.pitch": -1}}],
                 force=True
                 )

    # During beckoning wave
    session.call("rom.actuator.motor.write",
                 frames=[{"time": 800, "data": {"body.arms.left.lower.roll": -1.7}},
                         {"time": 1200, "data": {"body.arms.left.lower.roll": -1}},
                         {"time": 1600, "data": {"body.arms.left.lower.roll": -1.7}},
                         {"time": 2000, "data": {"body.arms.left.lower.roll": -1}},
                         {"time": 2400, "data": {"body.arms.left.lower.roll": -1.7}},
                         {"time": 2800, "data": {"body.arms.left.lower.roll": -1}}],
                 force=True
                 )

    # Retraction
    yield sleep(3)
    yield session.call("rom.optional.behavior.play", name="BlocklyStand")


@inlineCallbacks
def tell_story(session, details):
    yield session.call("rie.dialogue.say_animated", text="The other day I went to see a basketball game at the "
                                                         "stadium downtown. It was so cool with so many people "
                                                         "cheering and drums playing – it was like a big party. When "
                                                         "I got inside, I felt really excited. The game was awesome, "
                                                         "with great plays that made everyone cheer.")
    # Sentence with gesture "huge"
    big_gesture(session, details)
    yield session.call("rie.dialogue.say", text="The crowd and the stadium were so huge and also so loud.")

    yield session.call("rie.dialogue.say_animated",
                       text="After the game, even though our team didn't win and I was a bit sad, I was allowed to go "
                            "onto the court.")

    # Sentence with bounce and throw basketball gesture
    basketball_gesture(session, details)
    yield session.call("rie.dialogue.say",
                       text="I got the ball and bounced it around, threw it and even got it in the basket!")

    yield session.call("rie.dialogue.say_animated", text="Everyone cheered and I even got to meet some of the "
                                                         "players. It was a day full of basketball, a huge stadium, "
                                                         "and a lot of happy feelings. Pretty cool, right?")

    # Move robot back to neutral position
    session.call("rom.actuator.motor.write",
                 frames=[{"time": 200, "data": {"body.head.pitch": 0, "body.head.yaw": 0}}],
                 force=True
                 )
    yield session.call("rom.optional.behavior.play", name="BlocklyStand")


@inlineCallbacks
def main(session, details):
    yield session.call("rie.dialogue.config.language", lang="en")
    yield session.call("rom.optional.behavior.play", name="BlocklyStand")

    yield greeting(session, details)
    session.call("rie.dialogue.say", text="Would you like to hear a story?")

    # Robot reads the card
    card = yield session.call("rie.vision.card.read")
    card_id = card[-1]['data']['body'][0][-1]

    if card_id == 0:
        print("You responded YES")
        yield tell_story(session, details)

    elif card_id == 1:
        print("You responded NO")
        yield say_upset_sentence(session, details)

    yield session.leave()


wamp = Component(
    transports=[{
        "url": "ws://wamp.robotsindeklas.nl",
        "serializers": ["msgpack"],
        "max_retries": 0
    }],
    realm="rie.65eeee61d9eb6cfb396e75c8",
)

wamp.on_join(main)

if __name__ == "__main__":
    run([wamp])
