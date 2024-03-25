from autobahn.twisted.component import Component, run
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.util import sleep


@inlineCallbacks
def leg_extensions(session, details, reps):

    yield session.call("rie.dialogue.say", text="We'll start with raising our legs. I will show you once and then we will do the rest together")

    yield session.call("rom.actuator.motor.write",
                    frames=[{"time": 1500, "data": {"body.legs.left.lower.pitch": -0.75, "body.legs.right.lower.pitch": 0}},
                            {"time": 3000, "data": {"body.legs.left.lower.pitch": 0, "body.legs.right.lower.pitch": 0}},
                            {"time": 4500, "data": {"body.legs.left.lower.pitch": 0, "body.legs.right.lower.pitch": -0.75}},
                            {"time": 6000, "data": {"body.legs.left.lower.pitch": 0, "body.legs.right.lower.pitch": 0}}],
                    force=True
                    )
    
    text = "Now let's do " + str(reps) + " together - count with me!"
    yield session.call("rie.dialogue.say", text=text)

    for i in range(reps):
        yield session.call("rie.dialogue.say", text=str(i + 1))
        yield session.call("rom.actuator.motor.write",
                    frames=[{"time": 1500, "data": {"body.legs.left.lower.pitch": -0.75, "body.legs.right.lower.pitch": 0}},
                            {"time": 3000, "data": {"body.legs.left.lower.pitch": 0, "body.legs.right.lower.pitch": 0}},
                            {"time": 4500, "data": {"body.legs.left.lower.pitch": 0, "body.legs.right.lower.pitch": -0.75}},
                            {"time": 6000, "data": {"body.legs.left.lower.pitch": 0, "body.legs.right.lower.pitch": 0}}],
                    force=True
                    )     


@inlineCallbacks
def toe_reaches(session, details, reps):
    yield session.call("rie.dialogue.say", text="Now let's reach for our toes. I will show you once and then again we will do the rest together")

    yield session.call("rom.actuator.motor.write",
                    frames=[{"time": 1500, "data": {"body.legs.left.upper.pitch": -1.7, "body.legs.right.upper.pitch": -1.7, "body.arms.left.upper.pitch": -1, "body.arms.right.upper.pitch": -1}},
                            {"time": 3000, "data": {"body.legs.left.upper.pitch": -1.4, "body.legs.right.upper.pitch": -1.4, "body.arms.left.upper.pitch": -1, "body.arms.right.upper.pitch": -1}},
                            {"time": 4500, "data": {"body.legs.left.upper.pitch": -1.4, "body.legs.right.upper.pitch": -1.4, "body.arms.left.upper.pitch": -1, "body.arms.right.upper.pitch": -1}},],
                        force=True
                    )
    
    text = "Let's do " + str(reps) + " together!"
    yield session.call("rie.dialogue.say", text=text)

    for i in range(reps):
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
def twist_body(session, details, reps):
    yield session.call("rie.dialogue.say", text="Next were going to twist our body. This will feel great! Like before, first I'll show you and then we can do the rest together")

    yield session.call("rom.actuator.motor.write",
                        frames=[{"time": 1500, "data": {"body.torso.yaw": -0.7, "body.arms.left.upper.pitch": -1, "body.arms.right.upper.pitch": -1}},
                                {"time": 3000, "data": {"body.torso.yaw": 0, "body.arms.left.upper.pitch": -1, "body.arms.right.upper.pitch": -1}},
                                {"time": 4500, "data": {"body.torso.yaw": 0.7, "body.arms.left.upper.pitch": -1, "body.arms.right.upper.pitch": -1}},
                                {"time": 6000, "data": {"body.torso.yaw": 0, "body.arms.left.upper.pitch": -1, "body.arms.right.upper.pitch": -1}},],
                        force=True
                        )
    
    text = "Now let's do " + str(reps) + " together - count with me!"
    yield session.call("rie.dialogue.say", text=text)

    for i in range(reps):
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
def raise_arms(session,  details, reps):
    yield session.call("rie.dialogue.say", text="Let's begin with raising our arms one at a time. I will show you and then again we will do the rest together")

    yield session.call("rom.actuator.motor.write",
                        frames=[{"time": 2000, "data": {"body.arms.left.upper.pitch": -2.4, "body.arms.right.upper.pitch": 0}},
                                {"time": 4000, "data": {"body.arms.left.upper.pitch": 0, "body.arms.right.upper.pitch": 0}},
                                {"time": 6000, "data": {"body.arms.left.upper.pitch": 0, "body.arms.right.upper.pitch": -2.4}},
                                {"time": 8000, "data": {"body.arms.left.upper.pitch": 0, "body.arms.right.upper.pitch": 0}},],
                        force=True
                        )
    
    text = "Now let's do " + str(reps) + " together!"
    yield session.call("rie.dialogue.say", text=text)

    for i in range(reps):
        yield session.call("rie.dialogue.say", text=str(i + 1))
        yield session.call("rom.actuator.motor.write",
                        frames=[{"time": 2000, "data": {"body.arms.left.upper.pitch": -2.4, "body.arms.right.upper.pitch": 0}},
                                {"time": 4000, "data": {"body.arms.left.upper.pitch": 0, "body.arms.right.upper.pitch": 0}},
                                {"time": 6000, "data": {"body.arms.left.upper.pitch": 0, "body.arms.right.upper.pitch": -2.4}},
                                {"time": 8000, "data": {"body.arms.left.upper.pitch": 0, "body.arms.right.upper.pitch": 0}},],
                        force=True
                        )
        
    yield session.call("rie.dialogue.say", text="Now let's raise both arms together and hold them here for a few seconds!")
    yield session.call("rom.actuator.motor.write",
                        frames=[{"time": 2000, "data": {"body.arms.left.upper.pitch": -2.4, "body.arms.right.upper.pitch": -2.4}},
                                {"time": 6000, "data": {"body.arms.left.upper.pitch": -2.4, "body.arms.right.upper.pitch": -2.4}},
                                {"time": 8000, "data": {"body.arms.left.upper.pitch": 0, "body.arms.right.upper.pitch": 0}},],
                        force=True
                        )
    

@inlineCallbacks
def stretch_elbow(session, details, reps):
    yield session.call("rie.dialogue.say", text="It's time to stretch our elbows. Watch me and then again we will do the rest together")

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
    
    text = "Now let's do " + str(reps) + " together - count with me!"
    yield session.call("rie.dialogue.say", text=text)

    for i in range(reps):
        yield session.call("rie.dialogue.say", text=str(i + 1))
        yield session.call("rom.actuator.motor.write",
                        frames=[{"time": 2000, "data": {"body.arms.left.lower.roll": -1.5, "body.arms.right.lower.roll": -1.5}},
                                {"time": 4000, "data": {"body.arms.left.lower.roll": 0, "body.arms.right.lower.roll": 0}},
                                ],
                        force=True
                        )

    yield session.call("rom.optional.behavior.play", name="BlocklyStand")


@inlineCallbacks
def neck_side_to_side(session, details, reps):
    yield session.call("rie.dialogue.say", text="Now let's carefully turn our heads from side to side. I will show you and then again we will do the rest together")

    yield session.call("rom.actuator.motor.write",
                    frames=[{"time": 3000, "data": {"body.head.yaw": 0.8}},
                            {"time": 5000, "data": {"body.head.yaw": 0.8}},
                            {"time": 8000, "data": {"body.head.yaw": -0.8}},
                            {"time": 10000, "data": {"body.head.yaw": -0.8}},
                            {"time": 13000, "data": {"body.head.yaw": 0.0}}],
                    force=True
                    )
    
    text = "Now let's do " + str(reps) + " repetitions"
    yield session.call("rie.dialogue.say", text=text)

    for i in range(reps):
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
def tilt_head(session, details, reps):

    yield session.call("rie.dialogue.say", text="Now we will tilt our heads from side to side. Watch me and then we will do it together")

    yield session.call("rom.actuator.motor.write",
                    frames=[{"time": 3000, "data": {"body.head.roll": 0.17}},
                            {"time": 6000, "data": {"body.head.roll": -0.17}},
                            {"time": 9000, "data": {"body.head.roll": 0}},],
                    force=True
                    )
    
    text = "We will do " + str(reps) + " together!"
    yield session.call("rie.dialogue.say", text=text)

    for i in range(reps):
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
def lift_head(session, details, reps):
    yield session.call("rie.dialogue.say", text="Let's lift our heads up and down. It will feel great! I will show you once and then again we will do the rest together")

    yield session.call("rom.actuator.motor.write",
                    frames=[{"time": 3000, "data": {"body.head.pitch": -0.17}},
                            {"time": 6000, "data": {"body.head.pitch": 0.17}},
                            {"time": 9000, "data": {"body.head.pitch": 0}},],
                    force=True
                    )
    
    text = "Let's do this " + str(reps) + " times!"
    yield session.call("rie.dialogue.say", text=text)

    for i in range(reps):
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
def neck_exercises(session, details, reps):
    yield neck_side_to_side(session, details, reps)

    yield sleep(2)
    yield tilt_head(session, details, reps)
    
    yield sleep(2)
    yield lift_head(session, details, reps)


@inlineCallbacks
def touch_toes(session, details, reps):
    yield session.call("rie.dialogue.say", text="Let's try and touch our toes. Watch me first!")
    yield session.call("rom.optional.behavior.play", name="BlocklyTouchToes")

    text = "Great! Let's do " + str(reps) + " together!"
    yield session.call("rie.dialogue.say", text=text)

    for i in range(reps):
        yield session.call("rie.dialogue.say", text=str(i + 1))
        yield session.call("rom.optional.behavior.play", name="BlocklyTouchToes")
