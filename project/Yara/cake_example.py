from autobahn.twisted.component import Component, run
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.util import sleep

global sess, keyword


@inlineCallbacks
def on_keyword(frame):
    global sess, keyword
    c = frame["data"]["body"]["certainty"]
    print("certainty", c, ": ", frame)
    if "certainty" in frame["data"]["body"] and frame["data"]["body"]["certainty"] > 0.45:
        word = frame["data"]["body"]["text"]
        keyword = word
        yield sess.call("rie.dialogue.say_animated", text="Heard a keyword!")


@inlineCallbacks
def answer_keyword_question(session, details):
    # TODO: Get list from database (whatever I use for that)
    if keyword == "cake":
        list = [["Prepare the batter", True], ["Put the cake in the oven", False],
                ["Take the cake out of the oven", False]]
    elif keyword == "vacation":
        list = [["Pack your bags", True], ["Print your travel info", False], ["Leave on the 5th of April", False]]
    else:
        yield sess.call("rie.dialogue.say_animated", text="I'm sorry, I don't know anything about this.")
        return

    # Things that are done
    completed_items = [a for a, b in list if b is True]
    if len(completed_items) == 0:
        yield sess.call("rie.dialogue.say_animated", text="Nothing from this list is done yet. Do you want to start now?")
    elif len(completed_items) == len(list):
        yield sess.call("rie.dialogue.say_animated", text="Everything is already done for this! Do you want me to repeat every step?")
    else:
        yield sess.call("rie.dialogue.say_animated", text="The things that you have already done are:")
        for item in completed_items:
            yield sess.call("rie.dialogue.say_animated", text=item)

    # TODO: Specific question about what is done


@inlineCallbacks
def suggest_activity(session, details):
    print("Suggest activity!")
    answers = {"yes": ["yes", "sure", "yeah"], "no": ["no", "nope", "definitely not", "not now"]}

    answer = yield session.call("rie.dialogue.ask", question="Do you have some free time right now?", answers=answers)

    if answer == "yes":
        # TODO: Find a smart way to choose what to suggest to do right now (Maybe ask how long they have beforehand?)
        yield session.call("rie.dialogue.say_animated", text="Yes")
    elif answer == "no":
        session.call("rie.dialogue.say", text="Okay, I'll ask again later.")
        yield session.call("rom.optional.behavior.play", name="BlocklyHappy")
    else:
        yield session.call("rie.dialogue.say", text="Sorry, I couldn't understand what you said.")
    yield session.call("rie.dialogue.stop")

    # yield sess.call("rie.dialogue.say_animated", text="")


@inlineCallbacks
def main(session, details):
    global sess, keyword
    keyword = None
    sess = session

    yield session.call("rie.dialogue.config.language", lang="en")
    yield session.call("rie.dialogue.keyword.language", lang="en")

    # TODO: insert some random behavior while robot waits for input

    # # Randomly when used? Ask if user has free time, using word recognition
    # # TODO: maybe find a better moment for when the robot gives a suggestion?
    # yield suggest_activity(session, details)

    # Listen during conversation (LLM?) to figure out whether user wants to know/do something from a list
    print("Start keyword listening.")
    yield session.call("rie.dialogue.keyword.add", keywords=["cake", "vacation", "yes", "no"])
    yield session.subscribe(on_keyword, "rie.dialogue.keyword.stream")
    yield session.call("rie.dialogue.keyword.stream")
    # TODO: think of some better way for the user to start this interaction
    #  (not robot continuously trying to talk about it during normal conversation)
    yield session.call("rie.dialogue.keyword.remove", keywords=["yes", "no"])
    print(session.call("rie.dialogue.keyword.info"))
    keyword = "vacation"
    while keyword is None:
        # print("SLEEP")
        yield sleep(0.5)
    print(keyword)
    if keyword is not None:
        yield answer_keyword_question(session, details)

    print("After keyword part")

    # session.leave()  # Close the connection with the robot


wamp = Component(
    transports=[{
        "url": "ws://wamp.robotsindeklas.nl",
        "serializers": ["msgpack"],
        "max_retries": 0
    }],
    realm="rie.65f1b4ddd9eb6cfb396e87a8",
)

wamp.on_join(main)

if __name__ == "__main__":
    run([wamp])
