from autobahn.twisted.component import Component, run
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.util import sleep


@inlineCallbacks
def ask_if_exercises(session, details, exercises, finished_interaction):
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

        yield session.call("rie.dialogue.say_animated", text="Are you sure? It's going to be fun! Will you do some exercises with me?")

        text = yield session.call("rie.dialogue.stt.read")

        response = text[-1]['data']['body']['text']
        print("I heard ", response)

        if response == "":
            response = text[-1]['data']['body']['text']
            print("This time I heard ", response)

        yes = ["yes", "sure", "yeah", "okay", "definitely"]
        no = ["no", "not really", "i don't want to", "nah"]

        if response in yes:
            yield session.call("rie.dialogue.say_animated", text="I'm glad you changed your mind! Let's begin!")
            exercises = True
            finished_interaction = False

        elif response in no:
            yield session.call("rie.dialogue.say_animated", text="Okay, I understand - maybe next time")
            exercises = False
            finished_interaction = True

    return exercises, finished_interaction

@inlineCallbacks
def ask_if_sit_stand(session, details, position):

    ready = False

    question = "Are you already " + position + "?"
    yield session.call("rie.dialogue.say_animated", text=question)

    text = yield session.call("rie.dialogue.stt.read")

    answer = text[-1]['data']['body']['text']
    print("I heard ", answer)

    if answer == "":
        answer = text[-1]['data']['body']['text']
        print("This time I heard ", answer)

    yes = ["yes", "sure", "yeah", "ok", "definitely"]
    no = ["no", "not yet", "nah", "almost"]

    if answer in yes:
        ready = True

    elif answer in no:
        ready = False

    return ready

@inlineCallbacks
def do_exercises(session, details):

    yield session.call("rie.dialogue.say", text="Let's start by sitting down.")
    yield session.call("rom.optional.behavior.play", name="BlocklySitDown")

    ready = yield ask_if_sit_stand(session, details, "sitting")

    print(ready)

    if ready == True:
        yield session.call("rie.dialogue.say", text="Great! Now that we're sitting, let's start with some exercises.")
        yield sitting_exercises(session, details)

    else:
        yield session.call("rie.dialogue.say", text="No problem! I will wait a bit longer")
        yield sleep(5)
        yield sitting_exercises(session, details)

        

    yield sleep(2)
    yield session.call("rie.dialogue.say", text="You're doing great! Keep it up! And let's move onto standing exercises. Stand up when you're ready!")
    yield session.call("rom.optional.behavior.play", name="BlocklyStand")

    ready = yield ask_if_sit_stand(session, details, "standing")

    if ready == True:
        pass

    else:
        yield session.call("rie.dialogue.say", text="No problem! I will wait a bit longer")
        yield sleep(5)
        ready = yield ask_if_sit_stand(session, details, "standing")


    user_feeling = yield ask_feeling(session, details)

    if user_feeling == "good":
        yield session.call("rie.dialogue.say", text="Great! Then let's continue with some more exercises.")
        yield standing_exercises(session, details)
        
        yield sleep(2)
        finished_interaction = yield sign_off(session, details)

    elif user_feeling == "tired":
        yield session.call("rie.dialogue.say", text="I understand - maybe next time we can do some more exercises. For now, let's take a break.")
        finished_interaction = True

    return finished_interaction
    
@inlineCallbacks
def leg_extensions(session, details):

    yield session.call("rie.dialogue.say", text="Let's start with raising our legs. I will show you once and then we will do the rest together")

    yield session.call("rom.actuator.motor.write",
                    frames=[{"time": 1500, "data": {"body.legs.left.lower.pitch": -0.75, "body.legs.right.lower.pitch": 0}},
                            {"time": 3000, "data": {"body.legs.left.lower.pitch": 0, "body.legs.right.lower.pitch": 0}},
                            {"time": 4500, "data": {"body.legs.left.lower.pitch": 0, "body.legs.right.lower.pitch": -0.75}},
                            {"time": 6000, "data": {"body.legs.left.lower.pitch": 0, "body.legs.right.lower.pitch": 0}}],
                    force=True
                    )
    
    yield session.call("rie.dialogue.say", text="Now let's do 2 together - count with me!")

    for i in range(2):
        yield session.call("rie.dialogue.say", text=str(i + 1))
        yield session.call("rom.actuator.motor.write",
                    frames=[{"time": 1500, "data": {"body.legs.left.lower.pitch": -0.75, "body.legs.right.lower.pitch": 0}},
                            {"time": 3000, "data": {"body.legs.left.lower.pitch": 0, "body.legs.right.lower.pitch": 0}},
                            {"time": 4500, "data": {"body.legs.left.lower.pitch": 0, "body.legs.right.lower.pitch": -0.75}},
                            {"time": 6000, "data": {"body.legs.left.lower.pitch": 0, "body.legs.right.lower.pitch": 0}}],
                    force=True
                    )     

@inlineCallbacks
def toe_reaches(session, details):
    yield session.call("rie.dialogue.say", text="Now let's reach for our toes. I will show you once and then we will do the rest together")

    yield session.call("rom.actuator.motor.write",
                    frames=[{"time": 1500, "data": {"body.legs.left.upper.pitch": -1.7, "body.legs.right.upper.pitch": -1.7, "body.arms.left.upper.pitch": -1, "body.arms.right.upper.pitch": -1}},
                            {"time": 3000, "data": {"body.legs.left.upper.pitch": -1.4, "body.legs.right.upper.pitch": -1.4, "body.arms.left.upper.pitch": -1, "body.arms.right.upper.pitch": -1}},
                            {"time": 4500, "data": {"body.legs.left.upper.pitch": -1.4, "body.legs.right.upper.pitch": -1.4, "body.arms.left.upper.pitch": -1, "body.arms.right.upper.pitch": -1}},],
                        force=True
                    )
    
    yield session.call("rie.dialogue.say", text="Now let's do 2 together - count with me!")

    for i in range(2):
        yield session.call("rie.dialogue.say", text=str(i + 1))
        yield session.call("rom.actuator.motor.write",
                    frames=[{"time": 1500, "data": {"body.legs.left.upper.pitch": -1.7, "body.legs.right.upper.pitch": -1.7, "body.arms.left.upper.pitch": -1, "body.arms.right.upper.pitch": -1}},
                            {"time": 3000, "data": {"body.legs.left.upper.pitch": -1.4, "body.legs.right.upper.pitch": -1.4, "body.arms.left.upper.pitch": -1, "body.arms.right.upper.pitch": -1}},],
                    force=True
                            )
        
    yield session.call("rom.actuator.motor.write",
                frames=[{"time": 1500, "data": {"body.legs.left.upper.pitch": -1.4, "body.legs.right.upper.pitch": -1.4, "body.arms.left.upper.pitch": -1, "body.arms.right.upper.pitch": -1}},],
                force=True
                )
        
@inlineCallbacks
def twist_body(session, details):
    yield session.call("rie.dialogue.say", text="Next were going to twist our body. I will show you once and then again we will do the rest together")

    yield session.call("rom.actuator.motor.write",
                        frames=[{"time": 1500, "data": {"body.torso.yaw": -0.7, "body.arms.left.upper.pitch": -1, "body.arms.right.upper.pitch": -1}},
                                {"time": 3000, "data": {"body.torso.yaw": 0, "body.arms.left.upper.pitch": -1, "body.arms.right.upper.pitch": -1}},
                                {"time": 4500, "data": {"body.torso.yaw": 0.7, "body.arms.left.upper.pitch": -1, "body.arms.right.upper.pitch": -1}},
                                {"time": 6000, "data": {"body.torso.yaw": 0, "body.arms.left.upper.pitch": -1, "body.arms.right.upper.pitch": -1}},],
                        force=True
                        )
    
    yield session.call("rie.dialogue.say", text="Now let's do 2 together - count with me!")

    for i in range(2):
        yield session.call("rie.dialogue.say", text=str(i + 1))
        yield session.call("rom.actuator.motor.write",
                        frames=[{"time": 1500, "data": {"body.torso.yaw": -0.7, "body.arms.left.upper.pitch": -1, "body.arms.right.upper.pitch": -1}},
                                {"time": 3000, "data": {"body.torso.yaw": 0, "body.arms.left.upper.pitch": -1, "body.arms.right.upper.pitch": -1}},
                                {"time": 4500, "data": {"body.torso.yaw": 0.7, "body.arms.left.upper.pitch": -1, "body.arms.right.upper.pitch": -1}},
                                {"time": 6000, "data": {"body.torso.yaw": 0, "body.arms.left.upper.pitch": -1, "body.arms.right.upper.pitch": -1}},],
                        force=True
                        )

    yield session.call("rom.actuator.motor.write",
                        frames=[{"time": 1500, "data": {"body.torso.yaw": 0, "body.arms.left.upper.pitch": -1, "body.arms.right.upper.pitch": -1}}],
                        force=True
                        )

@inlineCallbacks
def sitting_exercises(session, details):

    yield leg_extensions(session, details)
    
    yield sleep(2)
    yield session.call("rie.dialogue.say", text="I hope youre feeling amazing! Now let's move on.")
    yield toe_reaches(session, details)

    yield sleep(2)
    yield session.call("rie.dialogue.say", text="Great work! Let's do the last sitting exercise.")
    yield twist_body(session, details)

    pass

@inlineCallbacks
def raise_arms(session,  details):
    yield session.call("rie.dialogue.say", text="Let's begin with raising our arms one at a time. I will show you once and then again we will do the rest together")

    yield session.call("rom.actuator.motor.write",
                        frames=[{"time": 2000, "data": {"body.arms.left.upper.pitch": -2.4, "body.arms.right.upper.pitch": 0}},
                                {"time": 4000, "data": {"body.arms.left.upper.pitch": 0, "body.arms.right.upper.pitch": 0}},
                                {"time": 6000, "data": {"body.arms.left.upper.pitch": 0, "body.arms.right.upper.pitch": -2.4}},
                                {"time": 8000, "data": {"body.arms.left.upper.pitch": 0, "body.arms.right.upper.pitch": 0}},],
                        force=True
                        )
    
    yield session.call("rie.dialogue.say", text="Now let's do 2 together - count with me!")

    for i in range(2):
        yield session.call("rie.dialogue.say", text=str(i + 1))
        yield session.call("rom.actuator.motor.write",
                        frames=[{"time": 2000, "data": {"body.arms.left.upper.pitch": -2.4, "body.arms.right.upper.pitch": 0}},
                                {"time": 4000, "data": {"body.arms.left.upper.pitch": 0, "body.arms.right.upper.pitch": 0}},
                                {"time": 6000, "data": {"body.arms.left.upper.pitch": 0, "body.arms.right.upper.pitch": -2.4}},
                                {"time": 8000, "data": {"body.arms.left.upper.pitch": 0, "body.arms.right.upper.pitch": 0}},],
                        force=True
                        )
        
    yield session.call("rie.dialogue.say", text="Now let's raise both arms together and keep them here for a few seconds!")
    yield session.call("rom.actuator.motor.write",
                        frames=[{"time": 2000, "data": {"body.arms.left.upper.pitch": -2.4, "body.arms.right.upper.pitch": -2.4}},
                                {"time": 6000, "data": {"body.arms.left.upper.pitch": -2.4, "body.arms.right.upper.pitch": -2.4}},
                                {"time": 8000, "data": {"body.arms.left.upper.pitch": 0, "body.arms.right.upper.pitch": 0}},],
                        force=True
                        )
    
@inlineCallbacks
def stretch_elbow(session, details):
    yield session.call("rie.dialogue.say", text="Now let's stretch our elbows. I will show you once and then again we will do the rest together")

    yield session.call("rom.actuator.motor.write",
                        frames=[{"time": 2000, "data": {"body.arms.left.upper.pitch": -1.5, "body.arms.right.upper.pitch": -1.5}},],
                                force=True
                                )

    yield session.call("rom.actuator.motor.write",
                        frames=[{"time": 2000, "data": {"body.arms.left.lower.roll": -1.5, "body.arms.right.lower.roll": -1.5}},
                                {"time": 4000, "data": {"body.arms.left.lower.roll": 0, "body.arms.right.lower.roll": 0}},
                                ],
                        force=True
                        )
    
    yield session.call("rie.dialogue.say", text="Now let's do 2 together - count with me!")

    for i in range(2):
        yield session.call("rie.dialogue.say", text=str(i + 1))
        yield session.call("rom.actuator.motor.write",
                        frames=[{"time": 2000, "data": {"body.arms.left.lower.roll": -1.5, "body.arms.right.lower.roll": -1.5}},
                                {"time": 4000, "data": {"body.arms.left.lower.roll": 0, "body.arms.right.lower.roll": 0}},
                                ],
                        force=True
                        )

    yield session.call("rom.optional.behavior.play", name="BlocklyStand")

@inlineCallbacks
def neck_side_to_side(session, details):
    yield session.call("rie.dialogue.say", text="Let's slowly turn our heads from side to side. I will show you once and then again we will do the rest together")

    yield session.call("rom.actuator.motor.write",
                    frames=[{"time": 3000, "data": {"body.head.yaw": 0.8}},
                            {"time": 5000, "data": {"body.head.yaw": 0.8}},
                            {"time": 8000, "data": {"body.head.yaw": -0.8}},
                            {"time": 10000, "data": {"body.head.yaw": -0.8}},
                            {"time": 13000, "data": {"body.head.yaw": 0.0}}],
                    force=True
                    )
    
    yield session.call("rie.dialogue.say", text="Now let's do 2 together - count with me!")

    for i in range(2):
        yield session.call("rie.dialogue.say", text=str(i + 1))
        yield session.call("rom.actuator.motor.write",
                    frames=[{"time": 3000, "data": {"body.head.yaw": 0.8}},
                            {"time": 5000, "data": {"body.head.yaw": 0.8}},
                            {"time": 8000, "data": {"body.head.yaw": -0.8}},
                            {"time": 10000, "data": {"body.head.yaw": -0.8}},
                            {"time": 13000, "data": {"body.head.yaw": 0.0}}],
                    force=True
                    )

@inlineCallbacks
def tilt_head(session, details):

    yield session.call("rie.dialogue.say", text="Let's tilt our heads from side to side. Watch me and then we will do it together")

    yield session.call("rom.actuator.motor.write",
                    frames=[{"time": 3000, "data": {"body.head.roll": 0.17}},
                            {"time": 6000, "data": {"body.head.roll": -0.17}},
                            {"time": 9000, "data": {"body.head.roll": 0}},],
                    force=True
                    )
    
    yield session.call("rie.dialogue.say", text="Now let's do 2 together - count with me!")

    for i in range(2):
        yield session.call("rie.dialogue.say", text=str(i + 1))
        yield session.call("rom.actuator.motor.write",
                    frames=[{"time": 2000, "data": {"body.head.roll": 0.17}},
                            {"time": 4000, "data": {"body.head.roll": 0.17}},
                            {"time": 6000, "data": {"body.head.roll": -0.17}},
                            {"time": 8000, "data": {"body.head.roll": -0.17}},
                            ],
                    force=True
                    )
        
    yield session.call("rom.actuator.motor.write",
                       frames=[{"time": 2000, "data": {"body.head.roll": 0}},],
                               force=True
                    )
    
@inlineCallbacks
def lift_head(session, details):
    yield session.call("rie.dialogue.say", text="Let's lift our heads up and down. I will show you once and then again we will do the rest together")

    yield session.call("rom.actuator.motor.write",
                    frames=[{"time": 3000, "data": {"body.head.pitch": -0.17}},
                            {"time": 6000, "data": {"body.head.pitch": 0.17}},
                            {"time": 9000, "data": {"body.head.pitch": 0}},],
                    force=True
                    )
    
    yield session.call("rie.dialogue.say", text="Now let's do 2 together - count with me!")

    for i in range(2):
        yield session.call("rie.dialogue.say", text=str(i + 1))
        yield session.call("rom.actuator.motor.write",
                    frames=[{"time": 2000, "data": {"body.head.pitch": -0.17}},
                            {"time": 4000, "data": {"body.head.pitch": -0.17}},
                            {"time": 6000, "data": {"body.head.pitch": 0.17}},
                            {"time": 8000, "data": {"body.head.pitch": 0.17}},
                            ],
                    force=True
                    )
        
    yield session.call("rom.actuator.motor.write",
                       frames=[{"time": 2000, "data": {"body.head.pitch": 0}},],
                               force=True
                    )

@inlineCallbacks
def neck_exercises(session, details):
    yield neck_side_to_side(session, details)

    yield sleep(2)
    yield tilt_head(session, details)
    
    yield sleep(2)
    yield lift_head(session, details)

@inlineCallbacks
def touch_toes(session, details):
    yield session.call("rie.dialogue.say", text="Let's try and touch out toes. I will show you once and then we can do two together")
    yield session.call("rom.optional.behavior.play", name="BlocklyTouchToes")

    yield session.call("rie.dialogue.say", text="Now let's do 2 together - count with me!")
    for i in range(2):
        yield session.call("rie.dialogue.say", text=str(i + 1))
        yield session.call("rom.optional.behavior.play", name="BlocklyTouchToes")

@inlineCallbacks
def standing_exercises(session, details):

    yield raise_arms(session, details)
    
    yield sleep(2)
    yield stretch_elbow(session, details)
    
    yield sleep(2)
    yield session.call("rie.dialogue.say", text="You're doing great! Now let's stretch our neck carefully.")
    yield neck_exercises(session, details)

    yield sleep(2)
    yield touch_toes(session, details)
        
    pass

@inlineCallbacks   
def ask_feeling(session, details):
    question = "Great! Now that we're standing, how do you feel? Are you feeling good and want to continue or tired and want to stop?"
    answers = {"good": ["good", "great", "okay", "amazing", "fine", "alright", "continue"], "tired": ["bad", "stop", "tired", "exhausted", "not good"]}

    answer = yield session.call("rie.dialogue.ask",
                                question=question,
                                answers=answers)

    print(answer)
    
    yield session.call("rie.dialogue.stop")
    
    return answer

@inlineCallbacks
def sign_off(session, details):
    yield session.call("rie.dialogue.say", text="Great job today! I hope you are feeling better. I'll see you next time! Enjoy the rest of your day!")
    
    finished_interaction = True
    
    return finished_interaction

@inlineCallbacks
def main(session, details):

    exercises = False
    finished_interaction = False

    yield session.call("rie.dialogue.config.language", lang="en")
    yield session.call("rom.optional.behavior.play", name="BlocklyStand")

    # ask if user wants to do exercises
    exercises, finished_interaction = yield ask_if_exercises(session, details, exercises, finished_interaction)

    if exercises == True:
        finished_interaction = yield do_exercises(session, details)

    while not finished_interaction:
        yield sleep(0.5)

    session.leave()  


wamp = Component(
    transports=[{
        "url": "ws://wamp.robotsindeklas.nl",
        "serializers": ["msgpack"],
        "max_retries": 0
    }],
    realm="rie.65f82ce7a6c4715863c5767a",
)

wamp.on_join(main)

if __name__ == "__main__":
    run([wamp])
