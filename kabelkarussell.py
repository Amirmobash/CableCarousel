from __future__ import annotations

import argparse
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import customtkinter as ctk
from PIL import Image, ImageDraw

try:
    import serial
except ModuleNotFoundError:
    serial = None


@dataclass(frozen=True)
class Cable:
    trommel: int
    farbe: str
    kabeltyp: str
    seriennummer: str
    laenge: float


KABEL_DB = (
    Cable(10, "Gelb", "CF29", "AB904410", 53.2),
    Cable(9, "Rot", "CF211", "AB904409", 68.0),
    Cable(8, "Braun", "CF113", "AB904408", 41.7),
    Cable(7, "Silber", "CF240", "AB904407", 88.3),
    Cable(6, "Orange", "CF10", "AB904406", 35.5),
    Cable(5, "Rosa", "CF9", "AB904405", 72.6),
    Cable(4, "Schwarz", "CF6", "AB904404", 61.0),
    Cable(3, "Grau", "CF130", "AB904403", 47.9),
    Cable(2, "Weiß", "CF98", "AB904402", 39.4),
    Cable(1, "Grün", "CF77.UL", "AB904401", 56.8),
)

MAX_LAENGE = max(cable.laenge for cable in KABEL_DB)

COLOR_MAP = {
    "Gelb": "#F6D84A",
    "Rot": "#D94444",
    "Braun": "#8A5A3C",
    "Silber": "#BFC5CC",
    "Orange": "#F49A38",
    "Rosa": "#EFA7C8",
    "Schwarz": "#202124",
    "Grau": "#8A8F98",
    "Weiß": "#FFFFFF",
    "Grün": "#2E8B57",
}

IMAGE_NAMES = {
    "Gelb": ("Gelb.png", "gelb.png", "yellow.png"),
    "Rot": ("Rot.png", "rot.png", "red.png"),
    "Braun": ("Braun.png", "braun.png", "brown.png"),
    "Silber": ("Silber.png", "silber.png", "silver.png"),
    "Orange": ("Orange.png", "orange.png"),
    "Rosa": ("Rosa.png", "rosa.png", "pink.png"),
    "Schwarz": ("Schwarz.png", "schwarz.png", "black.png"),
    "Grau": ("Grau.png", "grau.png", "gray.png", "grey.png"),
    "Weiß": ("Weiß.png", "Weiss.png", "weiss.png", "white.png"),
    "Grün": ("Grün.png", "Gruen.png", "gruen.png", "green.png"),
}


class ArduinoClient:
    def __init__(self, port: str, baudrate: int) -> None:
        self.port = port
        self.baudrate = baudrate
        self.connection = None
        self.last_error = ""

    @property
    def is_connected(self) -> bool:
        return self.connection is not None and getattr(self.connection, "is_open", False)

    def connect(self) -> bool:
        self.close()

        if serial is None:
            self.last_error = "pyserial ist nicht installiert"
            return False

        try:
            self.connection = serial.Serial(self.port, self.baudrate, timeout=1)
            time.sleep(2)
            self.last_error = ""
            return True
        except Exception as exc:
            self.connection = None
            self.last_error = str(exc)
            return False

    def send_trommel(self, trommel: int) -> bool:
        if not self.is_connected:
            self.last_error = "Arduino ist nicht verbunden"
            return False

        try:
            self.connection.write(f"{trommel}\n".encode("utf-8"))
            self.connection.flush()
            self.last_error = ""
            return True
        except Exception as exc:
            self.last_error = str(exc)
            return False

    def close(self) -> None:
        if self.connection is not None:
            try:
                self.connection.close()
            except Exception:
                pass
            self.connection = None


class KabelKarussellApp(ctk.CTk):
    def __init__(self, port: str, baudrate: int, fullscreen: bool) -> None:
        super().__init__()

        self.port = port
        self.baudrate = baudrate
        self.fullscreen_enabled = fullscreen
        self.arduino = ArduinoClient(port, baudrate)
        self.image_dir = Path(__file__).resolve().parent / "kabelkarussell_recolored"
        self.images: dict[str, ctk.CTkImage] = {}
        self.selected_cable: Optional[Cable] = None
        self.search_var = ctk.StringVar()

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.title("KabelKarussell")
        self.geometry("1280x820")
        self.minsize(1050, 700)
        self.attributes("-fullscreen", self.fullscreen_enabled)

        self.bind("<Escape>", lambda event: self.exit_fullscreen())
        self.bind("<F11>", lambda event: self.toggle_fullscreen())

        self.configure(fg_color="#F4F7FB")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.create_header()
        self.create_main_area()
        self.create_status_bar()

        self.search_var.trace_add("write", lambda *_: self.render_cards())

        self.render_cards()
        self.after(250, self.connect_arduino)

    def create_header(self) -> None:
        header = ctk.CTkFrame(self, corner_radius=0, fg_color="#FFFFFF", height=92)
        header.grid(row=0, column=0, sticky="ew")
        header.grid_columnconfigure(1, weight=1)

        title_box = ctk.CTkFrame(header, fg_color="transparent")
        title_box.grid(row=0, column=0, padx=28, pady=18, sticky="w")

        title = ctk.CTkLabel(
            title_box,
            text="KabelKarussell",
            font=ctk.CTkFont(family="Arial Black", size=30),
            text_color="#162033",
        )
        title.pack(anchor="w")

        subtitle = ctk.CTkLabel(
            title_box,
            text="Trommel auswählen, Kabeldaten prüfen und Arduino ansteuern",
            font=ctk.CTkFont(size=13),
            text_color="#667085",
        )
        subtitle.pack(anchor="w", pady=(2, 0))

        search_box = ctk.CTkFrame(header, fg_color="transparent")
        search_box.grid(row=0, column=1, padx=20, pady=18, sticky="ew")
        search_box.grid_columnconfigure(0, weight=1)

        self.search_entry = ctk.CTkEntry(
            search_box,
            textvariable=self.search_var,
            placeholder_text="Nach Trommel, Kabeltyp, Farbe oder Seriennummer suchen",
            height=42,
            corner_radius=14,
            border_width=1,
            font=ctk.CTkFont(size=14),
        )
        self.search_entry.grid(row=0, column=0, sticky="ew")

        clear_button = ctk.CTkButton(
            search_box,
            text="Leeren",
            width=80,
            height=42,
            corner_radius=14,
            command=self.clear_search,
        )
        clear_button.grid(row=0, column=1, padx=(10, 0))

        action_box = ctk.CTkFrame(header, fg_color="transparent")
        action_box.grid(row=0, column=2, padx=28, pady=18, sticky="e")

        self.connection_label = ctk.CTkLabel(
            action_box,
            text="Arduino wird geprüft",
            width=170,
            height=32,
            corner_radius=16,
            fg_color="#FFF4D6",
            text_color="#8A6100",
            font=ctk.CTkFont(size=13, weight="bold"),
        )
        self.connection_label.pack(anchor="e", pady=(0, 8))

        buttons = ctk.CTkFrame(action_box, fg_color="transparent")
        buttons.pack(anchor="e")

        reconnect_button = ctk.CTkButton(
            buttons,
            text="Verbinden",
            width=92,
            height=34,
            corner_radius=12,
            command=self.connect_arduino,
        )
        reconnect_button.grid(row=0, column=0, padx=(0, 8))

        close_button = ctk.CTkButton(
            buttons,
            text="Schließen",
            width=92,
            height=34,
            corner_radius=12,
            fg_color="#E5484D",
            hover_color="#C9363B",
            command=self.on_close,
        )
        close_button.grid(row=0, column=1)

    def create_main_area(self) -> None:
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.grid(row=1, column=0, sticky="nsew", padx=24, pady=22)
        main.grid_columnconfigure(0, weight=3)
        main.grid_columnconfigure(1, weight=1)
        main.grid_rowconfigure(0, weight=1)

        left_panel = ctk.CTkFrame(main, corner_radius=22, fg_color="#FFFFFF")
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 18))
        left_panel.grid_columnconfigure(0, weight=1)
        left_panel.grid_rowconfigure(1, weight=1)

        left_title = ctk.CTkFrame(left_panel, fg_color="transparent")
        left_title.grid(row=0, column=0, sticky="ew", padx=22, pady=(20, 8))
        left_title.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            left_title,
            text="Trommeln",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#162033",
        ).grid(row=0, column=0, sticky="w")

        self.result_count_label = ctk.CTkLabel(
            left_title,
            text="",
            font=ctk.CTkFont(size=13),
            text_color="#667085",
        )
        self.result_count_label.grid(row=0, column=1, sticky="e")

        self.card_frame = ctk.CTkScrollableFrame(
            left_panel,
            fg_color="transparent",
            corner_radius=0,
            scrollbar_button_color="#CBD5E1",
            scrollbar_button_hover_color="#94A3B8",
        )
        self.card_frame.grid(row=1, column=0, sticky="nsew", padx=14, pady=(0, 16))

        for col in range(4):
            self.card_frame.grid_columnconfigure(col, weight=1)

        self.detail_panel = ctk.CTkFrame(main, corner_radius=22, fg_color="#FFFFFF")
        self.detail_panel.grid(row=0, column=1, sticky="nsew")
        self.detail_panel.grid_columnconfigure(0, weight=1)

        self.create_detail_panel()

    def create_detail_panel(self) -> None:
        ctk.CTkLabel(
            self.detail_panel,
            text="Details",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#162033",
        ).grid(row=0, column=0, sticky="w", padx=24, pady=(24, 4))

        self.detail_title = ctk.CTkLabel(
            self.detail_panel,
            text="Keine Trommel ausgewählt",
            font=ctk.CTkFont(size=17, weight="bold"),
            text_color="#334155",
            wraplength=300,
        )
        self.detail_title.grid(row=1, column=0, sticky="w", padx=24, pady=(8, 20))

        self.preview_label = ctk.CTkLabel(self.detail_panel, text="")
        self.preview_label.grid(row=2, column=0, pady=(0, 16))

        self.color_chip = ctk.CTkFrame(
            self.detail_panel,
            width=220,
            height=42,
            corner_radius=16,
            fg_color="#E5E7EB",
            border_width=1,
            border_color="#D0D5DD",
        )
        self.color_chip.grid(row=3, column=0, sticky="ew", padx=24, pady=(0, 18))
        self.color_chip.grid_propagate(False)

        self.color_chip_label = ctk.CTkLabel(
            self.color_chip,
            text="Farbe: -",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#162033",
        )
        self.color_chip_label.place(relx=0.5, rely=0.5, anchor="center")

        self.detail_values: dict[str, ctk.CTkLabel] = {}
        fields = ("Seriennummer", "Kabeltyp", "Trommel", "Länge")

        fields_frame = ctk.CTkFrame(self.detail_panel, fg_color="transparent")
        fields_frame.grid(row=4, column=0, sticky="ew", padx=24, pady=(0, 18))
        fields_frame.grid_columnconfigure(1, weight=1)

        for row, field in enumerate(fields):
            label = ctk.CTkLabel(
                fields_frame,
                text=field,
                font=ctk.CTkFont(size=13),
                text_color="#667085",
            )
            label.grid(row=row, column=0, sticky="w", pady=7)

            value = ctk.CTkLabel(
                fields_frame,
                text="-",
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color="#162033",
                anchor="e",
            )
            value.grid(row=row, column=1, sticky="e", pady=7)
            self.detail_values[field] = value

        ctk.CTkLabel(
            self.detail_panel,
            text="Kabellänge",
            font=ctk.CTkFont(size=13),
            text_color="#667085",
        ).grid(row=5, column=0, sticky="w", padx=24, pady=(4, 8))

        self.length_progress = ctk.CTkProgressBar(self.detail_panel, height=14, corner_radius=8)
        self.length_progress.grid(row=6, column=0, sticky="ew", padx=24, pady=(0, 22))
        self.length_progress.set(0)

        self.send_button = ctk.CTkButton(
            self.detail_panel,
            text="Trommel erneut senden",
            height=44,
            corner_radius=14,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.resend_selected,
            state="disabled",
        )
        self.send_button.grid(row=7, column=0, sticky="ew", padx=24, pady=(0, 12))

        self.message_label = ctk.CTkLabel(
            self.detail_panel,
            text="Wähle links eine Trommel aus.",
            font=ctk.CTkFont(size=13),
            text_color="#667085",
            wraplength=300,
        )
        self.message_label.grid(row=8, column=0, sticky="ew", padx=24, pady=(0, 20))

    def create_status_bar(self) -> None:
        status = ctk.CTkFrame(self, corner_radius=0, fg_color="#FFFFFF", height=42)
        status.grid(row=2, column=0, sticky="ew")
        status.grid_columnconfigure(0, weight=1)

        self.status_label = ctk.CTkLabel(
            status,
            text=f"Port: {self.port}    Baudrate: {self.baudrate}",
            font=ctk.CTkFont(size=12),
            text_color="#667085",
        )
        self.status_label.grid(row=0, column=0, sticky="w", padx=24)

        shortcuts = ctk.CTkLabel(
            status,
            text="ESC: Fensteransicht    F11: Vollbild",
            font=ctk.CTkFont(size=12),
            text_color="#667085",
        )
        shortcuts.grid(row=0, column=1, sticky="e", padx=24)

    def render_cards(self) -> None:
        for widget in self.card_frame.winfo_children():
            widget.destroy()

        query = self.search_var.get().strip().lower()
        visible_cables = [
            cable for cable in KABEL_DB
            if query in self.search_text(cable)
        ]

        self.result_count_label.configure(text=f"{len(visible_cables)} von {len(KABEL_DB)}")

        if not visible_cables:
            empty = ctk.CTkLabel(
                self.card_frame,
                text="Keine passende Trommel gefunden",
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color="#667085",
            )
            empty.grid(row=0, column=0, columnspan=4, pady=60)
            return

        for index, cable in enumerate(visible_cables):
            row = index // 4
            col = index % 4
            self.create_card(cable, row, col)

    def create_card(self, cable: Cable, row: int, col: int) -> None:
        selected = self.selected_cable == cable
        border_color = "#2563EB" if selected else "#E2E8F0"
        fg_color = "#EFF6FF" if selected else "#FFFFFF"

        card = ctk.CTkFrame(
            self.card_frame,
            corner_radius=18,
            fg_color=fg_color,
            border_width=2 if selected else 1,
            border_color=border_color,
        )
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        card.grid_columnconfigure(0, weight=1)

        image = self.get_cable_image(cable.farbe)

        image_label = ctk.CTkLabel(card, text="", image=image)
        image_label.grid(row=0, column=0, pady=(16, 8))

        title = ctk.CTkLabel(
            card,
            text=f"Trommel {cable.trommel}",
            font=ctk.CTkFont(size=17, weight="bold"),
            text_color="#162033",
        )
        title.grid(row=1, column=0, pady=(2, 0))

        meta = ctk.CTkLabel(
            card,
            text=f"{cable.kabeltyp} · {cable.farbe}\n{cable.laenge:.1f} m",
            font=ctk.CTkFont(size=13),
            text_color="#667085",
            justify="center",
        )
        meta.grid(row=2, column=0, pady=(4, 14))

        button = ctk.CTkButton(
            card,
            text="Auswählen",
            height=34,
            corner_radius=12,
            command=lambda selected_cable=cable: self.select_cable(selected_cable),
        )
        button.grid(row=3, column=0, sticky="ew", padx=14, pady=(0, 14))

        for widget in (card, image_label, title, meta):
            widget.bind("<Button-1>", lambda event, selected_cable=cable: self.select_cable(selected_cable))

    def select_cable(self, cable: Cable) -> None:
        self.selected_cable = cable
        self.update_details(cable)
        self.send_selected(cable)
        self.render_cards()

    def update_details(self, cable: Cable) -> None:
        self.detail_title.configure(text=f"Trommel {cable.trommel} ausgewählt")
        self.preview_label.configure(image=self.get_cable_image(cable.farbe))
        self.color_chip.configure(fg_color=COLOR_MAP.get(cable.farbe, "#E5E7EB"))
        self.color_chip_label.configure(text=f"Farbe: {cable.farbe}")
        self.detail_values["Seriennummer"].configure(text=cable.seriennummer)
        self.detail_values["Kabeltyp"].configure(text=cable.kabeltyp)
        self.detail_values["Trommel"].configure(text=str(cable.trommel))
        self.detail_values["Länge"].configure(text=f"{cable.laenge:.1f} m")
        self.length_progress.set(cable.laenge / MAX_LAENGE)
        self.send_button.configure(state="normal")

    def send_selected(self, cable: Cable) -> None:
        if self.arduino.send_trommel(cable.trommel):
            self.message_label.configure(
                text=f"Trommel {cable.trommel} wurde an Arduino gesendet.",
                text_color="#15803D",
            )
        else:
            self.message_label.configure(
                text=f"Trommel ausgewählt, aber nicht gesendet: {self.arduino.last_error}",
                text_color="#B42318",
            )

        self.update_connection_state()

    def resend_selected(self) -> None:
        if self.selected_cable is not None:
            self.send_selected(self.selected_cable)

    def connect_arduino(self) -> None:
        self.connection_label.configure(
            text="Verbinde...",
            fg_color="#FFF4D6",
            text_color="#8A6100",
        )
        self.update_idletasks()

        if self.arduino.connect():
            self.message_label.configure(
                text=f"Arduino ist verbunden über {self.port}.",
                text_color="#15803D",
            )
        else:
            self.message_label.configure(
                text=f"Arduino nicht verbunden: {self.arduino.last_error}",
                text_color="#B42318",
            )

        self.update_connection_state()

    def update_connection_state(self) -> None:
        if self.arduino.is_connected:
            self.connection_label.configure(
                text="Arduino verbunden",
                fg_color="#DCFCE7",
                text_color="#166534",
            )
        else:
            self.connection_label.configure(
                text="Nicht verbunden",
                fg_color="#FEE2E2",
                text_color="#991B1B",
            )

    def get_cable_image(self, farbe: str) -> ctk.CTkImage:
        if farbe in self.images:
            return self.images[farbe]

        image = self.load_image_file(farbe)
        if image is None:
            image = self.create_fallback_image(farbe)

        ctk_image = ctk.CTkImage(light_image=image, dark_image=image, size=(96, 96))
        self.images[farbe] = ctk_image
        return ctk_image

    def load_image_file(self, farbe: str) -> Optional[Image.Image]:
        for filename in IMAGE_NAMES.get(farbe, (f"{farbe}.png",)):
            path = self.image_dir / filename
            if path.exists():
                try:
                    return Image.open(path).convert("RGBA").resize((160, 160))
                except Exception:
                    return None
        return None

    def create_fallback_image(self, farbe: str) -> Image.Image:
        size = 160
        color = COLOR_MAP.get(farbe, "#9CA3AF")
        image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)

        draw.rounded_rectangle((18, 18, 142, 142), radius=34, fill="#F8FAFC", outline="#CBD5E1", width=3)
        draw.ellipse((42, 42, 118, 118), fill=color, outline="#334155", width=5)
        draw.ellipse((66, 66, 94, 94), fill="#FFFFFF", outline="#CBD5E1", width=3)

        if farbe == "Weiß":
            draw.ellipse((42, 42, 118, 118), fill="#FFFFFF", outline="#94A3B8", width=5)
            draw.ellipse((66, 66, 94, 94), fill="#F8FAFC", outline="#CBD5E1", width=3)

        return image

    def search_text(self, cable: Cable) -> str:
        return f"{cable.trommel} {cable.farbe} {cable.kabeltyp} {cable.seriennummer} {cable.laenge}".lower()

    def clear_search(self) -> None:
        self.search_var.set("")
        self.search_entry.focus_set()

    def toggle_fullscreen(self) -> None:
        self.fullscreen_enabled = not self.fullscreen_enabled
        self.attributes("-fullscreen", self.fullscreen_enabled)

    def exit_fullscreen(self) -> None:
        self.fullscreen_enabled = False
        self.attributes("-fullscreen", False)

    def on_close(self) -> None:
        self.arduino.close()
        self.destroy()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", default="COM9")
    parser.add_argument("--baudrate", type=int, default=9600)
    parser.add_argument("--windowed", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    app = KabelKarussellApp(
        port=args.port,
        baudrate=args.baudrate,
        fullscreen=not args.windowed,
    )
    app.protocol("WM_DELETE_WINDOW", app.on_close)
    app.mainloop()


if __name__ == "__main__":
    main()
