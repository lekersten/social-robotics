from autobahn.twisted.component import Component, run
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.util import sleep

from datetime import datetime

from database_functions import create_connection
from suggest_activity import suggest_activity
from answer_question import answer_question

from exercise_process import exercises_main


conn = create_connection(f"db\pythonsqlite.db")
date = str(datetime.now())[:10]


@inlineCallbacks
def main(session, details):
    # Can be used to change the date to make sure that there is something in the database
    # global date
    # date = "2024-03-28"

    # set language to English (use 'nl' for Dutch)
    yield session.call("rie.dialogue.config.language", lang="en")
    # prompt from the robot to indicate that it started
    yield session.call("rie.dialogue.say", text="Robot started!")

    # yield exercises_main(session, details)

    yield suggest_activity(session, conn, date)

    yield answer_question(session, details, conn, date)

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
