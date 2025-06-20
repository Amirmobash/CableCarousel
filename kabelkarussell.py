import customtkinter as ctk
import serial
import time
from PIL import Image, ImageTk, ImageSequence
import os
import requests
from io import BytesIO

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# --- Kabel-Datenbank ---
kabel_db = [
  {"Trommel": 10, "Farbe": "Gelb", "Kabeltyp": "CF29", "Seriennummer": "AB904410", "Laenge": 53.2},
  {"Trommel": 9,  "Farbe": "Rot", "Kabeltyp": "CF211", "Seriennummer": "AB904409", "Laenge": 68.0},
  {"Trommel": 8,  "Farbe": "Braun", "Kabeltyp": "CF113", "Seriennummer": "AB904408", "Laenge": 41.7},
  {"Trommel": 7,  "Farbe": "Silber", "Kabeltyp": "CF240", "Seriennummer": "AB904407", "Laenge": 88.3},
  {"Trommel": 6,  "Farbe": "Orange", "Kabeltyp": "CF10", "Seriennummer": "AB904406", "Laenge": 35.5},
  {"Trommel": 5,  "Farbe": "Rosa", "Kabeltyp": "CF9", "Seriennummer": "AB904405", "Laenge": 72.6},
  {"Trommel": 4,  "Farbe": "Schwarz", "Kabeltyp": "CF6", "Seriennummer": "AB904404", "Laenge": 61.0},
  {"Trommel": 3,  "Farbe": "Grau", "Kabeltyp": "CF130", "Seriennummer": "AB904403", "Laenge": 47.9},
  {"Trommel": 2,  "Farbe": "Weiß", "Kabeltyp": "CF98", "Seriennummer": "AB904402", "Laenge": 39.4},
  {"Trommel": 1,  "Farbe": "Grün", "Kabeltyp": "CF77.UL", "Seriennummer": "AB904401", "Laenge": 56.8}
]

# Maximale erwartete Kabellaenge zur Normalisierung
MAX_LAENGE = max([k["Laenge"] for k in kabel_db])

try:
    arduino = serial.Serial('COM9', 9600, timeout=1)
    time.sleep(2)
except:
    arduino = None

root = ctk.CTk()
root.title("KabelKarussell")
root.attributes('-fullscreen', True)

label_title = ctk.CTkLabel(root, text="KabelKarussell", font=("Arial Black", 28))
label_title.pack(pady=10)

search_frame = ctk.CTkFrame(root)
search_frame.pack(pady=5)
search_entry = ctk.CTkEntry(search_frame, placeholder_text="Filter nach Kabeltyp oder Farbe", width=400)
search_entry.pack()

frame_grid = ctk.CTkScrollableFrame(root, width=900, height=360)
frame_grid.pack(pady=10)

info_frame = ctk.CTkFrame(root)
info_frame.pack(pady=15, fill="x", padx=20)

info_text = ctk.CTkLabel(info_frame, text="Wähle eine Kabeltrommel aus", font=("Arial", 16))
info_text.pack(pady=10)

label_sn = ctk.CTkLabel(info_frame, text="Seriennummer: -")
label_sn.pack()
label_typ = ctk.CTkLabel(info_frame, text="Kabeltyp: -")
label_typ.pack()
label_farbe = ctk.CTkLabel(info_frame, text="Farbe: -")
label_farbe.pack()
color_label = ctk.CTkLabel(info_frame, text=" ", width=20, height=20, fg_color="gray")
color_label.pack()
label_laenge = ctk.CTkLabel(info_frame, text="Länge: -")
label_laenge.pack()

progress = ctk.CTkProgressBar(info_frame, width=300)
progress.pack(pady=10)
progress.set(0)

animation_label = ctk.CTkLabel(root, text="")
animation_label.pack(pady=5)

def lade_bild(farbe=None):
    try:
        if farbe:
            filename = f"kabelkarussell_recolored/{farbe}.png"
        else:
            filename = "kabelkarussell_recolored/Gruen.png"
        path = os.path.join(os.path.dirname(__file__), filename)
        image = Image.open(path).resize((100, 100))
        return ImageTk.PhotoImage(image)
    except:
        return None
    except:
        return None
    except:
        return None
    except:
        return None

def farbe_hex(name):
    farben = {
        "Gelb": "#FFFF00", "Rot": "#FF0000", "Braun": "#8B4513", "Silber": "#C0C0C0",
        "Orange": "#FFA500", "Rosa": "#FFC0CB", "Schwarz": "#000000", "Grau": "#808080",
        "Weiß": "#FFFFFF", "Grün": "#008000"
    }
    return farben.get(name, "#AAAAAA")

def sende_trommel(index):
    daten = kabel_db[index]
    global img_tk
    img_tk = lade_bild(daten['Farbe'])
    if arduino:
        arduino.write(f"{daten['Trommel']}
".encode())
        info_text.configure(text=f"Trommel {daten['Trommel']} gesendet")
    else:
        info_text.configure(text="⚠️ Arduino nicht verbunden")

    label_sn.configure(text=f"Seriennummer: {daten['Seriennummer']}")
    label_typ.configure(text=f"Kabeltyp: {daten['Kabeltyp']}")
    label_farbe.configure(text=f"Farbe: {daten['Farbe']}" )
    color_label.configure(fg_color=farbe_hex(daten['Farbe']))
    label_laenge.configure(text=f"Länge: {daten['Laenge']} m")
    progress.set(daten['Laenge'] / MAX_LAENGE)

    animation_label.configure(text="[Bild geladen]")

def update_filter(*args):
    query = search_entry.get().lower()
    for widget in frame_grid.winfo_children():
        widget.destroy()
    for i, kabel in enumerate(kabel_db):
        if query in kabel['Kabeltyp'].lower() or query in kabel['Farbe'].lower():
            row = i // 5
            col = i % 5
            btn = ctk.CTkButton(frame_grid, text=f"Trommel {kabel['Trommel']}", width=120, height=100,
                                image=img_tk, compound="top", command=lambda i=i: sende_trommel(i))
            btn.grid(row=row, column=col, padx=10, pady=10)

img_tk = lade_bild("Grün")  # Standardbild
search_entry.bind("<KeyRelease>", update_filter)
update_filter()

root.mainloop()
