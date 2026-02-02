from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Button, Label, DataTable
from textual.containers import Container, Horizontal, Vertical
from textual.reactive import reactive
from textual.screen import Screen
from textual import events
from rich.text import Text
import time
import random
import os
from .logger import Logger

# --- Utils ---
def _resolve_asset_path(filename):
    """Resolve the path to an asset file, checking multiple locations."""
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(base_path, "..", "assets", filename)
    
    if not os.path.exists(path):
        path = os.path.join("assets", filename)
        
    return path if os.path.exists(path) else None

def load_words_from_file(filename):
    try:
        path = _resolve_asset_path(filename)
        if not path:
            return ["error", "loading", filename]

        with open(path, "r", encoding="utf-8") as f:
            content = f.read().strip()
            words = content.replace("\n", " ").split()
            return words
    except Exception as e:
        return ["error", "loading", str(e)]

def load_lines_from_file(filename):
    try:
        path = _resolve_asset_path(filename)
        if not path:
            return []

        with open(path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
            return lines
    except Exception:
        return []

def calculate_stats(start_time, total_chars, correct_chars):
    if start_time == 0:
        return 0, 0, 0
    
    elapsed = time.time() - start_time
    if elapsed <= 0:
        return 0, 0, 0
    
    minutes = elapsed / 60
    raw_wpm = (total_chars / 5) / minutes
    wpm = (correct_chars / 5) / minutes
    accuracy = (correct_chars / total_chars * 100) if total_chars > 0 else 100
    
    return wpm, accuracy, raw_wpm

# --- Widgets ---

class TypingArea(Static):
    """Widget to display typed text with coloring."""
    
    def render_content(self, target_text: str, user_input: str):
        display = Text()
        
        for i, char in enumerate(target_text):
            if i < len(user_input):
                if user_input[i] == char:
                    display.append(char, style="green")
                else:
                    if char == " ":
                        display.append("_", style="bold red")
                    else:
                        display.append(char, style="red")
            elif i == len(user_input):
                display.append(char, style="reverse bold white")
            else:
                display.append(char, style="dim white")
                
        self.update(display)

class StatsWidget(Static):
    wpm = reactive(0.0)
    time_left = reactive(0)
    
    def render(self):
        return f"WPM: {self.wpm:.0f} | Time: {self.time_left}s"

# --- Screens ---

class HistoryScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Back")]
    
    def on_mount(self):
        table = self.query_one(DataTable)
        table.add_columns("Date", "Mode", "Duration", "WPM", "Acc %", "Raw WPM")
        
        logger = Logger()
        history = logger.get_history()
        
        # Sort by date desc
        history.reverse()
        
        for entry in history:
            # Format timestamp
            ts = entry.get("timestamp", "")
            try:
                dt = ts.split("T")[0] + " " + ts.split("T")[1][:5]
            except (IndexError, ValueError):
                dt = ts
                
            table.add_row(
                dt,
                entry.get("mode", "?"),
                str(entry.get("duration", "?")),
                str(entry.get("wpm", 0)),
                str(entry.get("accuracy", 0)),
                str(entry.get("raw_wpm", 0))
            )

    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            Label("Past Results", classes="heading"),
            DataTable(),
            Button("Back (Esc)", variant="primary", id="back_btn"),
            id="history_container"
        )
        yield Footer()
        
    def on_button_pressed(self, event: Button.Pressed):
        self.app.pop_screen()

class MenuScreen(Screen):
    """Main Menu to select mode and settings."""
    BINDINGS = [("q", "quit", "Quit")]

    def compose(self) -> ComposeResult:
        # NOTE: If you update the layout of buttons here, you MUST update 
        # the 'rows' list in 'handle_arrow_navigation' to match the new grid structure.
        yield Header()
        yield Container(
            Label("Typer TUI", id="title"),
            Label("Difficulty:", classes="section_title"),
            Horizontal(
                Button("Easy", id="btn_easy", classes="mode_btn"),
                Button("Medium", id="btn_medium", classes="mode_btn"),
                Button("Hard", id="btn_hard", classes="mode_btn"),
                classes="btn_row"
            ),
            Label("Special:", classes="section_title"),
            Horizontal(
                Button("Numbers", id="btn_numbers", classes="mode_btn"),
                Button("Symbols", id="btn_symbols", classes="mode_btn"),
                Button("Twisters", id="btn_twisters", classes="mode_btn"),
                classes="btn_row"
            ),
            Label("Creative:", classes="section_title"),
            Horizontal(
                Button("Quotes", id="btn_quotes", classes="mode_btn"),
                Button("Stories", id="btn_stories", classes="mode_btn"),
                Button("Zen", id="btn_zen", classes="mode_btn"),
                classes="btn_row"
            ),
            Label("Developer:", classes="section_title"),
            Horizontal(
                Button("Code", id="btn_code", classes="mode_btn"),
                Button("Python", id="btn_python", classes="mode_btn"),
                Button("Terminal", id="btn_terminal", classes="mode_btn"),
                classes="btn_row"
            ),
            Label("Duration:", classes="section_title"),
            Horizontal(
                Button("15s", id="time_15", classes="time_btn"),
                Button("30s", id="time_30", classes="time_btn"),
                Button("60s", id="time_60", classes="time_btn"),
                Button("120s", id="time_120", classes="time_btn"),
                classes="btn_row"
            ),
            Horizontal(
                Button("View History", id="btn_history", variant="success"),
                Button("Start Test", id="btn_start", variant="primary"),
                classes="action_row"
            ),
            id="menu_container"
        )
        yield Footer()
    def on_mount(self):
        # Set defaults
        self.selected_mode = "medium.txt"
        self.selected_mode_name = "Medium"
        self.selected_time = 30
        
        # Highlight defaults
        self.query_one("#btn_medium").add_class("selected")
        self.query_one("#time_30").add_class("selected")

    def on_button_pressed(self, event: Button.Pressed):
        btn_id = event.button.id
        
        if btn_id == "btn_start":
            self.app.push_screen(TypingScreen(
                mode_file=self.selected_mode,
                mode_name=self.selected_mode_name,
                duration=self.selected_time
            ))
        
        elif btn_id == "btn_history":
            self.app.push_screen(HistoryScreen())
            
        elif btn_id.startswith("btn_"):
            # Mode selection
            self.query(".mode_btn").remove_class("selected")
            event.button.add_class("selected")
            
            modes = {
                "btn_easy": ("easy.txt", "Easy"),
                "btn_medium": ("medium.txt", "Medium"),
                "btn_hard": ("hard.txt", "Hard"),
                "btn_numbers": ("numbers.txt", "Numbers"),
                "btn_symbols": ("symbols.txt", "Symbols"),
                "btn_twisters": ("twisters.txt", "Twisters"),
                "btn_quotes": ("quotes.txt", "Quotes"),
                "btn_stories": ("stories.txt", "Stories"),
                "btn_zen": ("zen.txt", "Zen"),
                "btn_code": ("code_words.txt", "Code"),
                "btn_python": ("python.txt", "Python"),
                "btn_terminal": ("terminal.txt", "Terminal")
            }
            if btn_id in modes:
                self.selected_mode, self.selected_mode_name = modes[btn_id]
                
        elif btn_id.startswith("time_"):
            # Time selection
            self.query(".time_btn").remove_class("selected")
            event.button.add_class("selected")
            self.selected_time = int(btn_id.split("_")[1])

    def on_key(self, event: events.Key):
        if event.key in ["down", "up", "left", "right"]:
            self.handle_arrow_navigation(event.key)
            
    def handle_arrow_navigation(self, key):
        focused = self.app.focused
        if not focused:
            return

        # Define Rows - Must match compose() layout
        rows = [
            ["btn_easy", "btn_medium", "btn_hard"],        # Row 0: Difficulty
            ["btn_numbers", "btn_symbols", "btn_twisters"], # Row 1: Special
            ["btn_quotes", "btn_stories", "btn_zen"],       # Row 2: Creative
            ["btn_code", "btn_python", "btn_terminal"],     # Row 3: Developer
            ["time_15", "time_30", "time_60", "time_120"], # Row 4: Duration
            ["btn_history", "btn_start"]                   # Row 5: Actions
        ]
        
        # Find current position
        current_row, current_col = -1, -1
        for r_idx, row in enumerate(rows):
            if focused.id in row:
                current_row = r_idx
                current_col = row.index(focused.id)
                break
        
        if current_row == -1:
            return

        # Calculate new position
        if key == "right":
            if current_col < len(rows[current_row]) - 1:
                next_id = rows[current_row][current_col + 1]
                self.query_one(f"#{next_id}").focus()
                 
        elif key == "left":
            if current_col > 0:
                next_id = rows[current_row][current_col - 1]
                self.query_one(f"#{next_id}").focus()
                
        elif key == "down":
            if current_row < len(rows) - 1:
                next_row = rows[current_row + 1]
                next_col = min(current_col, len(next_row) - 1)
                
                # Special mapping for Duration -> Actions transition
                if current_row == 4:  # Duration row (4 items) to Actions (2 items)
                    if current_col <= 1: next_col = 0  # 15s/30s -> History
                    else: next_col = 1                  # 60s/120s -> Start
                
                next_id = next_row[next_col]
                self.query_one(f"#{next_id}").focus()
                
        elif key == "up":
            if current_row > 0:
                next_row = rows[current_row - 1]
                
                # Special mapping for Actions -> Duration transition
                if current_row == 5:  # Actions (2 items) to Duration (4 items)
                    if current_col == 0: next_col = 0  # History -> 15s
                    else: next_col = 3                  # Start -> 120s
                else:
                    next_col = min(current_col, len(next_row) - 1)
                    
                next_id = next_row[next_col]
                self.query_one(f"#{next_id}").focus()

class ResultsScreen(Screen):
    BINDINGS = [
        ("enter", "restart", "Restart"),
        ("m", "menu", "Menu"),
        ("escape", "menu", "Menu") # Escape goes to menu
    ]
    
    def __init__(self, wpm, accuracy, raw_wpm, mode_name, duration, **kwargs):
        super().__init__(**kwargs)
        self.wpm = wpm
        self.accuracy = accuracy
        self.raw_wpm = raw_wpm
        self.mode_name = mode_name
        self.duration = duration

    def compose(self) -> ComposeResult:
        yield Container(
            Label("Test Complete!", id="heading"),
            Horizontal(
                Vertical(
                    Label("WPM", classes="stat_title"),
                    Label(f"{self.wpm:.0f}", classes="stat_value"),
                    classes="stat_box"
                ),
                Vertical(
                    Label("Accuracy", classes="stat_title"),
                    Label(f"{self.accuracy:.0f}%", classes="stat_value"),
                    classes="stat_box"
                ),
                Vertical(
                    Label("Raw", classes="stat_title"),
                    Label(f"{self.raw_wpm:.0f}", classes="stat_value"),
                    classes="stat_box"
                ),
                id="stats_row"
            ),
            Horizontal(
                Button("Restart (Enter)", id="restart_btn", variant="primary"),
                Button("Menu (M)", id="menu_btn", variant="default"),
                classes="btn_row_center"
            ),
            id="results_box"
        )
    
    def on_mount(self):
        # Log results
        logger = Logger()
        logger.log_result(
            self.mode_name,
            self.duration,
            self.wpm,
            self.accuracy,
            self.raw_wpm
        )

    def on_key(self, event: events.Key):
        if event.key in ["left", "right"]:
            self.handle_arrow_navigation(event.key)
            
    def handle_arrow_navigation(self, key):
        focused = self.app.focused
        if not focused:
            # Default to Restart if nothing focused
            self.query_one("#restart_btn").focus()
            return

        if key == "right" and focused.id == "restart_btn":
             self.query_one("#menu_btn").focus()
        elif key == "left" and focused.id == "menu_btn":
             self.query_one("#restart_btn").focus()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "restart_btn":
            self.action_restart()
        elif event.button.id == "menu_btn":
            self.action_menu()
        
    def action_restart(self):
        # Pop results screen
        self.app.pop_screen()
        # The TypingScreen underneath needs to restart
        # We can't easily call methods on the screen below without a reference or query
        # But we pushed TypingScreen from MenuScreen.
        # Actually, if we pop, we are back at TypingScreen.
        # It's safer to rely on the App to handle "restart current TypingScreen"
        if isinstance(self.app.screen, TypingScreen):
            self.app.screen.restart_test()
            
    def action_menu(self):
        # Pop Results AND TypingScreen to go back to Menu
        # We need to pop twice? 
        # Stack: Menu -> Typing -> Results
        # Pop results -> Typing
        # Pop typing -> Menu
        self.app.pop_screen() 
        self.app.pop_screen()

class TypingScreen(Screen):
    BINDINGS = [
        ("ctrl+r", "restart_test", "Restart"),
        ("ctrl+w", "delete_word", "Delete Word"),
        ("escape", "back_to_menu", "Menu"),
    ]

    def __init__(self, mode_file="medium.txt", mode_name="Medium", duration=30, **kwargs):
        super().__init__(**kwargs)
        self.mode_file = mode_file
        self.mode_name = mode_name
        self.test_duration = duration
        
        self.target_text = ""
        self.user_input = ""
        self.start_time = 0
        self.test_running = False
        self.timer_handle = None

    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            Horizontal(
                Label(f"Mode: {self.mode_name}", classes="info_label"),
                StatsWidget(id="stats"),
                classes="top_bar"
            ),
            TypingArea(id="typing_area"),
            Label("Press any key to start...", id="instruction"),
            id="main_container"
        )
        yield Footer()

    def on_mount(self) -> None:
        self.restart_test()

    def action_back_to_menu(self):
        self.app.pop_screen()

    def restart_test(self) -> None:
        if self.timer_handle:
            self.timer_handle.stop()
            
        # Line-based modes (pick one random line/snippet)
        line_based_modes = [
            "sentences.txt", "stories.txt", "twisters.txt",
            "quotes.txt", "zen.txt", "python.txt", "terminal.txt"
        ]
        
        if self.mode_file in line_based_modes:
             words_or_lines = load_lines_from_file(self.mode_file)
             if not words_or_lines:
                 self.target_text = "Error loading content."
             else:
                 # Pick a random line/story
                 self.target_text = random.choice(words_or_lines).strip()
        else:
            all_words = load_words_from_file(self.mode_file)
            # Ensure we have enough words
            sample_size = min(100, len(all_words))
            if sample_size == 0:
                self.target_text = "Error loading words."
            else:
                self.target_text = " ".join(random.sample(all_words, sample_size))
            
        self.user_input = ""
        self.start_time = 0
        self.test_running = False
        
        self.query_one("#stats").time_left = self.test_duration
        self.query_one("#stats").wpm = 0
        self.query_one("#instruction").update("Start typing to begin...")
        self.query_one("#stats").update(f"WPM: 0 | Time: {self.test_duration}s")
        
        self.query_one(TypingArea).render_content(self.target_text, "")
        self.set_focus(None)

    def on_key(self, event: events.Key) -> None:
        if event.key == "ctrl+r":
            self.restart_test()
            return
            
        if event.key == "escape":
            self.action_back_to_menu()
            return

        # Start timer
        if not self.test_running and ((event.character and event.character.isprintable()) or event.key == "space"):
            self.start_test()

        if event.key == "backspace":
            if len(self.user_input) > 0:
                self.user_input = self.user_input[:-1]
                
        elif event.key == "ctrl+w" or event.key == "ctrl+h":
            if not self.user_input:
                return

            if self.user_input.endswith(" "):
                 self.user_input = self.user_input[:-1]
            else:
                last_space = self.user_input.rfind(" ")
                if last_space == -1:
                    self.user_input = ""
                else:
                    self.user_input = self.user_input[:last_space+1]

        elif event.character:
             if len(self.user_input) < len(self.target_text):
                 self.user_input += event.character

        self.query_one(TypingArea).render_content(self.target_text, self.user_input)
        
        if len(self.user_input) >= len(self.target_text):
            self.finish_test()

    def start_test(self):
        self.test_running = True
        self.start_time = time.time()
        self.timer_handle = self.set_interval(0.1, self.update_timer)
        self.query_one("#instruction").update("Go!")
        
    def update_timer(self):
        elapsed = time.time() - self.start_time
        remaining = self.test_duration - elapsed
        
        wpm, _, _ = self.calculate_current_stats()
        self.query_one("#stats").wpm = wpm
        self.query_one("#stats").time_left = int(remaining)
        self.query_one("#stats").update(f"WPM: {wpm:.0f} | Time: {int(remaining)}s")

        if remaining <= 0:
            self.finish_test()

    def finish_test(self):
        if self.timer_handle:
            self.timer_handle.stop()
        self.test_running = False
        
        wpm, accuracy, raw_wpm = self.calculate_current_stats()
        self.app.push_screen(ResultsScreen(
            wpm=wpm, 
            accuracy=accuracy, 
            raw_wpm=raw_wpm,
            mode_name=self.mode_name,
            duration=self.test_duration
        ))

    def calculate_current_stats(self):
        correct_chars = 0
        for i, char in enumerate(self.user_input):
            if i < len(self.target_text) and char == self.target_text[i]:
                correct_chars += 1
        return calculate_stats(self.start_time, len(self.user_input), correct_chars)

class TyperTUIApp(App):
    CSS_PATH = "typer_tui.css"
    
    def on_mount(self) -> None:
        self.push_screen(MenuScreen())
