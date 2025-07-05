# 🌐 OSI Model Visualization & Reference Tool

A sleek Python application built with Tkinter and Pillow, designed to help learners and professionals explore the OSI (Open Systems Interconnection) model layer-by-layer. This project combines educational content with dynamic animations and visual aesthetics.

## 🧠 Features

- 🖼️ **Tabbed Interface**: Each OSI layer has its own tab with descriptions and embedded visuals.
- 🎨 **Embedded Images**: Layer-specific PNG images scale dynamically for clean presentation.
- 📈 **Visualization Tab**: Animated packet flow through the seven OSI layers with clickable boxes and tooltips.
- 💡 **Interactive Tooltips**: Hover over any layer in the visualization to see debug info or live config advice.
- 🖱️ **Clickable Routing**: Click a layer box to jump directly to its detailed tab view.

## 📁 Project Structure
OSIModelApp/ ├── application.png ├── data_link.png ├── network.png ├── physical.png ├── presentation.png ├── session.png ├── transport.png ├── osi_model.py └── README.md


> 📸 Images should be named exactly as `{layer_name}.png` (lowercase, underscores) and placed in the same directory as your script.

## 🛠️ Technologies Used

- `Python 3.7+`
- `tkinter` — GUI framework
- `ttk.Notebook` — Tabbed layout
- `Pillow (PIL)` — Image handling and resizing
- `Canvas` — Custom packet animation
- `lambda bindings` — Tooltip and click events

## 🚀 Installation & Usage

1. **Install dependencies**:
   ```bash
   pip install pillow
   ```
2. **Ensure images exist for each OSI layer (.png format, named appropriately)**
    - Run the application:
   ```bash      
   python osi_model.py
   ```

## 🔍 OSI Layer Guide
Each tab features:- A themed icon or visual
- A plain-English summary of the layer's responsibilities
- Tips on configuration and troubleshooting techniques
  
The visualization tab displays:- A vertical layer stack
- Arrows indicating data flow
- A bouncing green packet to demonstrate live traversal
  
## 📜 License
This project is licensed under the MIT License.🙌 

## Credits 
Designed by Anuj James, combining technical insight with creative GUI design.
