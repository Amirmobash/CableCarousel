#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <Stepper.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

const int STEPS_PER_REV = 2048;
const int NUM_SPOOLS = 10;
const int STEPS_PER_SPOOL = STEPS_PER_REV / NUM_SPOOLS;
Stepper stepper(STEPS_PER_REV, 8, 10, 9, 11);

int currentSpool = 0;

String typ;
String sn;

void setup() {
  Serial.begin(9600);
  stepper.setSpeed(5);

  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
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
    int ziel = Serial.parseInt();
    if (ziel >= 1 && ziel <= NUM_SPOOLS) {
      int zielSpool = ziel - 1;
      int deltaSpool = zielSpool - currentSpool;
      int schritte = deltaSpool * STEPS_PER_SPOOL;

      stepper.step(schritte);
      currentSpool = zielSpool;

      switch (ziel) {
        case 10: typ = "CF77.UL.4"; sn = "AB904401"; break;
        case 9:  typ = "CF98.4.99"; sn = "AB904402"; break;
        case 8:  typ = "CF130.2.4"; sn = "AB904403"; break;
        case 7:  typ = "CF6.12.43"; sn = "AB904404"; break;
        case 6:  typ = "CF9.3.01"; sn = "AB904405"; break;
        case 5:  typ = "CF10.32"; sn = "AB904406"; break;
        case 4:  typ = "CF240.4.5"; sn = "AB904407"; break;
        case 3:  typ = "CF113.1.3"; sn = "AB904408"; break;
        case 2:  typ = "CF211.11"; sn = "AB904409"; break;
        case 1:  typ = "CF29.0"; sn = "AB904410"; break;
        default: typ = "-"; sn = "-"; break;
      }

      zeigeSpule(ziel);
    }
  }
}

void zeigeSpule(int spule) {
  display.clearDisplay();
  display.setTextSize(2);
  display.setCursor(0, 0);
  display.print("Spule: ");
  display.println(spule);

  display.setTextSize(2);
  display.setCursor(0, 20);
  display.print("");
  display.println(typ);

  display.setCursor(0, 45);
  display.print("");
  display.println(sn);

  display.display();
}
