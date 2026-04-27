# SRT-Project-Equipment-for-Garlic-Damage-Rate-Detection

It is a SRT project for garlic damage rate Detection, sorting, and weighing

It is a team work and I was in charge of **Embedded Design**, **Deep Learning Design** and **Project Proposal Planning and Development**.

## Description

`Dataset_Old/`, `Dataset_Old/` and `Dataset_New/` contain code for pre-training process including extension and separation of dataset.

**STM32F407ZGT6** is our main MCU for motor, sensor and servo control and buliding connection with **Raspberry Pi**.

`STM32F407ZGT6/` includes main control code for MCU, `main-on-raspberry.py` only works on **Raspberry Pi**.

**Yolov8n** is our detect model trained with our previously taken database, processed by `Dataset_Old/`, `Dataset_Old/` and `Dataset_New/`.

More information about **dataset**, please go to [Dataset_Old](https://github.com/CyniKal073/Dataset-Old-For-Yolov8), [Dataset_New]() and [Dataset_Extend]().
