import re
import time
import threading
from pynput import keyboard, mouse
from pynput.keyboard import Key
from PySide6.QtCore import QObject, Signal


class ActionRecorder(QObject):
    recording_finished = Signal(list)

    def __init__(self):
        super().__init__()
        self.actions = []
        self.keystroke_buffer = []
        self.recording = False
        self.last_key_time = time.time()
        self.lock = threading.Lock()
        self.active_modifiers = set()
        self.shell_context = None
        self.last_program_run = {"program": None, "timestamp": 0}

    def start(self):
        self.recording = True
        self.start_time = time.time()
        self.last_key_time = self.start_time

        self.keyboard_listener = keyboard.Listener(
            on_press=self._on_key_press,
            on_release=self._on_key_release
        )
        self.mouse_listener = mouse.Listener(
            on_click=self._on_mouse_click
        )

        self.keyboard_listener.start()
        self.mouse_listener.start()

    def stop(self):
        with self.lock:
            self.recording = False

        if hasattr(self, "keyboard_listener"):
            self.keyboard_listener.stop()
        if hasattr(self, "mouse_listener"):
            self.mouse_listener.stop()

        self._flush_keystrokes()
        cleaned = self._postprocess_actions(self.actions)
        self.recording_finished.emit(cleaned)

    def _on_key_press(self, key):
        if not self.recording:
            return

        now = time.time()
        if now - self.last_key_time > 1.2:
            self._flush_keystrokes()
        self.last_key_time = now

        if key in {Key.alt, Key.ctrl, Key.shift, Key.cmd}:
            self.active_modifiers.add(key)
            return

        if hasattr(key, "char") and key.char == "r" and Key.cmd in self.active_modifiers:
            self.keystroke_buffer.clear()
            return

        if Key.alt in self.active_modifiers and key == Key.f4:
            self._flush_keystrokes()
            self._add_action("hotkey", hotkey="ALT F4")
            return

        if key == Key.enter:
            self._flush_keystrokes()
            return

        if key == Key.backspace:
            if self.keystroke_buffer:
                self.keystroke_buffer.pop()
            return

        try:
            char = key.char if hasattr(key, 'char') and key.char else str(key)
        except Exception:
            char = str(key)

        self.keystroke_buffer.append(char)

    def _on_key_release(self, key):
        self.active_modifiers.discard(key)

    def _on_mouse_click(self, x, y, button, pressed):
        if self.recording and pressed:
            self._flush_keystrokes()
            self.actions.append({
                "type": "mouse_click",
                "position": (x, y),
                "timestamp": time.time()
            })

    def _flush_keystrokes(self):
        if not self.keystroke_buffer:
            return

        raw_seq = ''.join(self.keystroke_buffer).strip()
        self.keystroke_buffer.clear()

        if not raw_seq or raw_seq.lower() == "enter":
            return

        now = time.time()

        cleaned = (
            raw_seq.replace("Key.space", " ")
                .replace("`", "")
                .replace("'", "")
        )
        cleaned = re.sub(r"Key\.[a-zA-Z0-9_]+", "", cleaned)
        cleaned = re.sub(r"[_-][rl]", "", cleaned)
        cleaned = cleaned.strip()
        seq_lower = cleaned.lower()

        if not cleaned:
            return
        
        if re.match(r"^[a-z]{0,2}powershell(\.exe)?$", seq_lower):
            if self.shell_context == "powershell" and now - self.last_program_run.get("timestamp", 0) < 3:
                return
            self._add_action("run_program", program="powershell.exe", timestamp=now)
            self.shell_context = "powershell"
            self.last_program_run = {"program": "powershell", "timestamp": now}
            return

        if re.match(r"^[a-z]{0,2}cmd(\.exe)?$", seq_lower):
            if self.shell_context == "cmd" and now - self.last_program_run.get("timestamp", 0) < 3:
                return
            self._add_action("run_program", program="cmd.exe", timestamp=now)
            self.shell_context = "cmd"
            self.last_program_run = {"program": "cmd", "timestamp": now}
            return

        if self.shell_context and self._is_cli_command(seq_lower):
            self._add_action("cli_command", command=cleaned, shell=self.shell_context, timestamp=now)
            if seq_lower == "exit":
                self.shell_context = None
            return

        self._add_action("keystroke_sequence", sequence=cleaned, timestamp=now)



    def _recent_shell_launched(self, shell_name, now, window=5):
        for act in reversed(self.actions):
            if act["type"] == "run_program" and shell_name in act["program"].lower():
                return now - act["timestamp"] < window
        return False

    def _is_cli_command(self, cmd):
        return (
            cmd.startswith("echo")
            or any(cmd.startswith(prefix) for prefix in [
                "whoami", "ipconfig", "net user", "tasklist", "ping",
                "dir", "cd", "type", "exit"
            ])
        )

    def _add_action(self, type_, **kwargs):
        action = {"type": type_, "timestamp": time.time()}
        action.update(kwargs)
        self.actions.append(action)

    def _postprocess_actions(self, actions):
        cleaned = []
        for act in actions:
            if act["type"] == "keystroke_sequence":
                seq = act["sequence"].strip().lower()
                if seq == "enter":
                    continue
                if seq == ".f4":
                    cleaned.append({
                        "type": "hotkey",
                        "hotkey": "ALT F4",
                        "timestamp": act["timestamp"]
                    })
                    continue
            cleaned.append(act)
        return cleaned