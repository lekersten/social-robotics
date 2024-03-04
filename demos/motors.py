from autobahn.twisted.component import Component, run
from twisted.internet.defer import inlineCallbacks


@inlineCallbacks
def main(session, details):
    yield session.call("rom.optional.behavior.play", name="BlocklyStand")
    info = yield session.call("rom.actuator.motor.info")
    print(info)
    # Nod
    yield session.call("rom.actuator.motor.write",
                       frames=[{"time": 400, "data": {"body.head.pitch": 0.1}},
                               {"time": 1200, "data": {"body.head.pitch": -0.1}},
                               {"time": 2000, "data": {"body.head.pitch": 0.1}},
                               {"time": 2400, "data": {"body.head.pitch": 0.0}}],
                       force=True
                       )
    # yield session.call("rom.optional.behavior.play", name="BlocklySitDown")
    yield session.call("rom.optional.behavior.play", name="BlocklyArmsUp")
    session.leave()  # Close the connection with the robot


wamp = Component(
    transports=[{
        "url": "ws://wamp.robotsindeklas.nl",
        "serializers": ["msgpack"],
        "max_retries": 0
    }],
    realm="rie.65e5b9c7d9eb6cfb396e4516",
)

wamp.on_join(main)

if __name__ == "__main__":
    run([wamp])


"""
'body.arms.right.lower.roll': {'max': 6.46259971647245e-05, 'min': -1.745264625997165, 'type': 'joint'}, 
'body.arms.left.upper.pitch': {'max': 1.5943951023931953, 'min': -2.5943951023931953, 'type': 'joint'}, 
'body.legs.right.upper.pitch': {'max': 1.7453292519943295, 'min': -1.7453292519943295, 'type': 'joint'}, 
'body.legs.left.lower.pitch': {'max': 1.7453292519943295, 'min': -1.7453292519943295, 'type': 'joint'}, 
'body.head.yaw': {'min': -0.8726646259971648, 'type': 'joint', 'max': 0.8726646259971648}, 
'body.legs.left.foot.roll': {'max': 0.8410520681182421, 'min': -0.24105206811824215, 'type': 'joint'}, 
'body.legs.left.upper.pitch': {'max': 1.7453292519943295, 'min': -1.7453292519943295, 'type': 'joint'}, 
'body.legs.right.lower.pitch': {'max': 1.7453292519943295, 'min': -1.7453292519943295, 'type': 'joint'}, 
'body.torso.yaw': {'max': 0.8726646259971648, 'min': -0.8726646259971648, 'type': 'joint'}, 
'body.arms.right.upper.pitch': {'max': 1.5943951023931953, 'min': -2.5943951023931953, 'type': 'joint'}, 
'body.head.pitch': {'max': 0.17453292519943295, 'min': -0.17453292519943295, 'type': 'joint'}, 
'body.arms.left.lower.roll': {'min': -1.745264625997165, 'type': 'joint', 'max': 6.46259971647245e-05}, 
'body.head.roll': {'type': 'joint', 'max': 0.17453292519943295, 'min': -0.17453292519943295}, 
'body.legs.right.foot.roll': {'max': 0.24105206811824215, 'min': -0.8410520681182421, 'type': 'joint'}
"""