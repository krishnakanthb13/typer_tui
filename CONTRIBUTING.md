# Contributing to Typer TUI

Thank you for your interest in contributing to Typer TUI! We welcome contributions from the community to make this the best terminal typing experience.

## Bug Reports

If you find a bug, please create an issue with the following details:
1.  **OS**: (Windows/Mac/Linux)
2.  **Terminal Emulator**: (cmd, powershell, wezterm, iterm2, etc.)
3.  **Steps to Reproduce**: Detailed sequence of actions.
4.  **Expected vs Actual Behavior**.

## Feature Suggestions

We love new ideas! Please open a discussion or issue tagged "Enhancement". Keep in mind our **Design Philosophy** (Simplicity, Keyboard-centricity) when proposing features.

## Development Workflow

1.  **Fork** the repository.
2.  **Clone** your fork locally.
3.  **Create a Branch** for your feature: `git checkout -b feature/amazing-mode`
4.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
5.  **Code & Test**: Run the app locally to verify changes.
6.  **Commit**: Use clear, descriptive commit messages.
7.  **Push** to your fork.
8.  **Open a Pull Request**.

## Local Setup

It is recommended to use a virtual environment:

```bash
# Windows
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Checklist Before Submitting

*   [ ] The code follows the existing style (clean, modular).
*   [ ] No new linter errors (flake8/pylint is recommended).
*   [ ] You have tested the changes manually in the TUI.
*   [ ] Documentation is updated if the feature changes user interaction.

## License
By contributing, you agree that your contributions will be licensed under the project's **GPL v3 License**.
