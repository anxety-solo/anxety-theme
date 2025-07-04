from modules.script_callbacks import on_ui_settings
from modules.shared import OptionInfo, opts, cmd_opts
from modules.scripts import basedir
from modules import launch_utils

from pathlib import Path
import gradio as gr
import shutil
import re
import os

# --- CONSTANTS ---
section = ("ctp", "Anxety Theme")

ACCENTS = (
    "anxety",    # main
    "pink",
    "red",
    "peach",
    "yellow",
    "green",
    "blue"
)
SCRIPT_PATH = Path(basedir())
MODULES_DIR = SCRIPT_PATH / "modules"
STYLE_CSS = SCRIPT_PATH / "style.css"

# --- LOGGER ---
class Logger:
    @staticmethod
    def error(message: str):
        print(f"\033[31m[Anxety-Theme]:\033[0m {message}", flush=True)

    @staticmethod
    def warning(message: str):
        print(f"\033[33m[Anxety-Theme]:\033[0m {message}", flush=True)

    @staticmethod
    def info(message: str):
        print(f"\033[34m[Anxety-Theme]:\033[0m {message}", flush=True)

logger = Logger()

# --- UTILS ---
def get_module_names():
    """Return a list of available module names (CSS files) in the modules directory."""
    if MODULES_DIR.exists():
        return [f.stem for f in MODULES_DIR.glob("*.css") if f.is_file()]
    return []

def select_base_css():
    """Select and return the appropriate base CSS file path."""
    git_tag = launch_utils.git_tag()
    is_sd_ux = "-" in git_tag and git_tag[0] == "v" and git_tag.count("-") >= 2
    if is_sd_ux:
        return SCRIPT_PATH / 'flavors/anxety-ux.css'
    elif gr.__version__ >= '4.40.0':
        return SCRIPT_PATH / 'flavors/anxety-gr4.css'
    else:
        return SCRIPT_PATH / 'flavors/anxety.css'

def update_accent_in_css():
    """Update the accent color variable in the main CSS file."""
    current_accent = getattr(opts, 'at_accent_color', 'anxety')
    with open(STYLE_CSS, "r+") as file:
        pattern = re.compile(r"--ctp-accent:\s*(.*)")
        text = re.sub(
            pattern,
            f"--ctp-accent: var(--ctp-{current_accent});",
            file.read(),
            count=1,
        )
        file.seek(0)
        file.write(text)
        file.truncate()

def append_active_modules():
    """Append the CSS of all active modules to the main style file."""
    active_modules = getattr(opts, "at_active_modules", [])
    with open(STYLE_CSS, 'a') as main_css:
        for module_name in active_modules:
            module_path = MODULES_DIR / f"{module_name}.css"
            if module_path.is_file():
                main_css.write(f"\n\n/* Module: {module_name} */\n")
                with open(module_path, 'r') as mod_file:
                    main_css.write(mod_file.read())

def handle_cmd_accent():
    """Handle accent color selection from command line arguments."""
    if hasattr(cmd_opts, 'anxety') and cmd_opts.anxety:
        arg_color = cmd_opts.anxety.lower()
        if arg_color in ACCENTS:
            opts.at_accent_color = arg_color
            logger.info(f"Using command line accent color: {arg_color}")
        else:
            opts.at_accent_color = "anxety"
            logger.warning(f"Invalid color '{cmd_opts.anxety}'. Defaulting to 'anxety'.")
            logger.info(f"Available accent colors: {', '.join(ACCENTS)}")

def apply_theme():
    handle_cmd_accent()                        # Set accent color from command line if provided
    shutil.copy(select_base_css(), STYLE_CSS)  # Copy the selected base CSS file to the main style file
    update_accent_in_css()                     # Update the accent color variable in the CSS
    append_active_modules()                    # Append active module CSS to the main style file

def on_settings():
    """Create settings UI elements"""
    # Accent color selector
    opts.add_option(
        "at_accent_color",
        OptionInfo(
            default="anxety",
            label="Accent Color",
            component=gr.Radio,
            component_args={"choices": ACCENTS},
            onchange=update_accent_in_css,
            section=section,
            category_id="ui",
        ),
    )

    # Module selection
    module_names = get_module_names()
    opts.add_option(
        "at_active_modules",
        OptionInfo(
            default=module_names,
            label="Enabled Modules",
            component=gr.CheckboxGroup,
            component_args={"choices": module_names},
            onchange=apply_theme,
            section=section,
            category_id="ui",
        )
    )

    # Initial theme setup
    apply_theme()

on_ui_settings(on_settings)