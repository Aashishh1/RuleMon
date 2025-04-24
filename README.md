<div align='center'><img style="width:30%" src='https://github.com/user-attachments/assets/7e10e502-c8ab-4553-8a44-5b5f3e38fc74'/></div>

Welcome to **RuleMon**! 🌟
This project is a **computer vision-based system** designed to detect traffic violations like red light breaking, illegal parking, and wrong-way driving. It uses **OpenCV**, **TensorFlow**, and **PyQt5** to analyze real-time video and show results in a simple GUI.

## 📌 Features

- 🔴 **Signal Violation Detection** (Red Light Jumping)
- 🚫 **Illegal Parking Detection**
- ↩️ **Wrong Direction Movement Detection**
- 📹 **Live CCTV Feed Monitoring**
- 🧠 **Vehicle Type Classification (Car, Bike, Truck, etc.)**
- 🖥️ **Admin Dashboard (PyQt GUI)**
- 📁 **Violation Record Logging with Image Evidence**
- 📊 **Exportable CSV Reports**

---

## 🧠 Technologies Used

| Tool/Library | Purpose |
|--------------|---------|
| Python       | Core Programming Language |
| OpenCV       | Video Processing and Vehicle Detection |
| PyQt5        | GUI Development |
| SQLite       | Local Database to Store Violations |
| TensorFlow/Keras | Vehicle Type Classification |

---

## 🧠 TensorFlow/Keras in This Project

We use **TensorFlow with Keras** to build and run a deep learning model that can:

- 🧍 Detect vehicles in real-time video feeds  
- 🚦 Identify traffic rule violations such as:
  - Signal jumping  
  - Illegal parking  
  - Wrong direction movement

Keras provides a simple and flexible API to design the neural network, while TensorFlow ensures fast and efficient model execution, especially when processing continuous video streams from traffic cameras.

---

## 🖥️ PyQt5 in This Project

We use **PyQt5** to build the **Graphical User Interface (GUI)** of the Traffic Rules Violation Detection System.

This allows us to create a **user-friendly desktop application** for:

- 👮‍♂️ Admin dashboard for monitoring violations
- 🎥 Live video stream display
- 🔍 Search and view vehicle details
- 📊 Real-time traffic data tracking

---

## 📸 GUI Dashboard Preview

<table>
  <tr>
    <td><img src="https://github.com/user-attachments/assets/0c15f205-86bb-44cc-afe2-84eb633f2f9b" width="400"/><br><b>Admin Dashboard</b></td>
    <td><img src="https://github.com/user-attachments/assets/791f2768-8cc8-4956-8fe7-db1879f112a3" width="500"/><br><b>Violation Alert View</b></td>
  </tr>
</table>

---

## 🚦 Violation Types

<table>
  <tr>
    <td><img src="https://github.com/user-attachments/assets/a8e73fbb-eb33-4c1a-80d3-f6984688fa4d" width="500"/><br><b>Red Light Violation</b></td>
    <td><img src="https://github.com/user-attachments/assets/461c11f4-f9ca-4505-b164-f458952c2683" width="450"/><br><b>Illegal Parking</b></td>
    <td><img src="https://github.com/user-attachments/assets/b8f0aa48-1594-4d9d-952e-b4d949a42978" width="400"/><br><b>Direction</b></td>
  </tr>
</table>

---

## 📊 System Flow & Schema

<table>
  <tr>
    <td><img src="https://github.com/user-attachments/assets/3f361247-afa3-4f5d-9c93-b872b6db6f92" width="400"/><br><b>System Workflow</b></td>
    <td><img src="https://github.com/user-attachments/assets/30afdb9c-f763-46ec-9e6f-879e950cc9eb" width="400"/><br><b>Detection Flowchart</b></td>
  </tr>
  <tr>
    <td colspan="2" align="center">
      <img src="https://github.com/user-attachments/assets/825e09c8-02e3-433d-af30-18c4fe240b53" width="500"/><br><b>Database Design</b>
    </td>
  </tr>
</table>
