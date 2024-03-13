from autobahn.twisted.component import Component, run
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.util import sleep


@inlineCallbacks
def ask_if_exercises(session, details, exercises):
    question = "Would you like to do some exercises?"
    answers = {"yes": ["yes", "sure", "yeah", "ok", "definitely"], "no": ["no", "not really", "i don't want to"]}

    answer = yield session.call("rie.dialogue.ask",
                                question=question,
                                answers=answers)

    print(answer)
    
    yield session.call("rie.dialogue.stop")

    if answer == "yes":
        yield session.call("rie.dialogue.say_animated", text="Great! Let's begin!")
        exercises = True

    elif answer == "no":

        yield session.call("rie.dialogue.say_animated", text="Are you sure? It's going to be fun!")

        text = yield session.call("rie.dialogue.stt.read")

        response = text[-1]['data']['body']['text']
        print("I heard ", response)

        yes = ["yes", "sure", "yeah", "okay", "definitely"]
        no = ["no", "not really", "i don't want to", "nah"]

        if response in yes:
            yield session.call("rie.dialogue.say_animated", text="I'm glad you changed your mind! Let's begin!")
            exercises = True

        elif response in no:
            yield session.call("rie.dialogue.say_animated", text="Okay, I understand - maybe next time")
            exercises = False
            finished_interaction = True

    return exercises, finished_interaction


@inlineCallbacks
def do_exercises(session, details):

    yield session.call("rie.dialogue.say_animated", text="Are you standing, sitting or laying down?")
    yield sleep(2)

    text = yield session.call("rie.dialogue.stt.read")
    yield sleep(2)
    response = text[-1]['data']['body']['text']
    print("I heard ", response)

    standing = ["standing", "stand"]
    sitting = ["sitting", "sit"]
    laying = ["laying", "lay"]

    yield sleep(2)

    if response in laying or standing:
        yield sleep(2)
        print("IN RESPONSE")
        yield session.call("rie.dialogue.say_animated", text="We want to start with sitting down - follow my lead! Let me know when you're ready.")
        yield session.call("rom.optional.behavior.play", name="BlocklySitDown")

        text = yield session.call("rie.dialogue.stt.read")

        response = text[-1]['data']['body']['text']
        print("I heard ", response)

        ready = ["ready", "yes", "i'm ready", "let's go", "im done", "done"]

        if response in ready:
            print("SItting and ready to go")

    elif response in sitting:
        pass

    else:
        yield session.call("rie.dialogue.say_animated", text="I'm sorry, I didn't understand that. Let's try again.")
        do_exercises(session, details)

@inlineCallbacks
def sitting_exercises(session, details):
    yield session.call("rom.optional.behavior.play", name="BlocklySitDown")

    session.call("rom.actuator.motor.write",
                 frames=[{"time": 800, "data": {"body.legs.left.foot.roll": -0.2, "body.legs.right.foot.roll": 0.2}},
                         {"time": 1200, "data": {"body.legs.left.foot.roll": -0.2, "body.legs.right.foot.roll": 0.2}},
                         {"time": 1600, "data": {"body.legs.left.foot.roll": -0.2, "body.legs.right.foot.roll": 0.2}},
                         {"time": 2000, "data": {"body.legs.left.foot.roll": -0.2, "body.legs.right.foot.roll": 0.2}},
                         {"time": 2400, "data": {"body.legs.left.foot.roll": -0.2, "body.legs.right.foot.roll": 0.2}},
                         {"time": 2800, "data": {"body.legs.left.foot.roll": -0.2, "body.legs.right.foot.roll": 0.2}}],
                 force=True
                 )


    pass

@inlineCallbacks
def main(session, details):

    exercises = False
    finished_interaction = False


    yield session.call("rie.dialogue.config.language", lang="en")
    # yield session.call("rom.optional.behavior.play", name="BlocklyStand")

    # ask if user wants to do exercises
    # exercises, finished_interaction = yield ask_if_exercises(session, details, exercises)

    # print("HELLO")
    # print(exercises)

    # if exercises == True:
    #     do_exercises(session, details)

    sitting_exercises(session, details)

    while not finished_interaction:
        yield sleep(0.5)

    session.leave()  


wamp = Component(
    transports=[{
        "url": "ws://wamp.robotsindeklas.nl",
        "serializers": ["msgpack"],
        "max_retries": 0
    }],
    realm="rie.65f1b669d9eb6cfb396e87b2",
)

wamp.on_join(main)

if __name__ == "__main__":
    run([wamp])


# answer = yield session.call("rie.dialogue.ask",
#                         question="",
#                         answers="")

# yield session.call("rie.dialogue.stop")

# question2 = "Are you sure? It's going to be fun!"
# answers2 = {"yes": ["yes", "sure", "yeah", "ok"], "no": ["no", "not really", "i don't want to"]}

# answer2 = yield session.call("rie.dialogue.ask",
#                             question=question2,
#                             answers=answers2)
# print("TEST")
# print(answer2)

# yield sleep(2)
# if answer2 == "yes":
#     yield session.call("rie.dialogue.say_animated", text="I'm glad you changed your mind. Let's begin!")
#     exercises = True

# elif answer2 == "no":
#     yield session.call("rie.dialogue.say_animated", text="Okay, I understand - maybe next time")
#     exercises = False
#     finished_interaction = True

# yield session.call("rie.dialogue.stop")