from autobahn.twisted.component import Component, run
from twisted.internet.defer import inlineCallbacks


@inlineCallbacks
def main(session, details):
	yield session.call("rom.optional.behavior.play", name="BlocklyStand")
	session.call("rie.dialogue.say", text="I am singing! Laa, laa, laa!")
	yield session.call("rom.actuator.motor.write",
		frames=[{"time": 2000, "data": {"body.arms.left.upper.pitch": -4, 
           							  "body.arms.right.upper.pitch": -1.5,
           								"body.arms.left.lower.roll": 0.5,
                   						"body.arms.right.lower.roll": -1.5}},
				{"time": 2500, "data": {"body.arms.left.upper.pitch": -3, 
           							  "body.arms.right.upper.pitch": -1.5,
           								"body.arms.left.lower.roll": 0.5,
                   						"body.arms.right.lower.roll": -1.5,
                         				"body.head.pitch": 0.1}},
    			{"time": 3000, "data": {"body.arms.left.upper.pitch": -3, 
           							  "body.arms.right.upper.pitch": -1.5,
           								"body.arms.left.lower.roll": 0.5,
                   						"body.arms.right.lower.roll": -1.5,
                         				"body.head.pitch": -0.1}},
           		{"time": 3500, "data": {"body.arms.left.upper.pitch": -3, 
           							  "body.arms.right.upper.pitch": -1.5,
           								"body.arms.left.lower.roll": 0.5,
                   						"body.arms.right.lower.roll": -1.5,
                         				"body.head.pitch": 0.1}},
                {"time": 3500, "data": {"body.arms.left.upper.pitch": -3, 
           							  "body.arms.right.upper.pitch": -1.5,
           								"body.arms.left.lower.roll": 0.5,
                   						"body.arms.right.lower.roll": -1.5,
                         				"body.head.pitch": 0.0}}

            ],
		force=True
	)
	yield session.call("rom.optional.behavior.play", name="BlocklyStand")
	session.leave()


wamp = Component(
	transports=[{
		"url": "ws://wamp.robotsindeklas.nl",
		"serializers": ["msgpack"],
		"max_retries": 0
	}],
	realm="rie.65e8801fd9eb6cfb396e5570",
)

wamp.on_join(main)

if __name__ == "__main__":
	run([wamp])