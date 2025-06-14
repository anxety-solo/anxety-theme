from modules.script_callbacks import on_ui_settings
from modules.shared import OptionInfo, opts, cmd_opts
from modules.scripts import basedir
from modules import launch_utils

from pathlib import Path
import gradio as gr
import shutil
import re
import os


# Check git-tag UI | need to define SD-UX
git_tag = launch_utils.git_tag()
# Check for SD-UX version format (vX.X.X-XX-gXXXXXXXX)
is_SD_UX = "-" in git_tag and git_tag[0] == "v" and git_tag.count("-") >= 2


section = ("ctp", "Anxety Theme")

# Default accent colors
accents = (
    "anxety",    # main
    "pink",
    "red",
    "peach",
    "yellow",
    "green",
    "blue"
)

script_path = Path(basedir())

# Colorful logging implementation
class Logger:
    @staticmethod
    def error(message: str):
        print(f"\033[31m[Anxety-Theme]: {message}\033[0m")

    @staticmethod
    def warning(message: str):
        print(f"\033[33m[Anxety-Theme]: {message}\033[0m")

    @staticmethod
    def info(message: str):
        print(f"\033[34m[Anxety-Theme]: {message}\033[0m")

logger = Logger()

def get_module_names():
    """Get list of available CSS modules from modules directory"""
    modules_dir = os.path.join(script_path, "modules")
    if os.path.exists(modules_dir):
        module_files = [f for f in os.listdir(modules_dir)
                       if f.endswith(".css") and os.path.isfile(os.path.join(modules_dir, f))]
        return [os.path.splitext(f)[0] for f in module_files]
    return []

def on_accent_change():
    """Update accent color in CSS file"""
    current_accent = getattr(opts, 'accent_color', 'anxety')
    with open(os.path.join(script_path, "style.css"), "r+") as file:
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

def apply_theme():
    """Main theme application logic"""
    # Handle command line argument
    if hasattr(cmd_opts, 'anxety') and cmd_opts.anxety:
        arg_color = cmd_opts.anxety.lower()
        if arg_color in accents:
            opts.accent_color = arg_color
            logger.info(f"Using command line accent color: {arg_color}")
        else:
            opts.accent_color = "anxety"
            logger.warning(f"Invalid color '{cmd_opts.anxety}'. Defaulting to 'anxety'.")
            logger.info(f"Available accent colors: {', '.join(accents)}")

    # Copy base CSS template
    if is_SD_UX:
        source_css = os.path.join(script_path, 'flavors/anxety-ux.css')
    elif gr.__version__ >= '4.40.0':
        source_css = os.path.join(script_path, 'flavors/anxety-gr4.css')
    else:
        source_css = os.path.join(script_path, 'flavors/anxety.css')

    shutil.copy(source_css, os.path.join(script_path, 'style.css'))

    # Apply accent color
    on_accent_change()

    # Append active modules
    modules_dir = os.path.join(script_path, "modules")
    active_modules = getattr(opts, "active_modules", [])

    with open(os.path.join(script_path, 'style.css'), 'a') as main_css:
        for module_name in active_modules:
            module_path = os.path.join(modules_dir, f"{module_name}.css")
            if os.path.isfile(module_path):
                main_css.write(f"\n\n/* Module: {module_name} */\n")
                with open(module_path, 'r') as mod_file:
                    main_css.write(mod_file.read())

def on_settings():
    """Create settings UI elements"""
    # Accent color selector
    opts.add_option(
        "accent_color",
        OptionInfo(
            default="anxety",
            label="Accent Color",
            component=gr.Radio,
            component_args={"choices": accents},
            onchange=on_accent_change,
            section=section,
            category_id="ui",
        ),
    )

    # Module selection
    module_names = get_module_names()
    opts.add_option(
        "active_modules",
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