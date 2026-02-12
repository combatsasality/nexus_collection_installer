# Nexus Mods Collection Installer

A command-line tool that automatically downloads all mods from a **Nexus Mods collection** using Selenium and the Nexus Mods GraphQL API. Instead of manually clicking "Slow Download" on dozens of mods, this tool does it for you.

## How It Works

1. You provide a Nexus Mods **collection URL**.
2. The tool queries the Nexus Mods GraphQL API to retrieve the list of mods and files in the collection.
3. It launches an undetected Chrome browser, authenticates using your cookies, and automatically clicks the "Slow Download" button for every internal mod file.
4. External resources (non-Nexus links) are listed in the terminal for you to download manually.

## Requirements

- **Python 3.10+**
- **Google Chrome** (version 143 — must match the `version_main` set in `selenium_wrapper.py`)

## Installation

```bash
git clone https://github.com/combatsasality/nexus_collection_installer.git
cd nexus_collection_installer
pip install -r requirements.txt
```

## Setup — Obtaining Cookies

The tool requires your Nexus Mods session cookies to authenticate downloads. You need to export them from your browser:

1. Log in to [nexusmods.com](https://www.nexusmods.com) in your browser.
2. Open Developer Tools (`F12`) → **Application** tab → **Cookies** → `https://www.nexusmods.com`.
3. Create a `cookies.json` file in the project root with the following format:

You need cookies named `nexusmods_session` and `nexusmods_session_refresh`.

```json
[
  { "name": "cookie_name_1", "value": "cookie_value_1" },
  { "name": "cookie_name_2", "value": "cookie_value_2" }
]
```

> **Tip:** You can use a browser extension like [Cookie-Editor](https://cookie-editor.com/) to export cookies directly as JSON.

## Usage

```bash
python main.py
```

1. The program will prompt you to enter a Nexus Mods collection URL, e.g.:
   ```
   https://nexusmods.com/skyrimspecialedition/collections/abcdef
   ```
2. Chrome will open, load your cookies, and begin downloading each mod file automatically.
3. When the first mod starts downloading, you need allow the browser to always open Vortex (click "Always allow") so subsequent downloads are handled automatically.
4. Any external resources will be printed to the terminal for manual download.
5. Type `exit` to quit the program.

## Project Structure

| File                  | Description                                                               |
| --------------------- | ------------------------------------------------------------------------- |
| `main.py`             | Entry point — prompts for a collection URL and orchestrates the flow      |
| `nexus_graphql.py`    | Queries the Nexus Mods GraphQL API to resolve mod files from a collection |
| `selenium_wrapper.py` | Manages the Chrome browser, injects cookies, and automates downloads      |
| `cookies.json`        | Your Nexus Mods session cookies (not included — you must create this)     |
| `requirements.txt`    | Python dependencies                                                       |

## Notes

- Only the **slow download** option is used (no Nexus Mods Premium required).
- The first download takes ~5 seconds longer due to the initial download acceptance delay.
- Make sure your Chrome version matches the `version_main` parameter in `selenium_wrapper.py`. Update it if needed.
- The tool uses `undetected-chromedriver` to avoid bot detection.

## Disclaimer

This tool is intended for personal use to simplify downloading mod collections you have legitimate access to. Use responsibly and in accordance with the [Nexus Mods Terms of Service](https://www.nexusmods.com/about/termsofservice).

**⚠️ Use at your own risk.** Automating interactions with Nexus Mods may violate their Terms of Service and could result in your account being suspended or permanently banned. The author of this tool bears no responsibility for any consequences, including but not limited to account bans, IP blocks, or any other actions taken against you by Nexus Mods. By using this tool, you accept full responsibility for any risks involved.
