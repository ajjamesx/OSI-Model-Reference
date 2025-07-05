from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk
import os

class OSIModelApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("OSI Model Reference")
        self.geometry("900x650")
        self.configure(bg="#1e1e2e")

        self.tab_control = ttk.Notebook(self)
        self.layer_tabs = {}
        self.layer_images = {}

        self.create_text_tabs()
        self.create_visualization_tab()

        self.tab_control.pack(expand=1, fill="both")

    def load_image(self, name, max_size=(300, 300)):
        try:
            path = os.path.join(os.getcwd(), f"{name.lower().replace(' ', '_')}.png")
            img = Image.open(path)
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            tk_img = ImageTk.PhotoImage(img)
            self.layer_images[name] = tk_img
            return tk_img
        except Exception as e:
            print(f"Failed to load image for {name}: {e}")
            return None


    def create_text_tabs(self):
        layers = [
            ("Physical", "🔌 Handles raw bit transmission over physical media.\n\nConfiguration Tips:\n• Check cables, power\n• Use tools like cable testers\n• Look for link lights."),
            ("Data Link", "🧾 Responsible for MAC addressing and framing.\n\nConfiguration Tips:\n• Verify ARP cache\n• Fix duplex mismatches\n• Troubleshoot VLAN settings."),
            ("Network", "🗺️ Manages routing and IP addressing.\n\nConfiguration Tips:\n• Check routing tables\n• Ping gateways\n• Verify DNS settings."),
            ("Transport", "🚚 Ensures reliable data transfer via TCP/UDP.\n\nConfiguration Tips:\n• Validate firewall rules\n• Use netstat to check ports\n• Monitor retransmissions."),
            ("Session", "💬 Maintains connections between apps.\n\nConfiguration Tips:\n• Check session logs\n• Manage authentication\n• Observe session lifetimes."),
            ("Presentation", "🖼️ Translates data formats and handles encryption.\n\nConfiguration Tips:\n• Analyze SSL/TLS handshakes\n• Verify encoding issues\n• Use certificate validators."),
            ("Application", "🗣️ Provides services like web, email, and FTP.\n\nConfiguration Tips:\n• Use curl/telnet to test services\n• Check logs for errors\n• Review API responses.")
        ]

        for name, description in layers:
            tab = tk.Frame(self.tab_control, bg="#2d2d2d")

            # Create a vertical container for image + text
            content_frame = tk.Frame(tab, bg="#2d2d2d")
            content_frame.pack(expand=True, fill="both", padx=10, pady=10)

            img = self.load_image(name)
            if img:
                img_label = tk.Label(content_frame, image=img, bg="#2d2d2d")
                img_label.image = img  # Prevent GC
                img_label.pack(pady=(10, 5))

            text_widget = tk.Text(content_frame, bg="#2d2d2d", fg="#ffffff", wrap="word",
                                font=("Segoe UI", 12), relief="flat", height=12)
            text_widget.insert("1.0", description)
            text_widget.config(state="disabled")
            text_widget.pack(expand=True, fill="both")

            self.tab_control.add(tab, text=name)
            self.layer_tabs[name] = tab

    def create_visualization_tab(self):
        self.viz_tab = tk.Frame(self.tab_control, bg="#1e1e2e")
        self.canvas = tk.Canvas(self.viz_tab, bg="#1e1e2e", highlightthickness=0)
        self.canvas.pack(expand=True, fill="both")

        self.tooltip = tk.Label(self.canvas, bg="#f0f0f0", fg="#1e1e2e",
                                font=("Segoe UI", 10), bd=1, relief="solid", wraplength=220)
        self.tooltip.place_forget()

        self.layer_info = {
            "Application": "Handles web, email, FTP protocols.\nTools: curl, browser dev console.",
            "Presentation": "Encrypts/formats data.\nCheck TLS handshakes, encoding.",
            "Session": "Manages connection states.\nMonitor logs, auth cycles.",
            "Transport": "Controls flow via TCP/UDP.\nTroubleshoot ports, firewalls.",
            "Network": "Routes packets via IP.\nVerify DNS, routing tables.",
            "Data Link": "Transmits frames.\nFix MAC conflicts, ARP cache.",
            "Physical": "Moves bits over media.\nInspect cable, signal, power."
        }

        layers = list(self.layer_info.keys())
        self.packet = None
        self.current_layer = 0
        self.width = 700
        self.box_height = 60
        self.spacing = 20
        start_y = 50
        self.start_x = 100 + self.width / 2
        self.layer_positions = []

        for i, layer in enumerate(layers):
            y = start_y + i * (self.box_height + self.spacing)
            self.layer_positions.append(y + self.box_height / 2)
            tag = f"layer_{i}"

            self.canvas.create_rectangle(100, y, 100 + self.width, y + self.box_height,
                                         fill="#3a3f58", outline="#5a5a7a", width=2, tags=(tag,))
            self.canvas.create_text(100 + self.width / 2, y + self.box_height / 2,
                                    text=f"{layer} Layer", fill="#ffffff",
                                    font=("Segoe UI", 14, "bold"), tags=(tag,))
            self.canvas.tag_bind(tag, "<Enter>", lambda e, l=layer: self.show_tooltip(e, l))
            self.canvas.tag_bind(tag, "<Leave>", self.hide_tooltip)
            self.canvas.tag_bind(tag, "<Button-1>", lambda e, l=layer: self.open_tab(l))

            if i < len(layers) - 1:
                arrow_y = y + self.box_height + self.spacing / 2
                self.canvas.create_line(100 + self.width / 2, arrow_y - 20,
                                        100 + self.width / 2, arrow_y,
                                        arrow=tk.LAST, fill="#5a5a7a", width=2)

        self.packet = self.canvas.create_oval(self.start_x - 15, self.layer_positions[0] - 15,
                                              self.start_x + 15, self.layer_positions[0] + 15,
                                              fill="#80ff80", outline="")
        self.animate_packet()
        self.tab_control.add(self.viz_tab, text="Visualization")

    def animate_packet(self):
        if self.current_layer >= len(self.layer_positions):
            self.current_layer = 0
        target_y = self.layer_positions[self.current_layer]
        x = self.start_x
        self.canvas.coords(self.packet, x - 15, target_y - 15, x + 15, target_y + 15)
        self.current_layer += 1
        self.after(1000, self.animate_packet)

    def show_tooltip(self, event, layer_name):
        text = self.layer_info.get(layer_name, "No info available.")
        self.tooltip.config(text=text)
        self.tooltip.place(x=event.x + 20, y=event.y + 20)

    def hide_tooltip(self, event):
        self.tooltip.place_forget()

    def open_tab(self, layer_name):
        tab = self.layer_tabs.get(layer_name)
        if tab:
            self.tab_control.select(tab)

if __name__ == "__main__":
    OSIModelApp().mainloop()