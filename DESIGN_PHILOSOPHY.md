# Design Philosophy

## 1. Problem Definition
Most typing speed tests are web-based. They require a browser, an internet connection, and often come bloated with ads, trackers, or distracting UI elements. For developers who live in the terminal, switching context to a browser just to warm up or test typing speed is friction.

## 2. Why Typer TUI?
**Typer TUI** brings the typing test to where developers are already productive: the terminal. It is designed to be:
*   **Offline-First**: Zero latency, no internet needed.
*   **Instant**: Launches in milliseconds.
*   **Immersive**: Uses the same environment as your code editors and shells.

## 3. Design Principles

### A. Keyboard Centricity
The UI is navigable entirely by keyboard.
*   **Arrows**: Move between options.
*   **Enter**: Select/Restart.
*   **Design Choice**: No mouse interaction is required (though Textual supports it), preserving the flow of a typing session.

### B. Visual Feedback, Not Distraction
The interface uses color semantically:
*   **Green**: Correct character.
*   **Red**: Incorrect character.
*   **Dim White**: Future text.
animations are minimal to prevent eye strain during high-focus tasks.

### C. "Zero Config" Start
The application ships with sensible defaults (Medium difficulty, 30s) so a user can launch and start typing within 2 seconds.

## 4. Target Audience
*   **Developers**: Who want a quick warmup before a coding session.
*   **Sysadmins**: Who need to test keyboard latency/response in remote terminals over SSH.
*   **Minimalists**: Who prefer TUI over GUI/Web.

## 5. Trade-offs
*   **Simplicity vs. Features**: We deliberately exclude complex "typing lessons" or "courses". This is a *test* and *practice* tool, not a *teaching* tool.
*   **TUI Limitations**: While modern TUIs are powerful, we are constrained by the terminal grid. We embrace this by using clean, block-based layouts.
