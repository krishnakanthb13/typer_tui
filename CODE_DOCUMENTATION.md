# Code Documentation

## 1. File & Folder Structure

```
├── .agent/             # Agent workflows and skills (System)
├── assets/             # Text files for typing modes (easy, medium, etc.)
├── tui/                # Core Application Logic
│   ├── __init__.py
│   ├── app.py          # Main Textual App & Screens
│   └── logger.py       # JSON-based result logging
├── history.json        # Persistent storage for test results
├── main.py             # Application Entry Point
├── run.bat             # Windows Launcher
├── run.sh              # Unix/Mac Launcher
├── requirements.txt    # Python dependencies
└── LICENSE             # GPL v3 License
```

## 2. High-Level Architecture

The application is built using the **Textual** framework for Python, which provides a TUI (Terminal User Interface). It follows a reactive, event-driven architecture.

*   **App (`TyperTUIApp`)**: The main container that manages screens.
*   **Screens**: distinct views (Menu, Typing, Results, History).
*   **Widgets**: Reusable UI components (StatsWidget, TypingArea).
*   **Data Persistence**: Simple JSON file storage for history.

## 3. Core Modules

| File | Class/Function | Description |
| :--- | :--- | :--- |
| `main.py` | `main()` | Entry point; instantiates and runs the app. |
| `tui/app.py` | `TyperTUIApp` | The main Textual App class. |
| `tui/app.py` | `MenuScreen` | The landing screen for mode selection. |
| `tui/app.py` | `TypingScreen` | The core test environment. Handles input & timing. |
| `tui/app.py` | `ResultsScreen` | Displays WPM/Accuracy after a test. |
| `tui/app.py` | `HistoryScreen` | Displays past performance from JSON. |
| `tui/logger.py` | `Logger` | Handles reading/writing to `history.json`. |

## 4. Data Flow

1.  **Selection**: User selects Mode + Time in `MenuScreen`.
2.  **Initialization**: `TypingScreen` is pushed with selected config. Source text is loaded from `assets/`.
3.  **Interaction**: User types. `TypingArea` updates colors (Green/Red). `StatsWidget` updates WPM/Time.
4.  **Completion**: On time up or text finish, `ResultsScreen` is pushed.
5.  **Logging**: `ResultsScreen.on_mount` calls `Logger` to save stats to `history.json`.
6.  **Review**: User can view `HistoryScreen` which reads `history.json`.

## 5. Dependencies

*   **Runtime**:
    *   `textual`: The TUI framework.
    *   `rich`: For advanced text formatting (color, style).
*   **Dev**:
    *   Standard Python styling/linting tools (not strictly enforced in code but implied).

## 6. Execution Flow

`run.bat` / `run.sh` -> Check Env -> `python main.py` -> `TyperTUIApp` -> `MenuScreen`
