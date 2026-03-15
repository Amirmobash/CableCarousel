/*
 * Spulenauswähler mit Schrittmotor und OLED-Display
 * Autor: AmirMobasheraghdam
 * Datum: 2025
 * 
 * Dieses Programm steuert einen Schrittmotor, um eine von 10 Spulenpositionen anzufahren.
 * Über die serielle Schnittstelle wird die gewünschte Spulennummer (1-10) empfangen.
 * Das OLED-Display zeigt die Spulennummer, den Typ und die Seriennummer an.
 */

#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <Stepper.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

// Schrittmotoreinstellungen
const int SCHRITTE_PRO_UMDREHUNG = 2048;   // Schritte pro Umdrehung (bei 28BYJ-48)
const int ANZAHL_SPULEN = 10;               // Anzahl der Spulenpositionen
const int SCHRITTE_PRO_SPULE = SCHRITTE_PRO_UMDREHUNG / ANZAHL_SPULEN; // Schritte zwischen zwei Spulen
Stepper stepper(SCHRITTE_PRO_UMDREHUNG, 8, 10, 9, 11); // Motor-Pins: IN1, IN3, IN2, IN4

int aktuelleSpule = 0;   // aktuelle Position (0 = Spule 1, 1 = Spule 2, ...)

String typ;
String sn;

void setup() {
  Serial.begin(9600);
  stepper.setSpeed(5);   // Drehzahl in U/min (langsam für gleichmäßige Bewegung)

  // OLED initialisieren
  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    // Falls kein Display gefunden wird, in Endlosschleife hängen
    while (true);
  }

  display.clearDisplay();
  display.setTextSize(2);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(0, 10);
  display.println("Bereit...");
  display.display();
}

void loop() {
  if (Serial.available()) {
    int ziel = Serial.parseInt();              // Ziel-Spulennummer (1-10) einlesen
    if (ziel >= 1 && ziel <= ANZAHL_SPULEN) {
      int zielSpule = ziel - 1;                 // in nullbasierte Index umwandeln
      int deltaSpule = zielSpule - aktuelleSpule; // Differenz der Positionen
      int schritte = deltaSpule * SCHRITTE_PRO_SPULE; // benötigte Schritte

      stepper.step(schritte);                   // Motor verfahren
      aktuelleSpule = zielSpule;                 // neue Position merken

      // Typ und Seriennummer anhand der Spulennummer zuweisen
      switch (ziel) {
        case 10: typ = "CF77.UL.4"; sn = "AB904401"; break;
        case 9:  typ = "CF98.4.99"; sn = "AB904402"; break;
        case 8:  typ = "CF130.2.4"; sn = "AB904403"; break;
        case 7:  typ = "CF6.12.43"; sn = "AB94404";  break;
        case 6:  typ = "CF9.3.01";  sn = "AB904405"; break;
        case 5:  typ = "CF10.32";   sn = "AB904406"; break;
        case 4:  typ = "CF240.4.5"; sn = "AB94407";  break;
        case 3:  typ = "CF113.1.3"; sn = "AB904408"; break;
        case 2:  typ = "CF211.11";  sn = "AB904409"; break;
        case 1:  typ = "CF29.0";    sn = "AB90410";  break;
        default: typ = "-";          sn = "-";       break;
      }

      zeigeSpule(ziel);    // Anzeige aktualisieren
    }
  }
}

// Zeigt die Informationen der angewählten Spule auf dem OLED an
void zeigeSpule(int spule) {
  display.clearDisplay();
  display.setTextSize(2);
  display.setCursor(0, 0);
  display.print("Spule: ");
  display.println(spule);

  display.setTextSize(2);
  display.setCursor(0, 20);
  display.print("Typ: ");
  display.println(typ);

  display.setCursor(0, 45);
  display.print("SN:  ");
  display.println(sn);

  display.display();
}
