from autobahn.twisted.component import Component, run
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.util import sleep

import exercises 

reps = 3 # default repetitions
tired = False

@inlineCallbacks
def sign_off(session, details):

    session.call("rom.optional.behavior.play", name="BlocklyWaveRightArm")
    yield session.call("rie.dialogue.say", text="Amazing job today! I hope you are feeling better. I'll see you next time! Enjoy the rest of your day!")
    
    finished_interaction = True
    
    return finished_interaction


@inlineCallbacks   
def ask_feeling(session, details):
    question = "Now that we're standing, how do you feel? Are you feeling good and want to continue or do you want to stop?"

    yield session.call("rie.dialogue.say_animated", text=question)

    text = yield session.call("rie.dialogue.stt.read")

    answer = text[-1]['data']['body']['text']
    print(answer)

    if answer == "":
        text = yield session.call("rie.dialogue.stt.read")
        answer = text[-1]['data']['body']['text']
        print("This time I heard ", answer)

    good = ["good", "great", "okay", "amazing", "fine", "alright", "continue", "g"]
    tired = ["bad", "stop", "tired", "exhausted", "not good", "t"]

    if answer in good:
        feeling = "good"

    elif answer in tired:
        feeling = "tired"

    else:
        yield session.call("rie.dialogue.say_animated", text="I didn't quite catch that. I will ask again?")
        feeling = yield ask_feeling(session, details)

    return feeling


@inlineCallbacks
def ask_if_ready(session, details):

    question = "Are you ready now?"
    yield session.call("rie.dialogue.say_animated", text=question)

    text = yield session.call("rie.dialogue.stt.read")

    answer = text[-1]['data']['body']['text']
    print(answer)

    if answer == "":
        text = yield session.call("rie.dialogue.stt.read")
        answer = text[-1]['data']['body']['text']
        print("This time I heard ", answer)

    yes = ["yes", "sure", "yeah", "ready", "im ready"]
    no = ["no", "not yet", "nah", "almost"]

    if answer in yes:
        pass

    elif answer in no:
        yield session.call("rie.dialogue.say", text="That's okay! I can wait some more.")
        yield sleep(5)
        yield session.call("rie.dialogue.say", text="Okay - let's begin")


@inlineCallbacks
def ask_if_sit_stand(session, details, position):

    ready = False

    question = "Are you already " + position + "?"
    yield session.call("rie.dialogue.say_animated", text=question)

    text = yield session.call("rie.dialogue.stt.read")

    answer = text[-1]['data']['body']['text']
    print(answer)

    if answer == "":
        text = yield session.call("rie.dialogue.stt.read")
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
def get_ready_sitting(session, details):
    yield session.call("rie.dialogue.say", text="Let's start by sitting down.")
    yield session.call("rom.optional.behavior.play", name="BlocklySitDown")

    ready = yield ask_if_sit_stand(session, details, "sitting")

    if ready == True:
        pass

    else:
        yield session.call("rie.dialogue.say", text="No problem! I will wait a bit longer")
        yield sleep(5)

        yield ask_if_ready(session, details)


@inlineCallbacks
def sitting_exercises(session, details):

    yield exercises.leg_extensions(session, details, reps)
    
    yield sleep(2)
    yield session.call("rie.dialogue.say", text="I hope youre feeling amazing! Let's move on.")
    yield exercises.toe_reaches(session, details, reps)

    yield sleep(2)
    yield session.call("rie.dialogue.say", text="Great work! Let's do the last sitting exercise.")
    yield exercises.twist_body(session, details, reps)


@inlineCallbacks
def get_ready_standing(session, details):
    yield session.call("rie.dialogue.say", text="You're doing great! Keep it up! And let's move onto standing exercises. Stand up when you're ready!")
    yield session.call("rom.optional.behavior.play", name="BlocklyStand")

    ready = yield ask_if_sit_stand(session, details, "standing")

    if ready == True:
        pass

    else:
        yield session.call("rie.dialogue.say", text="No problem! I will wait a bit longer")
        yield sleep(5)

        yield ask_if_ready(session, details)


@inlineCallbacks
def standing_exercises(session, details):

    yield session.call("rom.optional.behavior.play", name="BlocklyStand")

    yield exercises.raise_arms(session, details, reps)
    
    yield sleep(2)
    yield exercises.stretch_elbow(session, details, reps)
    
    yield sleep(2)
    yield session.call("rie.dialogue.say", text="You're doing great! Now let's do some stretches for our necks.")
    yield exercises.neck_exercises(session, details, reps)

    yield sleep(2)
    yield exercises.touch_toes(session, details, reps)


@inlineCallbacks
def do_exercises(session, details):
    global reps, changed

    @inlineCallbacks
    def tired(frames):
        global tired, reps

        changed = False 
        if frames['data']['body']['final']:
            tired = ["tired", "t", "im tired", "I'm tired"]

            if frames["data"]["body"]["text"] in tired:
                print(frames["data"]["body"]["text"])
                tired = True
            
        if tired == True:
            if changed == False:
                changed = True
                print("User is tired.")
                yield session.call("rie.dialogue.stt.close")

                reps = max(round(reps / 2), 1)
            
                text = "I understand, you're tired. Let's only do " + str(reps) + "repetitions now."
                yield session.call("rie.dialogue.say", text=text)
                
            print("Reduced reps to ", reps)


    # sitting exercises
    yield get_ready_sitting(session, details)
    yield session.call("rie.dialogue.say", text="Great! Now that we're sitting, let's start with some exercises.")

    yield session.subscribe(tired, "rie.dialogue.stt.stream")
    yield session.call("rie.dialogue.stt.stream")

    yield sitting_exercises(session, details)


    # standing exercises
    yield sleep(2)
    yield get_ready_standing(session, details)

    user_feeling = yield ask_feeling(session, details)
    print(user_feeling)

    if user_feeling == "good":
        yield session.call("rie.dialogue.say", text="Great! Then let's continue with some more exercises.")

        yield session.call("rie.dialogue.stt.stream")
        
        yield standing_exercises(session, details)

        
        yield sleep(2)
        finished_interaction = yield sign_off(session, details)

    elif user_feeling == "tired":

        yield session.call("rie.dialogue.say", text="I understand, you did great! Maybe next time we can do some more exercises. For now, let's take a break. I'll see you later")
        finished_interaction = True

    return finished_interaction
    

@inlineCallbacks   
def ask_energy(session, details):

    global reps 

    question = "How are you feeling today? Are you feeling good and energetic or a bit tired?"

    yield session.call("rie.dialogue.say_animated", text=question)

    text = yield session.call("rie.dialogue.stt.read")

    answer = text[-1]['data']['body']['text']
    print(answer)

    if answer == "":
        text = yield session.call("rie.dialogue.stt.read")
        answer = text[-1]['data']['body']['text']
        print("This time I heard ", answer)

    good = ["energetic", "great", "amazing", "good"]
    tired = ["tired", "exhausted", "not good", "bad"]

    if answer in good:
        yield session.call("rie.dialogue.say_animated", text="That's nice to hear! Let's do 5 repetitions for each exercise!")
        reps = 5

    elif answer in tired:
        yield session.call("rie.dialogue.say_animated", text="No worries, we'll take it easy! Let's do 2 repetitions for each exercise.")
        reps = 2

    else:
        yield session.call("rie.dialogue.say_animated", text="Why don't we do 3 repetitions for each exercise?")
        reps = 3


@inlineCallbacks
def ask_if_exercises(session, details, exercises, finished_interaction):

    question = "Would you like to do some exercises?"

    yield session.call("rie.dialogue.say_animated", text=question)

    text = yield session.call("rie.dialogue.stt.read")

    answer = text[-1]['data']['body']['text']
    print(answer)

    if answer == "":
        text = yield session.call("rie.dialogue.stt.read")
        answer = text[-1]['data']['body']['text']
        print("This time I heard ", answer)

    yes = ["yes", "sure", "yeah", "ok", "definitely", "I would"] 
    no = ["no", "not really", "i don't want to"]

    if answer in yes:
        yield session.call("rie.dialogue.say_animated", text="Great! This is going to be fun!")
        exercises = True

    elif answer in no:

        yield session.call("rie.dialogue.say_animated", text="Are you sure? It's going to be fun! Will you do some exercises with me?")

        text = yield session.call("rie.dialogue.stt.read")

        response = text[-1]['data']['body']['text']
        print(response)

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
def exercises_main(session, details):

    exercises = False
    finished_interaction = False

    yield session.call("rie.dialogue.config.language", lang="en")
    yield session.call("rom.optional.behavior.play", name="BlocklyStand")

    # ask if user wants to do exercises
    exercises, finished_interaction = yield ask_if_exercises(session, details, exercises, finished_interaction)

    if exercises == True:
         # ask user energy to determine repetitions - default is 3
        yield ask_energy(session, details)
        finished_interaction = yield do_exercises(session, details)

    while not finished_interaction:
        yield sleep(0.5)


@inlineCallbacks
def main(session, details):

    yield exercises_main(session, details)

    session.leave()  


wamp = Component(
    transports=[{
        "url": "ws://wamp.robotsindeklas.nl",
        "serializers": ["msgpack"],
        "max_retries": 0
    }],
    realm="rie.66014f75a6c4715863c5a3f4",
)

wamp.on_join(main)

if __name__ == "__main__":
    run([wamp])
