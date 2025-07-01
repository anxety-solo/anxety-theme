<div align="center">
    <h2>Anxety Dark Theme for Stable Diffusion WebUI</h2>
    <h3>Gradio 3/4 Compatible • Modular CSS System</h3>
</div>


<img width="auto" height="auto" src="https://raw.githubusercontent.com/anxety-solo/anxety-theme/main/.images/A1111.png"/>
<img width="auto" height="auto" src="https://raw.githubusercontent.com/anxety-solo/anxety-theme/main/.images/SD-UX.png"/>


### 🛠 Installation
1. Open WebUI
2. Navigate to "Extensions" → "Install from URL"
3. Paste `https://github.com/anxety-solo/anxety-theme`
4. Install and reload WebUI
5. In Settings → "Anxety Theme" configure options
6. Apply settings and reload UI

### 🌟 Key Features
- **Modular CSS System** - Enable/disable components via modules
- **Automatic CSS Optimization** - Only active styles remain
- **Gradio 3/4 Compatibility**
- **Enhanced UI Elements**:
  - Fluent ToastError popup
  - Fluent DropDown menus
  - Custom TagComplete styling
  - Minimalist scrollbars
  - Adaptive layout improvements

### 🧩 How It Works
1. **Core System**:
   - Automatically detects Gradio version
   - Applies base theme from `flavors/` directory

2. **Modules Engine**:
   - Scans `modules/` directory for CSS files
   - All modules enabled by default
   - Toggle via checkboxes in settings
   - Styles merged into main `style.css`
   - Disabled modules are purged on reload

### 📦 Using Modules
- Add .css files with your custom styles
- Files will auto-appear in settings
- Toggle checkboxes to enable/disable
- Changes apply after UI reload
- Note: Module styles append to main CSS. Use specific selectors to avoid conflicts.

<div align="center"> <h6>🖌 Based on <a href="https://github.com/catppuccin/stable-diffusion-webui">Catppuccin Theme</a> 🖌</h6> </div>