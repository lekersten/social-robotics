from autobahn.twisted.component import Component, run
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.util import sleep

@inlineCallbacks
def main(session, details):
	question = "Is Paul a good prof?"
	answers = {"yes": ["yes", "sure", "yeah"], "super": ["super", "the best", "definitely"]}

	answer = yield session.call("rie.dialogue.ask",
								  question=question,
								  answers=answers)

	if answer == "yes":
		yield session.call("rie.dialogue.say_animated",
						   text="Good to hear that you think Paul is a good prof. I agree")
	elif answer == "super":
		session.call("rie.dialogue.say",
					 text="Great. Paul is indeed a super-duper prof")
		yield session.call("rom.optional.behavior.play",name="BlocklyHappy")
	else:
		yield session.call("rie.dialogue.say",
						   text="Sorry. What did you say? Be positive about Paul")
	yield session.call("rie.dialogue.stop")

	session.leave() # Close the connection with the robot

wamp = Component(
	transports=[{
		"url": "ws://wamp.robotsindeklas.nl",
		"serializers": ["msgpack"],
		"max_retries": 0
	}],
	realm="rie.65c4b794c01d7b660046f10a",
)

wamp.on_join(main)

if __name__ == "__main__":
	run([wamp])