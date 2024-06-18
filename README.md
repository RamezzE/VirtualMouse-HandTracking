# Virtual Mouse

## Table of Contents
- [Overview](#overview)
- [Methodology](#methodology)
- [Prerequisites](#prerequisites)
- [Building](#building)
- [Acknowledgements](#acknowledgements)
- [License](#license)

## Overview

Built using OpenCV, MediaPipe, Tensorflow and Kivy for the user interface, Virtual Mouse allows mouse control using several hand gestures mapped to perform different mouse functions such as movement, dragging, clicking, scrolling, zooming etc. These mappings can be changed and configured along with additional settings in runtime through the Kivy application.

### Sample Images

<p align="left">

  <img src="https://github.com/RamezzE/VirtualMouse-HandTracking/assets/117018553/d8aa8a15-9909-4fe9-a4cf-5f111e60f317" alt="Home Screen" height="200">
  <img src="https://github.com/RamezzE/VirtualMouse-HandTracking/assets/117018553/af41b857-a3d2-4b3d-b390-4ddb3d9aa6b7" alt="Camera Feedback Screen" height="200">
  <img src="https://github.com/RamezzE/VirtualMouse-HandTracking/assets/117018553/525fcf55-4758-4024-8715-3205220e4123" alt="Settings Screen 1" height="200">
  <img src="https://github.com/RamezzE/VirtualMouse-HandTracking/assets/117018553/0d81a47c-586b-440e-8f50-29a9a2ee7b35" alt="Settings Screen 2" height="200">
</p>

## Methodology

The Virtual Mouse Hand follows a structured methodology to achieve accurate hand gesture recognition and mapping to mouse actions for each frame.

![Methodology Flowchart](https://github.com/RamezzE/VirtualMouse-HandTracking/assets/117018553/7db9f201-7720-4c0c-9c5e-944f7876b4dc)

## Prerequisites
- Python
- Pip

### Linux
- You can run these commands on linux to install python, pip, python-venv and other dependencies

```
sudo apt-get update
sudo apt install python3
sudo apt install python3-pip
sudo apt install python3-venv
sudo apt-get install python3-tk python3-dev
```

### Windows
- Install python from the official website
- Check if pip is already installed by running: `pip help`
- If pip is not installed, please check this [guide](https://www.geeksforgeeks.org/download-and-install-pip-latest-version/#windows) for installing pip on Windows

## Building

1. **Clone the repository**

```
git clone https://github.com/RamezzE/VirtualMouse-HandTracking.git
```

2. **Navigate to project folder**

```
cd VirtualMouse-HandTracking
```

3. **Create and activate a python virtual environment**

#### Linux

```
python3 -m venv venv
source venv/bin/activate
```

#### Windows

```
python -m venv venv
venv\Scripts\activate
```

4. **Install necessary pip packages**

```
pip install -r requirements.txt
``` 
- If the above command does not work or throws an error, run the below command instead

```
pip install numpy tensorflow mediapipe scikit-learn kivy[base] kivyontop mouse pandas pyautogui pyaml opencv-python
```

5. **Run main application file**

```
python main.py
```

- Optionally, if you'd like to run the script directly without running the Kivy application, you can run the alternative main file

```
python main_no_gui.py
```

## Acknowledgements

Most of the icons used are provided by [Icons8](https://icons8.com/)

## License

This project is licensed under the [MIT License](LICENSE).
