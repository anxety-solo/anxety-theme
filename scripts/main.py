from modules.script_callbacks import on_ui_settings
from modules.shared import OptionInfo, opts

import gradio as gr
import shutil
import re
import os

section = ("ctp", "Anxety-Theme")

# Default accent colors
accents: tuple[str] = (
    "anxety",    # main
    "rosewater",
    "flamingo",
    "pink",
    "mauve",
    "red",
    "maroon",
    "peach",
    "yellow",
    "green",
    "teal",
    "sky",
    "blue",
    "sapphire",
    "lavender",
)

script_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

def on_accent_change():
    # Replace the color
    with open(os.path.join(script_path, "style.css"), "r+") as file:
        pattern = re.compile(r"--ctp-accent:\s*(.*)")
        text = re.sub(
            pattern,
            f"--ctp-accent: var(--ctp-{opts.accent_color});",
            file.read(),
            count=1,
        )

        file.seek(0)
        file.write(text)
        file.truncate()

def apply_theme():
    # Move css over
    if gr.__version__ >= '4.40.0':
        source_css = os.path.join(script_path, f'flavors/gradio4/anxety.css')
    else: 
        source_css = os.path.join(script_path, f'flavors/anxety.css')

    # Copy the contents of the selected theme CSS to style.css
    shutil.copy(source_css, os.path.join(script_path, 'style.css'))

    # Reapply accent color
    on_accent_change()

def on_settings():
    opts.add_option(
        "accent_color",
        OptionInfo(
            default="anxety",
            label="Accent",
            component=gr.Radio,
            component_args={"choices": accents},
            onchange=on_accent_change,
            section=section,
            category_id="ui",
        ),
    )
    
    # Initial setup
    apply_theme()

on_ui_settings(on_settings)

# Print warning about potential display issues
if gr.__version__ >= '4.40.0':
    print(f"\033[32m[anxety-theme]\033[0m There may be display issues on Gradio 4 | \033[34mForge\033[0m")