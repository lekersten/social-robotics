from autobahn.twisted.component import Component, run
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.util import sleep

from answer_question import answer_question

@inlineCallbacks
def main(session, details):
    global finish_dialogue, question, question_topics
    # set language to English (use 'nl' for Dutch)
    yield session.call("rie.dialogue.config.language", lang="en")
    # prompt from the robot to indicate that it started
    yield session.call("rie.dialogue.say", text="Robot started!")

    # TODO: function Lauren

    # TODO: function Yara (suggest something)

    yield answer_question(session, details)

    session.leave()


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