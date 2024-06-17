# Virtual Mouse

## Project Overview

The Virtual Mouse project is an application developed using Kivy that allows users to control the mouse using hand gestures. The application utilizes the MediaPipe library for detecting hand landmarks through a webcam and enhances the accuracy of hand gesture classification using a machine learning model. Various gestures are mapped to different mouse actions such as moving, clicking, and dragging, with the Kalman Filter being used to smoothen the hand movements. The user can configure the gestures mappings to the mouse function.

## Table of Contents

- [Folder Structure](#folder-structure)
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

## Folder Structure

```plaintext
VirtualMouse-HandTracking/
│
├── assets/
|
├── db/
│   ├── db.py
│   ├── actions.db
│   ├── schema.sql
│
├── models/
│   ├── GestureDetectionModel.py
│   ├── random_forest_model.pkl
│   ├── xgboost.pkl
│   ├── tfv3.keras
│
├── modules/
│   ├── GesturePredictor.py
│   ├── HandDetector.py
│   ├── KalmanFilter.py
│   ├── MouseController.py
│
├── views/
│   ├── components/
│   ├── screens/
│
├── training/
│   ├── collecting_data.py
│   ├── training.ipynb
|
├── presenters/
│   ├── CameraFeedbackPresenter.py
│   ├── CameraPresenter.py
│   ├── GestureDetectionPresenter.py
│   ├── SettingsPresenter.py
|
├── utils/
|
├── main.py
├── VirtualMouse.py
├── requirements.txt
├── paths.yaml
├── .gitignore
└── README.md
```

## Methodology

The Virtual Mouse Hand follows a structured methodology to achieve accurate hand gesture recognition and mapping to mouse actions:

1. **Hand Landmark Detection**: The application uses the MediaPipe library to detect hand landmarks from the webcam feed.
2. **Preprocessing**: The detected landmarks are normalized and preprocessed for prediction.
3. **Feature Engineering**: Applies Principal Component Analysis (PCA) to reduce the dimensionality of the data, enhancing performance and reducing noise.
4. **Gesture Prediction**: A machine learning model predicts the gestures based on the preprocessed landmarks.
5. **Kalman Filter**: The Kalman Filter smoothens the detected movements to ensure stable cursor control.
6. **Mouse Actions**: Various gestures are mapped to mouse actions such as moving, clicking, and dragging. The application includes logic to handle different gestures and perform corresponding mouse actions.
7. **Visualization**: The application highlights detected gestures on the video feed for better visualization and debugging.

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
