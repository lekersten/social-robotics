from autobahn.twisted.component import Component, run
from twisted.internet.defer import inlineCallbacks

from database_functions import get_all_current_steps


def find_highest_priority_activity(current_steps):
    # Determine the step in a list that needs to be done first
    # print(current_steps, type(current_steps[0]))

    # First order based on date
    first_end_date = min([c for a,b,c in current_steps])
    need_done_first = [(a,b) for a,b,c in current_steps if c == first_end_date]
    # Then order based on priority
    highets_priority = min([b for a,b in need_done_first])
    chosen_task = [a for a,b in need_done_first if b == highets_priority]
    return chosen_task[0]


@inlineCallbacks
def suggest_activity(session, conn, date):
    current_steps = get_all_current_steps(conn, date)
    if not current_steps:
        return

    answers = {"yes": ["yes", "sure", "yeah", "of course"], "no": ["no", "nope", "definitely not", "not now"]}
    answer = yield session.call("rie.dialogue.ask", question="Do you have some free time right now?", answers=answers)

    if answer == "yes":
        # TODO: Find a smart way to choose what to suggest to do right now (Maybe ask how long they have beforehand?)
        task = yield find_highest_priority_activity(current_steps)
        yield session.call("rie.dialogue.say", text="Maybe you can start to "+task+"?")
    elif answer == "no":
        session.call("rie.dialogue.say", text="Okay, I'll ask again later.")
        yield session.call("rom.optional.behavior.play", name="BlocklyHappy")
    yield session.call("rie.dialogue.stop")


@inlineCallbacks
def main(session, details):
    from datetime import datetime
    from database_functions import create_connection

    conn = yield create_connection(r"db\pythonsqlite.db")
    date = yield str(datetime.now())[:10]

    yield suggest_activity(session, conn, date)

    session.leave()  # Close the connection with the robot


wamp = Component(
    transports=[{
        "url": "ws://wamp.robotsindeklas.nl",
        "serializers": ["msgpack"],
        "max_retries": 0
    }],
    realm="rie.65fc5b1da6c4715863c58d2a",
)

wamp.on_join(main)

if __name__ == "__main__":
    run([wamp])
