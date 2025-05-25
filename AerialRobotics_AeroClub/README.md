# Week 1: Introduction to Webots and Multirotor Simulation
Deadline: 25 May EOD

### 1. **Objectives**
-Understand the components and basic flight dynamics of a quadrotor.
Install and configure Webots and Python controller support.
Execute a simple Webots controller to perform take-off, hover, and land.

---

### 2. **Setup & Prerequisites**
System Requirements


Operating System: Windows 10/11, macOS 10.15+, or Ubuntu 18.04+


RAM: Minimum 8 GB (16 GB recommended)


Disk Space: ≥ 5 GB free


CPU/GPU: Any modern multi-core CPU; GPU optional for hardware acceleration


*Install Webots*
-Download the 2023a version of Webot from https://cyberbotics.com/#download
-Follow the installer instructions for your platform.

*Install Python and Dependencies*
-Install Python 3.7–3.9 (from https://python.org).

*Create and activate a virtual environment:*

 	python -m venv webots-env
source webots-env/bin/activate   # Linux/macOS
webots-env\Scripts\activate      # Windows

Install required packages:
 pip install controller==0.1.0
 (The controller package provides the Python API for Webots.)


*Obtain Starter World and Controller*
  -Clone or download the AeroClub starter repository (if provided).
  -Alternatively, use Webots’ built-in mavic_2_pro example:
  -In Webots, navigate to File → Open Sample World.
  -Select projects/samples/robots/mavic_2_pro.wbt


*Directory Structure*
 Your project folder should contain:

 week1/
├── quadcopter.wbt
├── controllers/
│   └── takeoff_hover_land.py
└── README.md

---

### 3. **Concepts Covered**
Lift and Thrust: How rotor speed generates upward force.


Roll, Pitch, Yaw:


Roll: tilting about the front-to-rear axis


Pitch: tilting about the left-to-right axis


Yaw: rotation about the vertical axis


Coordinate Frames:


World frame (fixed) vs. body frame (attached to drone)


API Control Loop:


Sensor read → compute commands → send actuation → repeat

---

### 4. **Tasks**
Load the Starter World


Open quadcopter.wbt in Webots.


Verify that the environment loads and that the quadrotor model is visible.


Implement the Python Controller


Create controllers/takeoff_hover_land.py with the following logic, some of the code are not completed. Understand the logic and complete the code :

 from controller import Robot

#Create Robot instance
-robot = Robot()
-timestep = int(robot.getBasicTimeStep())

#Motor device names — adjust if needed
-motor_names = ["front left propeller", "front right propeller", "rear left propeller", "rear right propeller"]

# Initialize motors
-motors = []
-for name in motor_names:
    -motor = robot.getDevice(name)
    -if motor is None:
     -   print(f"Error: Motor device '{name}' not found. Please check device names.")
      -  exit(1)
    -motor.setPosition(float('inf'))  # Velocity control mode
    -motor.setVelocity(0.0)
    -motors.append(motor)

-def set_all_motors_velocity(velocity):
 -   for motor in motors:
        motor.setVelocity(velocity)

#Set motor velocities with opposite directions for proper torque balance
-def set_all_motors_velocity(base_velocity):
    #Direction multipliers for motors: +1 or -1 depending on spin direction
    -directions = [ - , - , -  , - ]  # Edit and adjust if your drone motor layout differs
    -for i, motor in enumerate(motors):
        -motor.setVelocity(base_velocity * directions[i])

#Set the Parameters
-takeoff_duration = 0.0   # seconds to reach hover velocity
-hover_duration = 0.0    # seconds to hover
-land_duration = 0.0     # seconds to land
-max_velocity =  0.0    # max motor velocity for hover (tune as needed)

#########################################################

     WRITE THE CODE FOR TAKEOFF, HOVER AND LAND HERE

#########################################################

-set_all_motors_velocity(0.0)

-print("Flight sequence complete.")


In Webots, assign this script as the controller for the mavic_2_pro node.


Run the Simulation


Click Run in Webots.


Observe the drone take off, hover at approximately 1 m, then land smoothly.

---

### 5. **Expected Output**
Controller Script: takeoff_hover_land.py with clear comments.


Simulation Recording:
-A screen capture or video (≤ 2 minutes) demonstrating take-off, hover, and landing.


Brief Report:
-A short README section describing any installation challenges or tips.

---

### 6. **Bonus Challenge (Optional)**
-Augment your controller to perform a square flight pattern at 1 m altitude before landing:
-Fly forward 1 m, right 1 m, backward 1 m, left 1 m.
-Return to the origin point.
-Land as before.

---

### 7. **Resources**

-Webots Installation Guide: https://cyberbotics.com/doc/guide/installing-webots
-Webots Python API Reference: https://cyberbotics.com/doc/reference/python-api 
-Mavic2Pro Tutorial: https://cyberbotics.com/doc/guide/mavic-2-pro?version=R2023a







