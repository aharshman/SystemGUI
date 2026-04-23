import customtkinter as ctk
import psutil
import platform
import socket
from datetime import datetime

# --- Theme Configuration ---
ctk.set_appearance_mode("Dark")

def get_windows_version():
    """Detailed check for Windows 11 vs 10 using build numbers."""
    if platform.system() == "Windows":
        try:
            build = int(platform.version().split('.')[-1])
            return "Windows 11" if build >= 22000 else "Windows 10"
        except: 
            return "Windows Desktop"
    return f"{platform.system()} {platform.release()}"

class CircularGauge(ctk.CTkCanvas):
    """Custom High-Density Circular Gauge."""
    def __init__(self, master, size=110, label="CPU", bg_color="#161616", **kwargs):
        super().__init__(master, width=size, height=size, bg=bg_color, highlightthickness=0, **kwargs)
        self.size, self.label_text, self.percent = size, label, 0
        self.draw_gauge()

    def draw_gauge(self):
        self.delete("all")
        pad, width = 10, 6
        # Track
        self.create_arc(pad, pad, self.size-pad, self.size-pad, start=0, extent=359, outline="#333", width=width, style="arc")
        # Value Arc
        color = "#3B8ED0" if self.percent < 70 else "#f1c40f" if self.percent < 90 else "#e74c3c"
        self.create_arc(pad, pad, self.size-pad, self.size-pad, start=90, extent=-(self.percent/100)*359, outline=color, width=width, style="arc")
        # Text (Force White)
        self.create_text(self.size/2, self.size/2-5, text=f"{int(self.percent)}%", fill="white", font=("Segoe UI", 11, "bold"))
        self.create_text(self.size/2, self.size/2+12, text=self.label_text, fill="white", font=("Segoe UI", 7, "bold"))

    def update_value(self, value):
        if self.percent != value:
            self.percent = value
            self.draw_gauge()

class CommandHUD(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.cpu_count = psutil.cpu_count() # Get logical cores for percentage normalization
        self.geometry("420x650")
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.attributes("-alpha", 0.98)
        self.configure(fg_color="#0a0a0a")

        self.start_net = psutil.net_io_counters()
        self.last_net = self.start_net
        self.boot_time = datetime.fromtimestamp(psutil.boot_time())
        
        self.setup_ui()
        self.update_stats()

    def setup_ui(self):
        # --- DRAGGABLE HEADER ---
        self.header = ctk.CTkFrame(self, fg_color="#161616", height=50, corner_radius=0)
        self.header.pack(fill="x")
        
        self.title_label = ctk.CTkLabel(self.header, text="CORE_COMMAND_PRO", font=("Consolas", 13, "bold"), text_color="white")
        self.title_label.pack(pady=12)
        
        self.title_label.bind("<ButtonPress-1>", self.start_move)
        self.title_label.bind("<B1-Motion>", self.do_move)
        
        ctk.CTkButton(self.header, text="✕", width=25, height=25, fg_color="transparent", hover_color="#c0392b", text_color="white", command=self.destroy).place(x=385, y=12)

        # --- GAUGE SECTION ---
        g_frame = ctk.CTkFrame(self, fg_color="transparent")
        g_frame.pack(pady=20)
        
        self.cpu_card = ctk.CTkFrame(g_frame, fg_color="#161616", corner_radius=15)
        self.cpu_card.pack(side="left", padx=10)
        self.cpu_gauge = CircularGauge(self.cpu_card, label="CPU LOAD")
        self.cpu_gauge.pack(padx=10, pady=10)

        self.ram_card = ctk.CTkFrame(g_frame, fg_color="#161616", corner_radius=15)
        self.ram_card.pack(side="left", padx=10)
        self.ram_gauge = CircularGauge(self.ram_card, label="RAM LOAD")
        self.ram_gauge.pack(padx=10, pady=10)

        # --- DATA CONSOLE (All White Text) ---
        self.console = ctk.CTkTextbox(self, font=("Consolas", 11), fg_color="#050505", border_width=1, border_color="#222", text_color="white")
        self.console.pack(fill="both", expand=True, padx=25, pady=(0, 25))

    def start_move(self, event):
        self.x, self.y = event.x, event.y

    def do_move(self, event):
        x = self.winfo_x() + event.x - self.x
        y = self.winfo_y() + event.y - self.y
        self.geometry(f"+{x}+{y}")

    def update_stats(self):
        now = datetime.now().strftime("%H:%M:%S")
        self.title_label.configure(text=f"HUD_CORE | {now}")

        self.cpu_gauge.update_value(psutil.cpu_percent())
        self.ram_gauge.update_value(psutil.virtual_memory().percent)

        net_now = psutil.net_io_counters()
        down_speed = (net_now.bytes_recv - self.last_net.bytes_recv) / 1024
        up_speed = (net_now.bytes_sent - self.last_net.bytes_sent) / 1024
        
        session_down = (net_now.bytes_recv - self.start_net.bytes_recv) / (1024**2)
        session_up = (net_now.bytes_sent - self.start_net.bytes_sent) / (1024**2)
        self.last_net = net_now

        disk = psutil.disk_usage('/')
        batt = psutil.sensors_battery()
        local_ip = socket.gethostbyname(socket.gethostname())

        self.console.configure(state="normal")
        self.console.delete("1.0", "end")
        
        log = (
            f" [SYSTEM_INFO]\n"
            f" OS     : {get_windows_version()}\n"
            f" UPTIME : {str(datetime.now() - self.boot_time).split('.')[0]}\n"
            f" IP_LOC : {local_ip}\n\n"
            
            f" [NETWORK_IO]\n"
            f" ↓ {down_speed:.1f} KB/s  ↑ {up_speed:.1f} KB/s\n"
            f" SESSION: {session_down:.1f}MB IN / {session_up:.1f}MB OUT\n\n"
            
            f" [STORAGE_METRICS]\n"
            f" DRIVE C: {disk.percent}% Used\n"
            f" FREE   : {disk.free/(1024**3):.1f} GB Remaining\n\n"
            
            f" [POWER_STATUS]\n"
            f" SOURCE : {'BATTERY ('+str(batt.percent)+'%)' if batt else 'A/C STATIC'}\n"
            f" STATE  : {'CHARGING' if (batt and batt.power_plugged) else 'CONNECTED'}\n\n"
            
            f" [TOP_PRIORITY_TASKS]\n"
            f" {'NAME':<18} | {'CPU %':>6}\n"
            f" {'-'*27}\n"
        )
        
        try:
            procs = []
            for p in psutil.process_iter(['name', 'cpu_percent']):
                # Filter noise
                if p.info['name'] not in ['Idle', 'System Idle Process', 'System Interrupts', 'interrupts']:
                    # NORMALIZE: Divide by number of logical cores so total never exceeds 100%
                    normalized_cpu = p.info['cpu_percent'] / self.cpu_count
                    procs.append({'name': p.info['name'], 'cpu': normalized_cpu})
            
            top = sorted(procs, key=lambda x: x['cpu'], reverse=True)[:5]
            for p in top:
                name = (p['name'][:18] + '..') if len(p['name']) > 18 else p['name']
                log += f" > {name:<18} {p['cpu']:>6.1f}%\n"
        except:
            log += " > Access Restricted\n"

        self.console.insert("1.0", log)
        self.console.configure(state="disabled")

        self.after(1000, self.update_stats)

if __name__ == "__main__":
    app = CommandHUD()
    app.mainloop()