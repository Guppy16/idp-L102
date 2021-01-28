# IDP L102
Team Name: Root g 
Robots: pi, e

The ultimate repo for the idp

# Tasks
- [ ] Write up First Report
  - [Draft](https://docs.google.com/document/d/1v2MvU0iz8C-MFJlQ4b2S1USyDgQTOsfpWKXyA-FDR0s/edit?usp=sharing)
  - [Latex](https://www.overleaf.com/read/jndqsdmcqbcx)
  - [ ] Create block diagrams of the electronic components
  - [ ] Think about the navigation algorithms required for the robot
- [ ] Improve Gannt Chart
- [ ] Complete all the Webots [tutorials](https://cyberbotics.com/doc/guide/tutorials) (in python)
 
 
- Before the first Presenetation ~ 5 days
  - [x] Gannt chart -> [ ] Make this better
  - [x] Get used to Webots ~ 2 days
  - [x] Initial CAD and PCB design ~ 5
  - [x] Inital algorithms for navigation ~ 4
- Before progress Meeting 1 ~ 7 days
  - [ ] Complete simulation of environment (2 robots)
  - [ ] Complete cad design of bulk components ~ 5
  - [ ] Finished full schematic ~ 3
  - [ ] Started implementing algorithms ~ 3
- Before Progress Meeting 2 ~ 7 days
  - [ ] Finished CAD design
  - [ ] Implemented Algorithms
  - [ ] Start documentation
- Before First Competition ~ 2 days
  - [ ] Fully tested algorithms in simulation
- Before Final Presentation
  - [ ] Complete presentation ~ 
- Before Final Competition
  - [ ] Improved the simulation environment
  - [ ] Improved software
- Before Final Report
  - [ ] Completed documentation

---
## Schecdule
- Week 1
  - Tue 26 14:30 - [First Presentation](https://docs.google.com/presentation/d/1Jz8pw5dtujUt2GG7nFzDspJj2hsbr5QpLF5pbWbA2lo/edit#slide=id.gb7adb26c31_0_31)
- Week 2
  - Thurs 28 16:00 - First Report
  - Tue 2 14:30 - Progress Meeting
- Week 3
  - Tue 9 14:30 - Progress Meeting
- Week 4
  - Thurs 11 09:00 - First Competition
  - Tue 16 09:00 - Final Presentation
  - Wed 17 14:00 - Final Competition
- Week 5
  - Mon 22 16:00 - Final Report and Documentation Deadline

---
## Software

- [x] Build a simulation
- [x] Add robots
- [ ] Add controllers to the robot to drive it using arrow keys
- [ ] Add a colour sensor
- [ ] Add a distance sensor
- [ ] Add a GPS sensor
- [ ] Add a compass
- [ ] Control Algorithm
  - AVOID THE OTHER ROBOT AT ALL COST. Possible ways of implelementing this:
    - Get the location of the other robot using GPS
    - Use IR emitter and receiver to send a signal
  - Find a block. This can be implemented in 2 ways: 
    - Rotate the robot
    - Rotate the distance sensor (trickier)
    - Ques: how to distringuish between a wall and block from far away
  - Get close to the block
    - Once the block is located, keep the heading aligned to the block
    - Don't get too close to it, because we don't know whether we'll be be aligned with it or not
  - Check the colour
    - Use the colour sensor
  - if it's not the right colour, restart the loop. otherwise:
    - Somehow get aligned to it
    - Get close to it and "pick it up"
    - Ques: How can we be confident that we've picked up the block
  - Once the block has been picked up
    - Use the GPS sensor to locate ur pos
    - Align the robot using the hall sensor


Extras
- [ ] Control the robot using a simple grid search algo (without building a map of the env)
- [ ] Test some extreme cases: e.g. detecting collisions, getting a block from the wall
- [ ] Build a map of the env by detecting blocks using the distance sensor with GPS
- [ ] Use an algo (e.g. A* or Dijkstras) to find the best path to search for blocks
- [ ] Add a servo to the distance sensor to make it rotate to build a more accurate map


---

## Useful Links
- CAD
  - [Parts list](https://www.vle.cam.ac.uk/pluginfile.php/19716321/mod_resource/content/0/Tools%20and%20Parts%20List%20Rev%202.0.pdf)
  - [Good and bad drawings](https://www.vle.cam.ac.uk/pluginfile.php/19604241/mod_resource/content/1/Good_Bad_drawing_examples.pdf)
  - 
- [repo for CAD](onshape.com)
