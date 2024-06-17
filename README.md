# Virtual Mouse

## Project Overview

The Virtual Mouse project is an application developed using Kivy that allows users to control the mouse using hand gestures. The application utilizes the MediaPipe library for detecting hand landmarks through a webcam and enhances the accuracy of hand gesture classification using a machine learning model. Various gestures are mapped to different mouse actions such as moving, clicking, and dragging, with the Kalman Filter being used to smoothen the hand movements. The user can configure the gestures mappings to the mouse function.

## Table of Contents

- [Methodology](#methodology)
- [Prerequisites](#prerequisites)
- [Building](#building)
- [Acknowledgements](#acknowledgements)
- [License](#license)

### Sample Images

<p align="left">
  <img src="https://github.com/RamezzE/VirtualMouse-HandTracking/assets/117018553/b76efedd-cf1e-4100-bd72-6b639ade0e38" alt="Sample 1" height="200">
  <img src="https://github.com/RamezzE/VirtualMouse-HandTracking/assets/117018553/3c52bc8f-24af-43c6-9c3c-627f80620de4" alt="Sample 2" height="200">
  <img src="https://github.com/RamezzE/VirtualMouse-HandTracking/assets/117018553/04d02d5a-4357-46d8-94d9-fbf0de08adb6" alt="Sample 3" height="200">
  <img src="https://github.com/RamezzE/VirtualMouse-HandTracking/assets/117018553/15e4f54f-552d-4e8d-8662-62ca61ac7b02" alt="Sample 4" height="200">
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
- If the above command does not work, run the below command

```
pip install numpy tensorflow mediapipe scikit-learn kivy[base] mouse pandas pyautogui pyaml opencv-python
```

5. **Run main application file**

```
python VirtualMouse.py
```

## Acknowledgements

Most of the icons used are provided by [Icons8](https://icons8.com/)

## License

This project is licensed under the [MIT License](LICENSE).
