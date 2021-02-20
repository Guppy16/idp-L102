# Script to convert a robot in a wbt file to a .proto file
# NOTE: need to manually change: name (DONE: baseColor, controller, mass and density)
import re

path_to_wbt = "../worlds/IDP-rootg" + ".wbt"
path_to_proto = "../protos/root_g" + ".proto"
robot_def = "DEF ROOT_G Robot"

r = re.compile(r'(?s)' + robot_def + r' (\{.*?\n\})')

# Extract robot code from wbt file
with open(path_to_wbt) as wbt_file:
    f = wbt_file.readlines()
text = "".join(f)
robot_text = r.findall(text)[0]

# Replace lines with IS parameters
robot_text = re.sub(r'controller (.*)', 'controller IS controller', robot_text)
robot_text = re.sub(r'baseColor (.*)', 'baseColor IS color', robot_text, count=1)
robot_text = re.sub(r'translation (.*)', 'translation IS translation\n\trotation IS rotation', robot_text, count=1)

with open(path_to_proto, 'w') as f:
    f.write(
        'PROTO root_g [\n\
            field SFVec3f    translation  1 0.15 1\n\
            field SFRotation rotation     0 1 0 3.14159\n\
            field SFColor    color        1 0 0\n\
            field SFString   name         "root_g"\n\
            field SFString   controller   "main_controller"\n\
        ]\n' +  "{\nRobot " + robot_text + "\n}"
    )
