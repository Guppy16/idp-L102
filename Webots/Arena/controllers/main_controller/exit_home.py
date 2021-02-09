import numpy as np

tol = 1e-2
# Add some try except decorator for divide by zero error?

def inside_home(gps_vals, HOME):
    """Returns true if robot pos is within home box"""
    pos = np.array([gps_vals[0],-gps_vals[2]])
    homeVec = HOME - pos
    return np.linalg.norm(homeVec) < 0.40
    print("Arrived home chief")

def heading_dot_home(gps_vals, cps_vals, HOME):
    """Return the dot product between the heading and the homeVec"""
    pos = np.array([gps_vals[0],-gps_vals[2]])
    homeVec = HOME - pos
    if np.linalg.norm(homeVec) < tol:
        return 0
    homeVec /= np.linalg.norm(homeVec)

    heading = np.array([cps_vals[0], cps_vals[2]])
    heading /= np.linalg.norm(heading)

    return np.dot(heading, homeVec)

def exit_home(gps_vals, cps_vals, l_motor, r_motor, HOME = np.array([1.0, 1.0]), MAX_SPEED=5):
    HOME = np.array(HOME)
    # Reverse motors if inside home
    if inside_home(gps_vals, HOME):
        r_motor.setVelocity(-MAX_SPEED)
        l_motor.setVelocity(-MAX_SPEED)

    # Rotate 180 once outside home
    else:
        r_motor.setVelocity(-0.2*MAX_SPEED)
    
    # Check if rotated 180
    return not heading_dot_home(gps_vals, cps_vals, HOME) + 1 < tol