# HPS_Project Team X: X-Trash

Designed by Team 10/Team X of the 2023 Google Hardware Product Sprint Program.

## Members
Bo-Wei (Cosmo), Wen

## Overview

X Trash, a revolutionary product that allows you to dispose of trash without leaving your workstation.

Trash simplifies trash disposal with a user-friendly process:

1. Send a message to X Trash.
2. X Trash moves to your location.
3. Open the trash lid and dispose of your trash.
4. X Trash autonomously returns to its original position.

This process eliminates the need for manual effort, making trash disposal effortless.

## Main features

### Indoor Positioning

X Trash uses a pair of ultra-wideband (UWB) ranging modules to navigate towards the user. This approach enhances mobility and eliminates the need for additional setup.

### Avoiding Obstacles

X Trash incorporates simple obstacle avoidance logic with ultrasonic sensors to detect obstacles within 20cm and adjust the direction accordingly.

### Automatic Lid Opening

X Trash utilizes ultrasonic modules to automatically open the lid when a user's hand is within 10cm and measuring trash levels.

### Trash Level Detection

X Trash utilizes ultrasonic modules to detect the trash level inside the bin, preventing overflow and notifying users when it's time to empty the bin

## Requirments

1. Raspberry Pi 3 Model B+ w/ SD card and basic programming requiements
2. CGM25-370 Metal Gear DC Motor
3. L298N DC Motor Driver
4. Power Sources: Power Bank and 11.1V Lithium Battery
5. ESP32 Ultra Wideband Module
6. HC-SR04 Ultrasonic Sensor Module x 3
7. Trash Bin
8. Other wiring and housing equipment for the modules above

### Execution

Navigate to this folder and execute:

```bash
python main.py
```

### Appearance and Demo

![image](./img/Team%20X.gif)
