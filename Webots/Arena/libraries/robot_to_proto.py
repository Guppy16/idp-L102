# Script to convert a robot in a wbt file to a .proto file
import re

path_to_wbt = "../worlds/IDP-rootg" + ".wbt"
path_to_proto = "../protos/rootg" + ".proto"
robot_def = "DEF NEW_ROBOT Robot"

r = re.compile(r'(?s)' + robot_def + r' (\{.*?\n\})')

# Extract robot code from wbt file
with open(path_to_wbt) as wbt_file:
    f = wbt_file.readlines()
text = "".join(f)
robot_text = r.findall(text)[0]

# Replace lines with IS parameters
r = re.compile(r'translation (.*)')
robot_text = r.sub('translation IS translation\n\trotation IS rotation', robot_text, count=1)

# Replace mass with bodyMass and density = -1

with open(path_to_proto, 'w') as f:
    f.write(
        "PROTO NewRRobot [\n\
            field SFVec3f    translation  1 0.09 -1\n\
            field SFRotation rotation     0 1 0 0\n\
            field SFFloat    bodyMass     1\n\
        ]\n" +  "{\nRobot " + robot_text + "\n}"
    )
