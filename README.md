# AIS Timer


<img src="assets/image.png" alt="Fluxa Logo" width="400"/>



AIS Timer is a Python script that tracks the time spent on different applications during a coding session. It provides a productivity analysis based on your activity log and your personal hobby.

## Features

- Tracks active applications and records the time spent on each.
- Analyzes productivity using OpenAI's ChatGPT based on your activity log.
- Displays an activity summary with total time spent on each application.

## Installation

### Prerequisites

- Python 3.x
- OpenAI Python library
- macOS (for the AppleScript integration)

### Steps to Install

1. Navigate to your home directory:

   ```bash
   cd ~
   ```

2. Clone the repository:

    ```bash
    git clone https://github.com/dykyivladk1/ai-timer.git
    ```

3. Open Zsh configuration file:

    ```bash
    nano ~/.zshrc
    ```

4. Add the following line to create an alias:

    ```bash
    alias ais='python3 ~/ai-timer/app.py'
    ```

5. Save the file and exit.

6. Apply the changes:

    ```bash
    source ~/.zshrc
    ```


### Usage

When first running the script, you will be asked for OpenAI API key, and for your hobby. Then to start tracking your activity, simply run:

    ```bash
    ais
    ```

To stop tracking, use `Ctrl + C`. The script will then analyze your activity and provide a summary.

