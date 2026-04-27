# SRT-Project-Equipment-for-Garlic-Damage-Rate-Detection

It is a SRT project for garlic damage rate Detection, sorting, and weighing

It is a team work and I was in charge of **Embedded Design**, **Deep Learning Design** and **Project Proposal Planning and Development**.

## Description

1. `Dataset_Old/`, `Dataset_Old/` and `Dataset_New/` contain code for pre-training process including extension and separation of dataset.

2. **STM32F407ZGT6** is our main MCU for motor, sensor and servo control and buliding connection with **Raspberry Pi**.

3. `STM32F407ZGT6/` includes main control code for MCU, `main-on-raspberry.py` only works on **Raspberry Pi**.

4. **Yolov8n** is our detect model trained with our previously taken database, processed by `Dataset_Old/`, `Dataset_Old/` and `Dataset_New/`.

5. More information about **dataset processing**, please go to [Dataset_Old](https://github.com/CyniKal073/Dataset-Old-For-Yolov8), [Dataset_New](https://github.com/CyniKal073/Dataset-New-For-Yolov11) and [Dataset_Extend](https://github.com/CyniKal073/Dataset-Extend).

6. `camera with flask_test/` contains implementation of UDP protocol communication in local area network and connection with Flask server.

7. `tkinter_test` contains UI interface based on Python's Tkinter which controls hardware devices and provides real-time monitoring image recognition.
