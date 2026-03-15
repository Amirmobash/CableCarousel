# CableCarousel 🎡

**Author:** Amir Mobasheraghdam  
**University:** University of Isfahan  

Cable Carousel is a visually interactive user interface developed in Python using **customtkinter**. It enables intuitive control and selection of cable reels (spools) in industrial or logistics environments. The system communicates with an Arduino to drive stepper motors, providing a complete hardware-software solution for automated warehouse management.

---

## 🇬🇧 

Cable Carousel is a modern GUI application designed to manage and select cable reels in a warehouse. It features a clickable carousel of reel images, real-time metadata display, and direct control over an Arduino‑controlled stepper motor. The software is built with **CustomTkinter** for a sleek, professional look and integrates **Pillow** for image processing and **PySerial** for serial communication.

### Features

- Clickable image buttons for each cable reel
- Display of reel metadata: **Type, Color, Serial Number, Length**
- Arduino control via serial port to position the correct reel
- High‑quality, real‑color cable drum images
- Progress bar to visualise motor movement
- Search and filter functionality to quickly find reels

### Requirements

```bash
pip install customtkinter pillow pyserial
```

---

## 🇩🇪 Deutsche Beschreibung

Cable Carousel ist eine visuell interaktive Benutzeroberfläche, die mit Python und **customtkinter** entwickelt wurde. Sie ermöglicht die intuitive Steuerung und Auswahl von Kabeltrommeln (Spulen) in industriellen oder logistischen Umgebungen. Das System kommuniziert mit einem Arduino, um Schrittmotoren anzusteuern, und bietet somit eine komplette Hardware‑Software‑Lösung für die automatisierte Lagerverwaltung.

### Funktionen

- Anklickbare Bildschaltflächen für jede Kabeltrommel
- Anzeige von Metadaten: **Typ, Farbe, Seriennummer, Länge**
- Arduino‑Steuerung über serielle Schnittstelle zur Positionierung der richtigen Spule
- Hochwertige, farbechte Kabeltrommel‑Bilder
- Fortschrittsbalken zur Visualisierung der Motorbewegung
- Such‑ und Filterfunktion für schnelles Auffinden der Spulen

### Voraussetzungen

```bash
pip install customtkinter pillow pyserial
```

---

## 🚀 Getting Started / Erste Schritte

1. **Clone the repository**  
   ```bash
   git clone https://github.com/yourusername/CableCarousel.git
   cd CableCarousel
   ```
2. **Install dependencies** (see above)  
3. **Connect Arduino** with the stepper motor shield and upload the corresponding firmware.  
4. **Run the application**  
   ```bash
   python main.py
   ```

---

## 🛠️ Hardware / Arduino Setup

- **Microcontroller:** Arduino Uno / Nano  
- **Motor driver:** ULN2003 (for 28BYJ-48 stepper) or compatible  
- **Stepper motor:** 28BYJ-48 (or similar)  
- **Wiring:** Connect motor to pins 8,9,10,11 as defined in the Arduino sketch.

The Arduino sketch listens for serial commands (e.g., "5" to go to spool 5) and rotates the motor accordingly.

---

## 📦 Project Structure

```
CableCarousel/
├── main.py                 # Main GUI application
├── arduino/                # Arduino firmware
│   └── cable_carousel.ino
├── assets/                 # Images, icons, etc.
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

---

## 📸 Screenshots

*(Insert screenshots of the application here)*

---

## 📝 License

This project is open source and available under the **MIT License**.

---

## 🏷️ Hashtags

#CableCarousel #Python #CustomTkinter #Arduino #StepperMotor #IndustrialAutomation #WarehouseManagement #GUI #OpenSource #UniversityOfIsfahan #AmirMobasheraghdam #HumanMachineInterface #HMI #Automation #IoT #EmbeddedSystems #CableReel #SpoolSelector #LogisticsTech #SmartWarehouse

---

**Made with ❤️ by Amir Mobasheraghdam**  
University of Isfahan, Iran
```
