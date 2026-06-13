# CableCarousel 🎡

**Author:** Amir Mobasheraghdam
**University:** University of Isfahan
**Project Type:** Python GUI · Arduino Control · Industrial Automation · HMI

CableCarousel is a modern human-machine interface developed in Python using **CustomTkinter**. It provides an intuitive visual system for selecting and managing cable reels in industrial, laboratory, warehouse, or logistics environments. The application communicates with an Arduino through a serial connection and can be used to control a stepper motor-based cable carousel.

The project combines a professional graphical user interface, structured cable metadata, image-based reel selection, search functionality, and hardware communication into one complete software-hardware prototype.

---

## 🇬🇧 English Description

CableCarousel is a visually interactive desktop application designed to manage and select cable reels. It allows users to choose a specific cable drum from a graphical interface, view important cable information, and send the selected reel number directly to an Arduino-controlled stepper motor system.

The software is built with **Python** and **CustomTkinter** for a clean and modern interface. **Pillow** is used for image handling, while **PySerial** manages communication between the computer and Arduino.

This project is suitable for educational demonstrations, laboratory prototypes, warehouse automation concepts, smart storage systems, and human-machine interface development.

---

## 🇩🇪 Deutsche Beschreibung

CableCarousel ist eine visuell interaktive Desktop-Anwendung zur Verwaltung und Auswahl von Kabeltrommeln. Die Software ermöglicht es dem Benutzer, eine bestimmte Kabeltrommel über eine grafische Benutzeroberfläche auszuwählen, relevante Kabelinformationen anzuzeigen und die ausgewählte Trommelnummer direkt an ein Arduino-gesteuertes Schrittmotorsystem zu senden.

Die Anwendung wurde mit **Python** und **CustomTkinter** entwickelt, um eine moderne und übersichtliche Benutzeroberfläche bereitzustellen. **Pillow** wird für die Bildverarbeitung verwendet, während **PySerial** die serielle Kommunikation zwischen Computer und Arduino übernimmt.

Das Projekt eignet sich für Ausbildungszwecke, Laborprototypen, Lagerautomatisierung, intelligente Aufbewahrungssysteme und die Entwicklung von Human-Machine-Interfaces.

---

## ✨ Key Features

* Modern graphical user interface using **CustomTkinter**
* Interactive cable reel selection
* Image-based reel buttons
* Real-time display of cable metadata
* Cable information includes:

  * Reel number
  * Cable type
  * Color
  * Serial number
  * Length
* Search and filter functionality
* Serial communication with Arduino
* Stepper motor control support
* Progress bar for cable length visualization
* Fullscreen and windowed mode support
* Fallback image generation if reel images are missing
* Clean and maintainable Python code structure
* Suitable for industrial automation and HMI demonstrations

---

## 🧰 Technologies Used

| Technology    | Purpose                             |
| ------------- | ----------------------------------- |
| Python        | Main programming language           |
| CustomTkinter | Modern graphical user interface     |
| Pillow        | Image processing                    |
| PySerial      | Serial communication with Arduino   |
| Arduino       | Hardware control                    |
| Stepper Motor | Physical reel positioning           |
| Git / GitHub  | Version control and project hosting |

---

## 📦 Requirements

Install the required Python packages:

```bash
pip install customtkinter pillow pyserial
```

Or install them using the included `requirements.txt` file:

```bash
pip install -r requirements.txt
```

Recommended Python version:

```bash
Python 3.10+
```

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/CableCarousel.git
cd CableCarousel
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Connect the Arduino

Connect the Arduino board to your computer using USB.

Default serial configuration:

```text
Port: COM9
Baudrate: 9600
```

On Windows, the port may be something like:

```text
COM3, COM4, COM7, COM9
```

On Linux or macOS, it may look like:

```text
/dev/ttyUSB0
/dev/ttyACM0
/dev/cu.usbmodemXXXX
```

### 4. Upload Arduino Firmware

Open the Arduino sketch located in:

```text
arduino/cable_carousel.ino
```

Upload it to your Arduino board using the Arduino IDE.

### 5. Run the Application

```bash
python main.py
```

Run in windowed mode:

```bash
python main.py --windowed
```

Run with a custom serial port:

```bash
python main.py --port COM7
```

Run with a custom baudrate:

```bash
python main.py --baudrate 9600
```

---

## 🖥️ Application Interface

The interface contains:

* A top header with the project title and search bar
* A cable reel selection area
* Interactive reel cards
* A detail panel for selected cable information
* Arduino connection status
* Manual reconnect button
* Fullscreen support
* Search filter for reel number, cable type, color, serial number, and length

---

## 🔎 Search Functionality

The search bar can filter cable reels by:

```text
Trommel number
Cable type
Color
Serial number
Length
```

Examples:

```text
CF29
Grün
AB904401
10
56.8
```

---

## 🧵 Cable Database Example

The internal cable database stores each cable reel with structured metadata:

```python
Cable(10, "Gelb", "CF29", "AB904410", 53.2)
Cable(9, "Rot", "CF211", "AB904409", 68.0)
Cable(8, "Braun", "CF113", "AB904408", 41.7)
Cable(7, "Silber", "CF240", "AB904407", 88.3)
Cable(6, "Orange", "CF10", "AB904406", 35.5)
Cable(5, "Rosa", "CF9", "AB904405", 72.6)
Cable(4, "Schwarz", "CF6", "AB904404", 61.0)
Cable(3, "Grau", "CF130", "AB904403", 47.9)
Cable(2, "Weiß", "CF98", "AB904402", 39.4)
Cable(1, "Grün", "CF77.UL", "AB904401", 56.8)
```

---

## 🛠️ Hardware Setup

### Required Hardware

* Arduino Uno, Nano, or compatible board
* Stepper motor
* Stepper motor driver
* External power supply if required
* USB cable
* Cable carousel mechanical structure
* Cable reels or reel mockups

### Example Components

| Component         | Example                    |
| ----------------- | -------------------------- |
| Microcontroller   | Arduino Uno / Arduino Nano |
| Motor             | 28BYJ-48 Stepper Motor     |
| Driver            | ULN2003 Driver Board       |
| Power Supply      | 5V external supply         |
| Control Interface | USB Serial                 |

---

## 🔌 Example Wiring

For a 28BYJ-48 stepper motor with ULN2003 driver:

| ULN2003 IN Pin | Arduino Pin |
| -------------- | ----------- |
| IN1            | 8           |
| IN2            | 9           |
| IN3            | 10          |
| IN4            | 11          |
| VCC            | 5V          |
| GND            | GND         |

The exact wiring can be changed in the Arduino sketch.

---

## 🔁 Serial Communication Protocol

The Python application sends the selected reel number to the Arduino through the serial port.

Example command sent from Python:

```text
5
```

This means:

```text
Move carousel to reel number 5
```

The Arduino receives the number, calculates the required motor movement, and rotates the carousel to the selected position.

---

## 🧠 Arduino Logic

The Arduino firmware should:

1. Wait for serial input
2. Read the selected reel number
3. Validate the received number
4. Calculate the target position
5. Rotate the stepper motor
6. Stop when the target reel is reached

Example logic:

```text
Receive reel number → calculate target angle → move stepper motor → stop at selected reel
```

---

## 📁 Project Structure

```text
CableCarousel/
├── main.py
├── requirements.txt
├── README.md
├── LICENSE
├── arduino/
│   └── cable_carousel.ino
├── assets/
│   ├── Gelb.png
│   ├── Rot.png
│   ├── Braun.png
│   ├── Silber.png
│   ├── Orange.png
│   ├── Rosa.png
│   ├── Schwarz.png
│   ├── Grau.png
│   ├── Weiss.png
│   └── Gruen.png
└── docs/
    └── screenshots/
```

---

## 🖼️ Assets

The application can use custom reel images stored in the assets or image folder.

Recommended image format:

```text
PNG
```

Recommended image size:

```text
512x512 px
```

Recommended naming:

```text
Gelb.png
Rot.png
Braun.png
Silber.png
Orange.png
Rosa.png
Schwarz.png
Grau.png
Weiss.png
Gruen.png
```

If no image is found, the application automatically generates a clean fallback reel icon based on the cable color.

---

## 📸 Screenshots

Add screenshots of the application here:

```text
docs/screenshots/main_ui.png
docs/screenshots/detail_panel.png
docs/screenshots/search_filter.png
```

Example Markdown:

```markdown
![Main Interface](docs/screenshots/main_ui.png)
![Detail Panel](docs/screenshots/detail_panel.png)
![Search Filter](docs/screenshots/search_filter.png)
```

---

## 🧪 Testing

Before using the system with real hardware, test the application without Arduino connected.

The GUI should still run and display:

```text
Arduino not connected
```

After connecting Arduino, press:

```text
Verbinden
```

Then select a reel and check whether the reel number is sent correctly.

---

## ⚠️ Troubleshooting

### Arduino is not connected

Check the following:

* Arduino is connected via USB
* Correct COM port is selected
* No other software is using the same port
* Arduino IDE Serial Monitor is closed
* PySerial is installed
* Correct baudrate is used

### Permission error on Linux

Run:

```bash
sudo usermod -a -G dialout $USER
```

Then restart the system.

### Module not found

Install dependencies again:

```bash
pip install customtkinter pillow pyserial
```

### Images are not displayed

Check:

* Image folder exists
* File names are correct
* Images are in PNG format
* Path inside the Python code is correct

---

## 🧩 Possible Improvements

Future versions may include:

* Database support using SQLite
* Automatic homing sensor calibration
* Real-time motor position feedback
* QR code or barcode scanning
* User authentication
* Touchscreen optimization
* Dark mode
* Multi-language interface
* Export of cable inventory as CSV or PDF
* Logging of reel usage
* Integration with warehouse management systems
* Web dashboard
* Raspberry Pi deployment

---

## 🎓 Educational Value

This project demonstrates several important engineering and programming concepts:

* Python GUI development
* Object-oriented programming
* Serial communication
* Embedded systems integration
* Arduino motor control
* Industrial user interface design
* Human-machine interaction
* Hardware-software prototyping
* Automation system design
* Clean project structure
* Practical inventory management

---

## 🏭 Use Cases

CableCarousel can be adapted for:

* Cable storage systems
* Industrial warehouses
* Laboratory cable management
* Automated spool selection
* Smart inventory systems
* Educational automation projects
* Production line assistance
* HMI demonstrations
* Embedded systems training
* Logistics prototypes

---

## 📄 requirements.txt

Example `requirements.txt`:

```text
customtkinter
pillow
pyserial
```

---

## 📜 License

This project is released under the **MIT License**.

You are free to use, modify, and distribute this project according to the terms of the MIT License.

---

## 👤 Author

**Amir Mobasheraghdam**
University of Isfahan
Iran

---

## 🏷️ Hashtags

`#CableCarousel` `#Python` `#CustomTkinter` `#Arduino` `#StepperMotor` `#IndustrialAutomation` `#WarehouseManagement` `#GUI` `#OpenSource` `#UniversityOfIsfahan` `#AmirMobasheraghdam` `#HumanMachineInterface` `#HMI` `#Automation` `#IoT` `#EmbeddedSystems` `#CableReel` `#SpoolSelector` `#LogisticsTech` `#SmartWarehouse`

---

## ❤️ Acknowledgement

Made with passion for automation, engineering, and practical software-hardware integration.

**Made with ❤️ by Amir Mobasheraghdam**
University of Isfahan, Iran
