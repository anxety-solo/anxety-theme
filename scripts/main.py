from modules.script_callbacks import on_ui_settings
from modules.shared import OptionInfo, opts
from modules.scripts import basedir

from pathlib import Path
import gradio as gr
import shutil
import re
import os

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

def get_module_names():
    """Get the list of modules from the modules folder"""
    modules_dir = os.path.join(script_path, "modules")
    if os.path.exists(modules_dir):
        module_files = [f for f in os.listdir(modules_dir) 
                       if f.endswith(".css") and os.path.isfile(os.path.join(modules_dir, f))]
        return [os.path.splitext(f)[0] for f in module_files]
    return []

def on_accent_change():
    """Updating the accent color in CSS"""
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
    """The main function of applying the topic"""
    # Copy the basic CSS
    if gr.__version__ >= '4.40.0':
        source_css = os.path.join(script_path, 'flavors/anxety-gr4.css')
    else: 
        source_css = os.path.join(script_path, 'flavors/anxety.css')
    shutil.copy(source_css, os.path.join(script_path, 'style.css'))

    # Applying the accent
    on_accent_change()

    # Add active modules
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
    """Interface settings"""
    # Set the accent color
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

    # Customizing the modules
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

    # Initial setup
    apply_theme()

on_ui_settings(on_settings)