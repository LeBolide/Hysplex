# Hysplex - Sim racing startup manager
# Copyright (C) 2026 Hysplex
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

import json
import os
import subprocess
import sys
import threading
import time
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk


APP_TITLE = "H Y S P L E X"
APP_VERSION = "version 1.0.0"
SCRIPT_DIR = Path(sys.executable).resolve().parent if getattr(sys, "frozen", False) else Path(__file__).resolve().parent
CONFIG_FILE = SCRIPT_DIR / "hysplex_apps.json"
STARTUP_SCRIPT_NAME = "Hysplex Startup.cmd"
APP_LAUNCH_DELAY_SECONDS = 1
APP_READY_TIMEOUT_SECONDS = 30
APP_READY_POLL_SECONDS = 0.5
CREATE_NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)

VR_CLIENT_PRESETS = {
    "SteamVR": {
        "path": r"C:\Program Files (x86)\Steam\steam.exe",
        "args": ["-applaunch", "250820"],
    },
    "Meta Quest Link": {
        "path": r"C:\Program Files\Oculus\Support\oculus-client\Client.exe",
        "args": [],
    },
    "Virtual Desktop Streamer": {
        "path": r"C:\Program Files\Virtual Desktop Streamer\VirtualDesktop.Streamer.exe",
        "args": [],
    },
    "Windows Mixed Reality": {
        "path": "explorer.exe",
        "args": ["shell:AppsFolder\\Microsoft.WindowsMixedRealityPortal_8wekyb3d8bbwe!App"],
    },
    "Pimax Play": {
        "path": r"C:\Program Files\Pimax\PimaxClient\PimaxClient.exe",
        "args": [],
    },
    "Custom": {
        "path": "",
        "args": [],
    },
}

UI_THEMES = {
    "Graphite": {
        "bg": "#1f2226",
        "sidebar_bg": "#24282d",
        "card_bg": "#2c3036",
        "card_border": "#3a4047",
        "text": "#e2e0dc",
        "muted": "#a7adb4",
        "accent": "#8fa7b3",
        "accent_dark": "#657f8d",
        "danger": "#8f5f5a",
        "danger_active": "#a56f69",
        "secondary": "#383e45",
        "secondary_active": "#424a52",
        "input_bg": "#23272c",
        "button_text": "#101417",
        "disabled_bg": "#494e55",
        "icon_bg": "#1f2226",
        "icon_shadow": "#15181b",
        "icon_glow": "#657f8d",
        "icon_body": "#2c3036",
        "icon_accent": "#8fa7b3",
        "icon_lens": "#bcc9cf",
        "icon_highlight": "#f1eee7",
        "icon_sparkle": "#c7b89d",
    },
    "Fire": {
        "bg": "#202126",
        "sidebar_bg": "#2d2f35",
        "card_bg": "#35373d",
        "card_border": "#505258",
        "text": "#d8d8d8",
        "muted": "#a8abb2",
        "accent": "#ff5a1f",
        "accent_dark": "#c93a1a",
        "danger": "#b82418",
        "danger_active": "#d33122",
        "secondary": "#44474e",
        "secondary_active": "#484b52",
        "input_bg": "#24262b",
        "button_text": "#1b0d07",
        "disabled_bg": "#4a4c52",
        "icon_bg": "#202126",
        "icon_shadow": "#7a2112",
        "icon_glow": "#c93a1a",
        "icon_body": "#24262b",
        "icon_accent": "#ff5a1f",
        "icon_lens": "#ff8a4a",
        "icon_highlight": "#ffd0b8",
        "icon_sparkle": "#c93a1a",
    },
    "Ice": {
        "bg": "#202126",
        "sidebar_bg": "#2d2f35",
        "card_bg": "#35373d",
        "card_border": "#505258",
        "text": "#d8e7eb",
        "muted": "#a8b8bd",
        "accent": "#7ce3f2",
        "accent_dark": "#128ea5",
        "danger": "#0f6b80",
        "danger_active": "#1594ad",
        "secondary": "#44474e",
        "secondary_active": "#484b52",
        "input_bg": "#24262b",
        "button_text": "#062229",
        "disabled_bg": "#4a4c52",
        "icon_bg": "#202126",
        "icon_shadow": "#0a5d72",
        "icon_glow": "#128ea5",
        "icon_body": "#24262b",
        "icon_accent": "#7ce3f2",
        "icon_lens": "#b9f4fb",
        "icon_highlight": "#effcff",
        "icon_sparkle": "#d9fbff",
    },
    "Acid": {
        "bg": "#202126",
        "sidebar_bg": "#2d2f35",
        "card_bg": "#35373d",
        "card_border": "#505258",
        "text": "#dde8dc",
        "muted": "#aab6aa",
        "accent": "#78ff1f",
        "accent_dark": "#1fbf3a",
        "danger": "#2f8f18",
        "danger_active": "#43c722",
        "secondary": "#44474e",
        "secondary_active": "#484b52",
        "input_bg": "#24262b",
        "button_text": "#102006",
        "disabled_bg": "#4a4c52",
        "icon_bg": "#202126",
        "icon_shadow": "#1b5d16",
        "icon_glow": "#1fbf3a",
        "icon_body": "#24262b",
        "icon_accent": "#78ff1f",
        "icon_lens": "#a8ff4a",
        "icon_highlight": "#eaffc8",
        "icon_sparkle": "#b6ff00",
    },
}


def get_theme(name: str | None = None) -> dict:
    theme_name = name or str(config.get("ui_theme", DEFAULT_CONFIG["ui_theme"]))
    return UI_THEMES.get(theme_name, UI_THEMES["Graphite"])


DEFAULT_CONFIG = {
    "vr_mode_on": {
        "kill_processes": [
            "OneDrive.exe",
            "Teams.exe",
            "Discord.exe",
            "Spotify.exe",
            "msedge.exe",
            "chrome.exe",
            "firefox.exe",
        ],
        "stop_services": ["SysMain", "WSearch", "DiagTrack", "Print Spooler"],
        "power_plan": "SCHEME_MIN",
        "launch_linked_apps_sequentially": True,
    },
    "vr_client": {
        "name": "SteamVR",
        "path": VR_CLIENT_PRESETS["SteamVR"]["path"],
        "args": VR_CLIENT_PRESETS["SteamVR"]["args"],
        "launch_on_start": True,
    },
    "vr_mode_off": {
        "steamvr_shutdown_wait_seconds": 20,
        "close_linked_apps": True,
        "kill_processes": [
            "vrmonitor.exe",
            "vrserver.exe",
            "vrdashboard.exe",
            "vrcompositor.exe",
            "vrwebhelper.exe",
            "steamtours.exe",
        ],
        "start_services": ["SysMain", "WSearch", "DiagTrack", "Print Spooler"],
        "power_plan": "SCHEME_BALANCED",
    },
    "linked_apps": [],
    "start_with_windows": False,
    "ui_theme": "Graphite",
}

root: tk.Tk
on_button: tk.Button
off_button: tk.Button
add_app_button: tk.Button
remove_app_button: tk.Button
browse_vr_client_button: tk.Button
export_config_button: tk.Button
import_config_button: tk.Button
ui_theme_button: tk.Button
ui_theme_menu: tk.Menu
app_listbox: tk.Listbox
summary_linked_apps_label: tk.Label
summary_vr_client_label: tk.Label
status_label: tk.Label
nav_buttons: dict[str, tk.Widget] = {}
vr_client_name_var: tk.StringVar
vr_client_path_var: tk.StringVar
vr_client_args_var: tk.StringVar
launch_vr_client_var: tk.BooleanVar
start_with_windows_var: tk.BooleanVar
config: dict = {}
linked_apps: list[str] = []
launched_linked_app_processes: list[tuple[str, subprocess.Popen]] = []
pending_window_geometry: str | None = None


def refresh_sidebar_nav() -> None:
    """Redraw sidebar buttons from the current saved theme."""
    if "root" not in globals():
        return

    selected_page = getattr(root, "current_page_name", "dashboard")
    for nav_name, button in nav_buttons.items():
        if isinstance(button, SidebarNavItem):
            button.set_selected(nav_name == selected_page)


def schedule_sidebar_nav_refresh() -> None:
    """Refresh after Tk button press/release/hover repaints have completed."""
    if "root" not in globals():
        return

    refresh_sidebar_nav()
    root.after_idle(refresh_sidebar_nav)
    root.after(25, refresh_sidebar_nav)
    root.after(100, refresh_sidebar_nav)


def center_window(window: tk.Tk, width: int, height: int) -> None:
    """Place the window in the center of the current primary monitor."""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = max(0, (screen_width - width) // 2)
    y = max(0, (screen_height - height) // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")


class SidebarNavItem(tk.Canvas):
    """Sidebar navigation item that redraws from get_theme() instead of storing colors."""

    def __init__(self, parent, text: str, command) -> None:
        super().__init__(parent, height=44, highlightthickness=0, bd=0, cursor="hand2")
        self.nav_text = text
        self.command = command
        self.selected = False
        self.font = ("Segoe UI", 10, "bold")
        self.bind("<Configure>", lambda _event: self.draw())
        self.bind("<Button-1>", self.on_click)
        self.draw()

    def set_selected(self, selected: bool) -> None:
        self.selected = selected
        self.draw()

    def draw(self) -> None:
        theme = get_theme()
        width = max(1, self.winfo_width())
        height = max(1, self.winfo_height())
        bg = theme["accent_dark"] if self.selected else theme["sidebar_bg"]
        fg = "white" if self.selected else theme["muted"]
        self.configure(bg=bg)
        self.delete("all")
        self.create_rectangle(0, 0, width, height, fill=bg, outline=bg)
        self.create_text(20, height // 2, text=self.nav_text, fill=fg, font=self.font, anchor="w")

    def on_click(self, _event) -> None:
        if self.command:
            self.command()


class RoundedButton(tk.Canvas):
    """Small rounded button drawn with Tkinter only, no external UI dependency."""

    def __init__(
        self,
        parent,
        text: str,
        command,
        bg_color: str,
        fg_color: str,
        active_bg: str,
        disabled_bg: str,
        width: int = 150,
        height: int = 42,
    ) -> None:
        super().__init__(parent, width=width, height=height, highlightthickness=0, bd=0, bg=parent.cget("bg"))
        self.button_text = text
        self.command = command
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.active_bg = active_bg
        self.disabled_bg = disabled_bg
        self.enabled = True
        self.hovered = False
        self.radius = 12
        self.font = ("Segoe UI", 11, "bold")

        self.bind("<Configure>", lambda _event: self.draw())
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)
        self.draw()

    def draw(self) -> None:
        self.delete("all")
        width = max(1, self.winfo_width())
        height = max(1, self.winfo_height())
        color = self.disabled_bg if not self.enabled else self.active_bg if self.hovered else self.bg_color
        radius = min(self.radius, width // 2, height // 2)

        self.create_rectangle(radius, 0, width - radius, height, fill=color, outline=color)
        self.create_rectangle(0, radius, width, height - radius, fill=color, outline=color)
        self.create_oval(0, 0, radius * 2, radius * 2, fill=color, outline=color)
        self.create_oval(width - radius * 2, 0, width, radius * 2, fill=color, outline=color)
        self.create_oval(0, height - radius * 2, radius * 2, height, fill=color, outline=color)
        self.create_oval(width - radius * 2, height - radius * 2, width, height, fill=color, outline=color)
        self.create_text(width // 2, height // 2, text=self.button_text, fill=self.fg_color, font=self.font)

    def on_enter(self, _event) -> None:
        if self.enabled:
            self.hovered = True
            self.draw()

    def on_leave(self, _event) -> None:
        self.hovered = False
        self.draw()

    def on_click(self, _event) -> None:
        if self.enabled and self.command:
            self.command()

    def configure(self, cnf=None, **kwargs):
        if "state" in kwargs:
            self.enabled = kwargs.pop("state") != tk.DISABLED
            self.draw()
        return super().configure(cnf or {}, **kwargs)

    config = configure


def relaunch_with_pythonw_if_needed() -> None:
    """When double-clicked as .py, switch to pythonw.exe so no console stays open."""
    if not sys.platform.startswith("win"):
        return

    current_exe = Path(sys.executable)
    if current_exe.name.lower() == "pythonw.exe":
        return

    pythonw_exe = current_exe.with_name("pythonw.exe")
    if not pythonw_exe.exists():
        return

    subprocess.Popen(
        [str(pythonw_exe), str(Path(__file__).resolve())],
        cwd=str(SCRIPT_DIR),
        creationflags=CREATE_NO_WINDOW,
    )
    sys.exit(0)


def create_vr_icon(theme: dict) -> tk.PhotoImage:
    """Create a small VR headset icon for the app window without extra files."""
    icon = tk.PhotoImage(width=64, height=64)
    icon.put(theme["icon_bg"], to=(0, 0, 64, 64))

    # Theme glow/shadow
    icon.put(theme["icon_shadow"], to=(10, 20, 54, 46))
    icon.put(theme["icon_glow"], to=(8, 18, 56, 44))

    # Headset body
    icon.put(theme["icon_body"], to=(12, 20, 52, 42))
    icon.put(theme["icon_accent"], to=(12, 18, 52, 22))
    icon.put(theme["icon_accent"], to=(12, 40, 52, 44))
    icon.put(theme["icon_accent"], to=(10, 22, 14, 40))
    icon.put(theme["icon_accent"], to=(50, 22, 54, 40))

    # Lenses
    icon.put(theme["icon_lens"], to=(18, 26, 29, 36))
    icon.put(theme["icon_lens"], to=(35, 26, 46, 36))
    icon.put(theme["icon_highlight"], to=(20, 27, 25, 30))
    icon.put(theme["icon_highlight"], to=(37, 27, 42, 30))

    # Strap and small VR sparkle
    icon.put(theme["icon_accent"], to=(28, 14, 36, 18))
    icon.put(theme["icon_sparkle"], to=(31, 49, 33, 57))
    icon.put(theme["icon_sparkle"], to=(27, 52, 37, 54))
    return icon


def run_hidden(command: list[str], check: bool = False) -> subprocess.CompletedProcess:
    """Run a Windows command without opening a console window."""
    return subprocess.run(
        command,
        cwd=str(SCRIPT_DIR),
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=CREATE_NO_WINDOW,
        check=check,
    )


def deep_merge(defaults: dict, loaded: dict) -> dict:
    """Merge a loaded JSON config over defaults, preserving new default keys."""
    merged = dict(defaults)
    for key, value in loaded.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def load_config() -> dict:
    if not CONFIG_FILE.exists():
        return deep_merge(DEFAULT_CONFIG, {})

    try:
        loaded = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return deep_merge(DEFAULT_CONFIG, {})

    if not isinstance(loaded, dict):
        return deep_merge(DEFAULT_CONFIG, {})

    merged = deep_merge(DEFAULT_CONFIG, loaded)
    apps = merged.get("linked_apps", [])
    merged["linked_apps"] = [str(app) for app in apps if isinstance(app, str) and app.strip()] if isinstance(apps, list) else []
    return merged


def save_config() -> None:
    CONFIG_FILE.write_text(json.dumps(config, indent=2), encoding="utf-8")


def sync_linked_apps_from_config() -> None:
    global linked_apps
    apps = config.get("linked_apps", [])
    linked_apps = [str(app) for app in apps if isinstance(app, str) and app.strip()] if isinstance(apps, list) else []
    config["linked_apps"] = linked_apps


def save_linked_apps() -> None:
    config["linked_apps"] = linked_apps
    save_config()


def get_config_list(section: str, key: str) -> list[str]:
    value = config.get(section, {}).get(key, [])
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if isinstance(item, str) and item.strip()]


def get_config_string(section: str, key: str, fallback: str = "") -> str:
    value = config.get(section, {}).get(key, fallback)
    return str(value) if isinstance(value, str) else fallback


def is_process_running(process_name: str) -> bool:
    result = subprocess.run(
        ["tasklist", "/fi", f"imagename eq {process_name}", "/nh"],
        cwd=str(SCRIPT_DIR),
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        creationflags=CREATE_NO_WINDOW,
        check=False,
    )
    output = result.stdout.decode(errors="ignore") if result.stdout else ""
    return process_name.lower() in output.lower()


def is_vr_runtime_running() -> bool:
    return any(is_process_running(process_name) for process_name in get_config_list("vr_mode_off", "kill_processes"))


def kill_process(process_name: str) -> None:
    # Ignore failures because the app may not be running.
    run_hidden(["taskkill", "/f", "/im", process_name])


def control_service(action: str, service_name: str) -> int:
    # Returns the code so we can report admin/permission issues without stopping everything.
    return run_hidden(["net", action, service_name]).returncode


def set_power_plan(plan: str) -> int:
    return run_hidden(["powercfg", "-setactive", plan]).returncode


def refresh_app_listbox() -> None:
    app_listbox.delete(0, tk.END)
    for app_path in linked_apps:
        app_listbox.insert(tk.END, app_path)


def refresh_profile_summary() -> None:
    if "summary_linked_apps_label" in globals():
        summary_linked_apps_label.config(text=f"Linked apps: {len(linked_apps)}")

    if "summary_vr_client_label" in globals():
        vr_client = config.get("vr_client", {}) if isinstance(config.get("vr_client", {}), dict) else {}
        summary_vr_client_label.config(text=f"Launch client: {str(vr_client.get('name', 'Custom'))}")


def set_status(message: str) -> None:
    if "status_label" in globals():
        status_label.config(text=message)


def add_linked_app() -> None:
    app_path = filedialog.askopenfilename(
        title="Choose a program to launch when pressing Start",
        filetypes=[
            ("Programs", "*.exe *.bat *.cmd *.lnk"),
            ("All files", "*.*"),
        ],
    )
    if not app_path:
        return

    normalized_path = str(Path(app_path))
    if normalized_path in linked_apps:
        messagebox.showinfo(APP_TITLE, "This program is already in the list.")
        return

    linked_apps.append(normalized_path)
    save_linked_apps()
    refresh_app_listbox()
    refresh_profile_summary()


def remove_selected_linked_app() -> None:
    selection = list(app_listbox.curselection())
    if not selection:
        messagebox.showinfo(APP_TITLE, "Select a program to remove first.")
        return

    for index in reversed(selection):
        del linked_apps[index]

    save_linked_apps()
    refresh_app_listbox()
    refresh_profile_summary()


def launch_program(path_text: str, args: list[str] | None = None) -> tuple[int, subprocess.Popen | None]:
    path_text = path_text.strip()
    if not path_text:
        return 2, None

    args = args or []
    path = Path(path_text)
    if path_text.lower() != "explorer.exe" and not path.exists():
        return 2, None

    cwd = str(path.parent) if path_text.lower() != "explorer.exe" else str(SCRIPT_DIR)
    process = subprocess.Popen(
        [path_text, *args],
        cwd=cwd,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=CREATE_NO_WINDOW,
    )
    return 0, process


def process_has_main_window(process_id: int) -> bool:
    """Return True when Windows reports a main window for this process."""
    powershell_command = (
        f"$p = Get-Process -Id {process_id} -ErrorAction SilentlyContinue; "
        "if ($p -and $p.MainWindowHandle -ne 0) { exit 0 }; exit 1"
    )
    return run_hidden([
        "powershell",
        "-NoProfile",
        "-ExecutionPolicy",
        "Bypass",
        "-Command",
        powershell_command,
    ]).returncode == 0


def wait_for_program_ready(process: subprocess.Popen | None) -> None:
    """Wait until the launched app has a main window, or continue after timeout."""
    if process is None:
        return

    deadline = time.monotonic() + APP_READY_TIMEOUT_SECONDS
    while time.monotonic() < deadline:
        # If the launcher process exits quickly, it may have handed off to a child
        # app. Do not block the whole launch sequence in that case.
        if process.poll() is not None:
            return
        if process_has_main_window(process.pid):
            return
        time.sleep(APP_READY_POLL_SECONDS)


def launch_linked_apps() -> list[str]:
    warnings: list[str] = []
    launch_sequentially = bool(config.get("vr_mode_on", {}).get("launch_linked_apps_sequentially", True))

    for app_path in linked_apps:
        result, process = launch_program(app_path)
        if result == 2:
            warnings.append(f"Linked program was not found: {app_path}")
            continue
        if result != 0:
            warnings.append(f"Could not launch linked program: {app_path}")
            continue
        if process is not None:
            launched_linked_app_processes.append((app_path, process))
        if launch_sequentially:
            wait_for_program_ready(process)

    return warnings


def launch_vr_client() -> int:
    vr_client = config.get("vr_client", {})
    if not isinstance(vr_client, dict):
        return 2

    path = str(vr_client.get("path", ""))
    args_value = vr_client.get("args", [])
    args = [str(arg) for arg in args_value if isinstance(arg, str)] if isinstance(args_value, list) else []
    result, _process = launch_program(path, args)
    return result


def close_launched_linked_apps() -> list[str]:
    warnings: list[str] = []
    closed_names: set[str] = set()

    # First close the exact process IDs launched during this app session.
    for app_path, process in list(launched_linked_app_processes):
        if process.poll() is not None:
            continue

        run_hidden(["taskkill", "/pid", str(process.pid)])
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            run_hidden(["taskkill", "/f", "/pid", str(process.pid)])

        closed_names.add(Path(app_path).name.lower())

    launched_linked_app_processes.clear()

    # Some launchers start a child process and then exit. Fall back to the configured
    # executable names so Stop can still clean up the linked apps.
    for app_path in linked_apps:
        process_name = Path(app_path).name
        if not process_name.lower().endswith(".exe") or process_name.lower() in closed_names:
            continue
        kill_process(process_name)

    return warnings


def request_clean_steamvr_shutdown() -> None:
    powershell_command = (
        "Get-Process vrmonitor -ErrorAction SilentlyContinue | "
        "ForEach-Object { if ($_.MainWindowHandle -ne 0) { [void]$_.CloseMainWindow() } }"
    )
    run_hidden([
        "powershell",
        "-NoProfile",
        "-ExecutionPolicy",
        "Bypass",
        "-Command",
        powershell_command,
    ])


def run_vr_mode_on() -> list[str]:
    warnings: list[str] = []

    for process_name in get_config_list("vr_mode_on", "kill_processes"):
        kill_process(process_name)

    for service_name in get_config_list("vr_mode_on", "stop_services"):
        if control_service("stop", service_name) not in (0, 2):
            warnings.append(f"Could not stop service: {service_name}")

    power_plan = get_config_string("vr_mode_on", "power_plan")
    if power_plan and set_power_plan(power_plan) != 0:
        warnings.append(f"Could not switch power plan: {power_plan}")

    vr_client = config.get("vr_client", {}) if isinstance(config.get("vr_client", {}), dict) else {}
    if bool(vr_client.get("launch_on_start", True)):
        vr_client_result = launch_vr_client()
        vr_client_name = str(vr_client.get("name", "VR client"))
        vr_client_path = str(vr_client.get("path", ""))
        if vr_client_result == 2:
            warnings.append(f"{vr_client_name} was not found at: {vr_client_path}")
        elif vr_client_result != 0:
            warnings.append(f"Could not launch {vr_client_name}.")

    warnings.extend(launch_linked_apps())

    return warnings


def run_vr_mode_off() -> list[str]:
    warnings: list[str] = []

    vr_runtime_was_running = is_vr_runtime_running()
    if vr_runtime_was_running:
        request_clean_steamvr_shutdown()

        # Give SteamVR time to send sleep/standby commands to base stations before
        # cleaning up remaining VR processes. This matches the earlier behavior
        # that worked reliably with base-station power management.
        wait_seconds = config.get("vr_mode_off", {}).get("steamvr_shutdown_wait_seconds", 20)
        try:
            time.sleep(max(0, int(wait_seconds)))
        except (TypeError, ValueError):
            time.sleep(20)

    if bool(config.get("vr_mode_off", {}).get("close_linked_apps", True)):
        warnings.extend(close_launched_linked_apps())

    if vr_runtime_was_running:
        for process_name in get_config_list("vr_mode_off", "kill_processes"):
            kill_process(process_name)

    for service_name in get_config_list("vr_mode_off", "start_services"):
        if control_service("start", service_name) not in (0, 2):
            warnings.append(f"Could not start service: {service_name}")

    power_plan = get_config_string("vr_mode_off", "power_plan")
    if power_plan and set_power_plan(power_plan) != 0:
        warnings.append(f"Could not restore power plan: {power_plan}")

    return warnings


def apply_vr_client_preset(*_args) -> None:
    name = vr_client_name_var.get()
    preset = VR_CLIENT_PRESETS.get(name)
    if not preset:
        return

    vr_client_path_var.set(preset["path"])
    vr_client_args_var.set(" ".join(preset["args"]))


def browse_vr_client_path() -> None:
    app_path = filedialog.askopenfilename(
        title="Choose VR client executable",
        filetypes=[
            ("Programs", "*.exe *.bat *.cmd *.lnk"),
            ("All files", "*.*"),
        ],
    )
    if app_path:
        vr_client_path_var.set(str(Path(app_path)))
        if vr_client_name_var.get() != "Custom":
            vr_client_name_var.set("Custom")


def save_vr_client_settings() -> None:
    path = vr_client_path_var.get().strip()
    args_text = vr_client_args_var.get().strip()
    config["vr_client"] = {
        "name": vr_client_name_var.get().strip() or "Custom",
        "path": path,
        "args": args_text.split() if args_text else [],
        "launch_on_start": launch_vr_client_var.get(),
    }
    save_config()
    refresh_profile_summary()


def set_config_list_item(section: str, key: str, item: str, enabled: bool) -> None:
    values = get_config_list(section, key)
    existing_lower = {value.lower() for value in values}

    if enabled and item.lower() not in existing_lower:
        values.append(item)
    elif not enabled:
        values = [value for value in values if value.lower() != item.lower()]

    config.setdefault(section, {})[key] = values
    save_config()


def save_start_power_plan_setting(enabled: bool) -> None:
    config.setdefault("vr_mode_on", {})["power_plan"] = "SCHEME_MIN" if enabled else ""
    save_config()


def save_restore_power_plan_setting(enabled: bool) -> None:
    config.setdefault("vr_mode_off", {})["power_plan"] = "SCHEME_BALANCED" if enabled else ""
    save_config()


def save_close_linked_apps_setting(enabled: bool) -> None:
    config.setdefault("vr_mode_off", {})["close_linked_apps"] = enabled
    save_config()


def save_launch_vr_client_setting() -> None:
    config.setdefault("vr_client", {})["launch_on_start"] = launch_vr_client_var.get()
    save_config()


def save_sequential_linked_apps_setting(enabled: bool) -> None:
    config.setdefault("vr_mode_on", {})["launch_linked_apps_sequentially"] = enabled
    save_config()


def get_startup_script_path() -> Path:
    appdata = os.environ.get("APPDATA")
    if not appdata:
        raise OSError("The APPDATA environment variable is not available.")
    return Path(appdata) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup" / STARTUP_SCRIPT_NAME


def quote_cmd_arg(value: str) -> str:
    return '"' + value.replace('"', '\\"') + '"'


def build_startup_command() -> str:
    if getattr(sys, "frozen", False):
        return f"start \"\" {quote_cmd_arg(str(Path(sys.executable).resolve()))}"

    current_exe = Path(sys.executable).resolve()
    pythonw_exe = current_exe.with_name("pythonw.exe")
    launcher_exe = pythonw_exe if pythonw_exe.exists() else current_exe
    return f"start \"\" {quote_cmd_arg(str(launcher_exe))} {quote_cmd_arg(str(Path(__file__).resolve()))}"


def enable_windows_startup() -> None:
    startup_script = get_startup_script_path()
    startup_script.parent.mkdir(parents=True, exist_ok=True)
    startup_script.write_text(
        "@echo off\r\n"
        "rem Auto-start Hysplex. Remove this file or disable the option in the app to undo.\r\n"
        f"{build_startup_command()}\r\n",
        encoding="utf-8",
    )


def disable_windows_startup() -> None:
    startup_script = get_startup_script_path()
    if startup_script.exists():
        startup_script.unlink()


def save_start_with_windows_setting() -> None:
    enabled = start_with_windows_var.get()

    try:
        if enabled:
            enable_windows_startup()
        else:
            disable_windows_startup()
    except OSError as exc:
        start_with_windows_var.set(not enabled)
        messagebox.showerror(APP_TITLE, f"Could not update Windows startup setting:\n{exc}")
        return

    config["start_with_windows"] = enabled
    save_config()


def refresh_settings_ui_from_config() -> None:
    sync_linked_apps_from_config()
    refresh_app_listbox()
    refresh_profile_summary()

    vr_client = config.get("vr_client", {}) if isinstance(config.get("vr_client", {}), dict) else {}
    vr_client_name_var.set(str(vr_client.get("name", "SteamVR")))
    vr_client_path_var.set(str(vr_client.get("path", VR_CLIENT_PRESETS["SteamVR"]["path"])))
    args_value = vr_client.get("args", VR_CLIENT_PRESETS["SteamVR"]["args"])
    vr_client_args_var.set(" ".join(str(arg) for arg in args_value) if isinstance(args_value, list) else "")
    launch_vr_client_var.set(bool(vr_client.get("launch_on_start", True)))

    start_with_windows_var.set(bool(config.get("start_with_windows", False)))


def export_config() -> None:
    export_path = filedialog.asksaveasfilename(
        title="Export Hysplex config",
        defaultextension=".json",
        filetypes=[("JSON config", "*.json"), ("All files", "*.*")],
        initialfile="hysplex_apps.json",
    )
    if not export_path:
        return

    try:
        Path(export_path).write_text(json.dumps(config, indent=2), encoding="utf-8")
    except OSError as exc:
        messagebox.showerror(APP_TITLE, f"Could not export config:\n{exc}")
        return

    messagebox.showinfo(APP_TITLE, "Config exported.")


def save_ui_theme_setting(theme_name: str) -> None:
    global pending_window_geometry

    if theme_name not in UI_THEMES:
        return

    old_theme_name = str(config.get("ui_theme", DEFAULT_CONFIG["ui_theme"]))
    if old_theme_name == theme_name:
        return

    config["ui_theme"] = theme_name
    save_config()

    # Rebuild the window instead of recoloring existing widgets. This prevents
    # Tk widgets from keeping stale active/pressed colors from earlier themes.
    pending_window_geometry = root.geometry()
    root.destroy()
    main()


def import_config() -> None:
    import_path = filedialog.askopenfilename(
        title="Import Hysplex config",
        filetypes=[("JSON config", "*.json"), ("All files", "*.*")],
    )
    if not import_path:
        return

    try:
        loaded = json.loads(Path(import_path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        messagebox.showerror(APP_TITLE, f"Could not read config:\n{exc}")
        return

    if not isinstance(loaded, dict):
        messagebox.showerror(APP_TITLE, "This file is not a valid Hysplex config.")
        return

    confirmed = messagebox.askyesno(APP_TITLE, "Import this config and replace the current launcher settings?")
    if not confirmed:
        return

    current_startup_setting = bool(config.get("start_with_windows", False))
    config.clear()
    config.update(deep_merge(DEFAULT_CONFIG, loaded))
    config["start_with_windows"] = current_startup_setting
    sync_linked_apps_from_config()
    save_config()
    refresh_settings_ui_from_config()
    messagebox.showinfo(APP_TITLE, "Config imported. The Windows startup setting was left unchanged.")


def run_task(action_name: str, task_function) -> None:
    """Run a VR task in the background and keep routine success feedback in the UI."""
    set_buttons_enabled(False)
    verb = "Starting" if action_name == "Start" else "Stopping"
    set_status(f"{verb} VR mode…")

    def worker() -> None:
        try:
            warnings = task_function()
            if warnings:
                message = f"{action_name} completed with warnings:\n\n" + "\n".join(warnings)
                root.after(0, lambda: set_status(f"{action_name} completed with warnings."))
                root.after(0, lambda: messagebox.showwarning(APP_TITLE, message))
            else:
                root.after(0, lambda: set_status(f"{action_name} complete."))
        except Exception as exc:
            error_message = f"Failed to run {action_name}:\n{exc}"
            root.after(0, lambda: set_status(f"{action_name} failed."))
            root.after(0, lambda: messagebox.showerror(APP_TITLE, error_message))
        finally:
            root.after(0, lambda: set_buttons_enabled(True))

    threading.Thread(target=worker, daemon=True).start()


def launch_vr_mode_on() -> None:
    run_task("Start", run_vr_mode_on)


def launch_vr_mode_off() -> None:
    run_task("Stop", run_vr_mode_off)


def set_buttons_enabled(enabled: bool) -> None:
    state = tk.NORMAL if enabled else tk.DISABLED
    on_button.config(state=state)
    off_button.config(state=state)
    add_app_button.config(state=state)
    remove_app_button.config(state=state)
    browse_vr_client_button.config(state=state)
    export_config_button.config(state=state)
    import_config_button.config(state=state)
    ui_theme_button.config(state=state)


def main() -> None:
    global root, on_button, off_button, add_app_button, remove_app_button, browse_vr_client_button, export_config_button, import_config_button, ui_theme_button, ui_theme_menu
    global app_listbox, summary_linked_apps_label, summary_vr_client_label, status_label, nav_buttons, linked_apps, config, vr_client_name_var, vr_client_path_var, vr_client_args_var, launch_vr_client_var, start_with_windows_var, pending_window_geometry

    root = tk.Tk()
    root.title(APP_TITLE)
    root.resizable(True, True)
    if pending_window_geometry:
        root.geometry(pending_window_geometry)
        pending_window_geometry = None
    else:
        center_window(root, 900, 744)
    root.minsize(820, 624)

    config = load_config()
    sync_linked_apps_from_config()
    save_config()

    theme = get_theme()
    root.vr_icon = create_vr_icon(theme)
    root.iconphoto(True, root.vr_icon)

    bg = theme["bg"]
    sidebar_bg = theme["sidebar_bg"]
    card_bg = theme["card_bg"]
    card_border = theme["card_border"]
    text = theme["text"]
    muted = theme["muted"]
    accent = theme["accent"]
    accent_dark = theme["accent_dark"]
    danger = theme["danger"]
    input_bg = theme["input_bg"]
    secondary = theme["secondary"]

    root.configure(bg=bg)
    style = ttk.Style(root)
    style.theme_use("clam")
    style.configure("TCombobox", fieldbackground=input_bg, background=card_bg, foreground=text, arrowcolor=accent)
    style.map(
        "TCombobox",
        fieldbackground=[("readonly", input_bg)],
        foreground=[("readonly", text)],
        background=[("readonly", card_bg)],
        selectbackground=[("readonly", input_bg)],
        selectforeground=[("readonly", text)],
    )
    root.option_add("*TCombobox*Listbox.background", input_bg)
    root.option_add("*TCombobox*Listbox.foreground", text)
    root.option_add("*TCombobox*Listbox.selectBackground", accent_dark)
    root.option_add("*TCombobox*Listbox.selectForeground", "white")

    def label(parent, label_text: str, **kwargs) -> tk.Label:
        return tk.Label(parent, text=label_text, bg=kwargs.pop("bg", card_bg), fg=kwargs.pop("fg", text), **kwargs)

    def card(parent, **kwargs) -> tk.Frame:
        outer = tk.Frame(parent, bg=card_border)
        inner = tk.Frame(outer, bg=card_bg, padx=18, pady=16, **kwargs)
        inner.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        return outer

    def styled_button(parent, button_text: str, command, bg_color: str = accent, fg_color: str = theme["button_text"]) -> RoundedButton:
        active_color = theme["danger_active"] if bg_color == danger else theme["secondary_active"] if bg_color == secondary else accent_dark
        return RoundedButton(
            parent,
            text=button_text,
            command=command,
            bg_color=bg_color,
            fg_color=fg_color,
            active_bg=active_color,
            disabled_bg=theme["disabled_bg"],
        )

    def dark_checkbutton(parent, button_text: str, variable: tk.BooleanVar, command) -> tk.Checkbutton:
        return tk.Checkbutton(
            parent,
            text=button_text,
            variable=variable,
            command=command,
            bg=card_bg,
            fg=text,
            activebackground=card_bg,
            activeforeground=text,
                selectcolor=input_bg,
            relief=tk.FLAT,
            bd=0,
            highlightthickness=0,
            font=("Segoe UI", 10),
        )

    shell = tk.Frame(root, bg=bg)
    shell.pack(fill=tk.BOTH, expand=True)

    sidebar = tk.Frame(shell, bg=sidebar_bg, width=210)
    sidebar.pack(side=tk.LEFT, fill=tk.Y)
    sidebar.pack_propagate(False)

    logo = tk.Frame(sidebar, bg=sidebar_bg, padx=18, pady=20)
    logo.pack(fill=tk.X)
    tk.Label(logo, text=APP_TITLE, bg=sidebar_bg, fg=text, font=("Segoe UI", 14, "bold"), anchor="w", wraplength=170).pack(fill=tk.X)
    tk.Label(logo, text=APP_VERSION, bg=sidebar_bg, fg=muted, font=("Segoe UI", 9), anchor="w").pack(fill=tk.X, pady=(4, 0))

    content = tk.Frame(shell, bg=bg, padx=28, pady=26)
    content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    top_bar = tk.Frame(content, bg=bg)
    top_bar.pack(fill=tk.X, pady=(0, 20))

    ui_theme_menu = tk.Menu(root, tearoff=False, bg=card_bg, fg=text, activebackground=accent_dark, activeforeground="white", bd=0)
    for theme_name in UI_THEMES:
        ui_theme_menu.add_command(label=theme_name, command=lambda selected_theme=theme_name: save_ui_theme_setting(selected_theme))

    def show_ui_theme_menu() -> None:
        x = ui_theme_button.winfo_rootx()
        y = ui_theme_button.winfo_rooty() + ui_theme_button.winfo_height()
        ui_theme_menu.tk_popup(x, y)
        ui_theme_menu.grab_release()

    action_card = card(top_bar)
    action_card.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 12))
    action_inner = action_card.winfo_children()[0]

    on_button = styled_button(action_inner, "START", launch_vr_mode_on, accent, theme["button_text"])
    on_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8))

    off_button = styled_button(action_inner, "STOP", launch_vr_mode_off, danger, "white")
    off_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(8, 0))

    ui_theme_button = tk.Button(
        top_bar,
        text="◐",
        command=show_ui_theme_menu,
        bg=card_bg,
        fg=text,
        activebackground=accent_dark,
        activeforeground="white",
        relief=tk.FLAT,
        bd=0,
        padx=10,
        pady=8,
        cursor="hand2",
        font=("Segoe UI", 13, "bold"),
        width=2,
    )
    ui_theme_button.pack(side=tk.RIGHT, anchor="n")

    page_container = tk.Frame(content, bg=bg)
    page_container.pack(fill=tk.BOTH, expand=True)

    pages: dict[str, tk.Frame] = {}
    nav_buttons = {}

    def show_page(name: str) -> None:
        root.current_page_name = name
        for page in pages.values():
            page.pack_forget()
        pages[name].pack(fill=tk.BOTH, expand=True)
        schedule_sidebar_nav_refresh()

    def nav_button(name: str, title: str) -> None:
        button = SidebarNavItem(sidebar, title, lambda page_name=name: show_page(page_name))
        button.pack(fill=tk.X, padx=10, pady=2)
        nav_buttons[name] = button

    controls_tab = tk.Frame(page_container, bg=bg)
    apps_tab = tk.Frame(page_container, bg=bg)
    vr_client_tab = tk.Frame(page_container, bg=bg)
    extra_tab = tk.Frame(page_container, bg=bg)
    pages["dashboard"] = controls_tab
    pages["apps"] = apps_tab
    pages["client"] = vr_client_tab
    pages["extra"] = extra_tab

    nav_button("dashboard", "Overview")
    nav_button("apps", "Apps")
    nav_button("client", "VR")
    nav_button("extra", "Actions")

    label(controls_tab, "Overview", bg=bg, font=("Segoe UI", 18, "bold"), anchor="w").pack(fill=tk.X, pady=(0, 14))

    status_card = card(controls_tab)
    status_card.pack(fill=tk.X, pady=(8, 0))
    status_inner = status_card.winfo_children()[0]
    label(status_inner, "Status", font=("Segoe UI", 12, "bold"), anchor="w").pack(fill=tk.X)
    status_label = label(status_inner, "Ready.", fg=muted, anchor="w")
    status_label.pack(fill=tk.X, pady=(6, 0))

    options_card = card(controls_tab)
    options_card.pack(fill=tk.X, pady=(18, 0))
    options_inner = options_card.winfo_children()[0]
    label(options_inner, "Start Options", font=("Segoe UI", 13, "bold"), anchor="w").pack(fill=tk.X, pady=(0, 8))

    launch_vr_client_var = tk.BooleanVar(value=bool(config.get("vr_client", {}).get("launch_on_start", True)))
    dark_checkbutton(options_inner, "Launch VR client when pressing Start", launch_vr_client_var, save_launch_vr_client_setting).pack(anchor="w", pady=3)

    sequential_linked_apps_var = tk.BooleanVar(value=bool(config.get("vr_mode_on", {}).get("launch_linked_apps_sequentially", True)))
    dark_checkbutton(
        options_inner,
        "Wait until each linked app opens before launching next",
        sequential_linked_apps_var,
        lambda: save_sequential_linked_apps_setting(sequential_linked_apps_var.get()),
    ).pack(anchor="w", pady=3)

    start_with_windows_var = tk.BooleanVar(value=bool(config.get("start_with_windows", False)))
    dark_checkbutton(options_inner, "Start with Windows", start_with_windows_var, save_start_with_windows_setting).pack(anchor="w", pady=3)

    summary_card = card(controls_tab)
    summary_card.pack(fill=tk.X, pady=(18, 0))
    summary_inner = summary_card.winfo_children()[0]
    vr_client = config.get("vr_client", {}) if isinstance(config.get("vr_client", {}), dict) else {}
    label(summary_inner, "Profile Summary", font=("Segoe UI", 13, "bold"), anchor="w").pack(fill=tk.X)
    summary_linked_apps_label = label(summary_inner, f"Linked apps: {len(linked_apps)}", fg=muted, anchor="w")
    summary_linked_apps_label.pack(fill=tk.X, pady=(8, 0))
    summary_vr_client_label = label(summary_inner, f"Launch client: {str(vr_client.get('name', 'Custom'))}", fg=muted, anchor="w")
    summary_vr_client_label.pack(fill=tk.X, pady=(4, 0))

    config_button_frame = tk.Frame(controls_tab, bg=bg)
    config_button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(16, 0))
    export_config_button = styled_button(config_button_frame, "Export Config", export_config, secondary, text)
    export_config_button.pack(side=tk.LEFT)
    import_config_button = styled_button(config_button_frame, "Import Config", import_config, secondary, text)
    import_config_button.pack(side=tk.LEFT, padx=(8, 0))

    label(apps_tab, "Linked Apps", bg=bg, font=("Segoe UI", 20, "bold"), anchor="w").pack(fill=tk.X)
    label(apps_tab, "Programs listed here launch automatically when you press Start.", bg=bg, fg=muted, font=("Segoe UI", 10), anchor="w").pack(fill=tk.X, pady=(2, 16))

    apps_card = card(apps_tab)
    apps_card.pack(fill=tk.BOTH, expand=True)
    apps_inner = apps_card.winfo_children()[0]

    list_frame = tk.Frame(apps_inner, bg=card_bg)
    list_frame.pack(fill=tk.BOTH, expand=True)

    app_listbox = tk.Listbox(
        list_frame,
        height=10,
        selectmode=tk.EXTENDED,
        bg=input_bg,
        fg=text,
        selectbackground=accent_dark,
        selectforeground="white",
        relief=tk.FLAT,
        bd=0,
        highlightthickness=1,
        highlightbackground=card_border,
        font=("Segoe UI", 10),
    )
    app_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(list_frame, orient=tk.VERTICAL, command=app_listbox.yview, bg=card_bg, troughcolor=input_bg)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    app_listbox.config(yscrollcommand=scrollbar.set)

    button_frame = tk.Frame(apps_inner, bg=card_bg)
    button_frame.pack(fill=tk.X, pady=(12, 0))

    add_app_button = styled_button(button_frame, "Add Program...", add_linked_app)
    add_app_button.pack(side=tk.LEFT)

    remove_app_button = styled_button(button_frame, "Remove Selected", remove_selected_linked_app, secondary, text)
    remove_app_button.pack(side=tk.LEFT, padx=(8, 0))

    vr_client = config.get("vr_client", {}) if isinstance(config.get("vr_client", {}), dict) else {}
    vr_client_name_var = tk.StringVar(value=str(vr_client.get("name", "SteamVR")))
    vr_client_path_var = tk.StringVar(value=str(vr_client.get("path", VR_CLIENT_PRESETS["SteamVR"]["path"])))
    args_value = vr_client.get("args", VR_CLIENT_PRESETS["SteamVR"]["args"])
    args_text = " ".join(str(arg) for arg in args_value) if isinstance(args_value, list) else ""
    vr_client_args_var = tk.StringVar(value=args_text)
    for vr_client_setting_var in (vr_client_name_var, vr_client_path_var, vr_client_args_var):
        vr_client_setting_var.trace_add("write", lambda *_args: save_vr_client_settings())

    label(vr_client_tab, "VR", bg=bg, font=("Segoe UI", 18, "bold"), anchor="w").pack(fill=tk.X)
    label(vr_client_tab, "Choose the VR software to launch.", bg=bg, fg=muted, font=("Segoe UI", 10), anchor="w").pack(fill=tk.X, pady=(2, 16))

    client_card = card(vr_client_tab)
    client_card.pack(fill=tk.X)
    client_inner = client_card.winfo_children()[0]

    form = tk.Frame(client_inner, bg=card_bg)
    form.pack(fill=tk.X)
    form.columnconfigure(1, weight=1)

    label(form, "Client:", anchor="w").grid(row=0, column=0, sticky="w", pady=6, padx=(0, 10))
    preset_box = ttk.Combobox(form, textvariable=vr_client_name_var, values=list(VR_CLIENT_PRESETS.keys()), state="readonly")
    preset_box.grid(row=0, column=1, sticky="ew", pady=6)
    preset_box.bind("<<ComboboxSelected>>", apply_vr_client_preset)

    label(form, "Path:", anchor="w").grid(row=1, column=0, sticky="w", pady=6, padx=(0, 10))
    tk.Entry(form, textvariable=vr_client_path_var, bg=input_bg, fg=text, insertbackground=text, relief=tk.FLAT).grid(row=1, column=1, sticky="ew", pady=6, ipady=5)
    browse_vr_client_button = styled_button(form, "Browse...", browse_vr_client_path, secondary, text)
    browse_vr_client_button.grid(row=1, column=2, sticky="e", padx=(8, 0), pady=6)

    show_advanced_var = tk.BooleanVar(value=False)
    args_label = label(form, "Arguments:", anchor="w")
    args_entry = tk.Entry(form, textvariable=vr_client_args_var, bg=input_bg, fg=text, insertbackground=text, relief=tk.FLAT)

    def toggle_advanced_launch_options() -> None:
        if show_advanced_var.get():
            args_label.grid(row=3, column=0, sticky="w", pady=6, padx=(0, 10))
            args_entry.grid(row=3, column=1, columnspan=2, sticky="ew", pady=6, ipady=5)
        else:
            args_label.grid_remove()
            args_entry.grid_remove()

    advanced_checkbox = dark_checkbutton(form, "Show advanced launch options", show_advanced_var, toggle_advanced_launch_options)
    advanced_checkbox.grid(row=2, column=1, columnspan=2, sticky="w", pady=(8, 2))
    toggle_advanced_launch_options()

    label(extra_tab, "Actions", bg=bg, font=("Segoe UI", 18, "bold"), anchor="w").pack(fill=tk.X)
    label(extra_tab, "Choose which Start and Stop actions the launcher should perform.", bg=bg, fg=muted, font=("Segoe UI", 10), anchor="w").pack(fill=tk.X, pady=(2, 18))

    extra_container = tk.Frame(extra_tab, bg=bg)
    extra_container.pack(fill=tk.BOTH, expand=True)

    start_extra_card = card(extra_container)
    start_extra_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 8))
    start_extra_inner = start_extra_card.winfo_children()[0]
    label(start_extra_inner, "Start actions", font=("Segoe UI", 13, "bold"), anchor="w").pack(fill=tk.X, pady=(0, 8))

    def extra_list_toggle(parent, text_value: str, section: str, key: str, item: str) -> None:
        item_var = tk.BooleanVar(value=item.lower() in {value.lower() for value in get_config_list(section, key)})
        dark_checkbutton(
            parent,
            text_value,
            item_var,
            lambda section_name=section, key_name=key, item_name=item, variable=item_var: set_config_list_item(section_name, key_name, item_name, variable.get()),
        ).pack(anchor="w", pady=4)

    for process_name in DEFAULT_CONFIG["vr_mode_on"]["kill_processes"]:
        extra_list_toggle(start_extra_inner, f"Close {process_name}", "vr_mode_on", "kill_processes", process_name)

    label(start_extra_inner, "Services", fg=muted, anchor="w").pack(fill=tk.X, pady=(10, 2))
    for service_name in DEFAULT_CONFIG["vr_mode_on"]["stop_services"]:
        extra_list_toggle(start_extra_inner, f"Stop {service_name}", "vr_mode_on", "stop_services", service_name)

    performance_power_var = tk.BooleanVar(value=bool(get_config_string("vr_mode_on", "power_plan")))
    dark_checkbutton(start_extra_inner, "Switch to high performance power plan", performance_power_var, lambda: save_start_power_plan_setting(performance_power_var.get())).pack(anchor="w", pady=(10, 2))

    stop_extra_card = card(extra_container)
    stop_extra_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(8, 0))
    stop_extra_inner = stop_extra_card.winfo_children()[0]
    label(stop_extra_inner, "Stop actions", font=("Segoe UI", 13, "bold"), anchor="w").pack(fill=tk.X, pady=(0, 8))

    close_linked_apps_var = tk.BooleanVar(value=bool(config.get("vr_mode_off", {}).get("close_linked_apps", True)))
    dark_checkbutton(stop_extra_inner, "Close linked apps launched by Start", close_linked_apps_var, lambda: save_close_linked_apps_setting(close_linked_apps_var.get())).pack(anchor="w", pady=2)

    for process_name in DEFAULT_CONFIG["vr_mode_off"]["kill_processes"]:
        extra_list_toggle(stop_extra_inner, f"Close {process_name}", "vr_mode_off", "kill_processes", process_name)

    label(stop_extra_inner, "Services", fg=muted, anchor="w").pack(fill=tk.X, pady=(10, 2))
    for service_name in DEFAULT_CONFIG["vr_mode_off"]["start_services"]:
        extra_list_toggle(stop_extra_inner, f"Start {service_name}", "vr_mode_off", "start_services", service_name)

    restore_power_var = tk.BooleanVar(value=bool(get_config_string("vr_mode_off", "power_plan")))
    dark_checkbutton(stop_extra_inner, "Restore balanced power plan", restore_power_var, lambda: save_restore_power_plan_setting(restore_power_var.get())).pack(anchor="w", pady=(10, 2))

    refresh_app_listbox()
    show_page("dashboard")

    root.mainloop()


if __name__ == "__main__":
    relaunch_with_pythonw_if_needed()
    main()
