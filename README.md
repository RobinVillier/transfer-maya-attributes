
# Transfer Maya Attrs

A Maya tool for transfering custom attributes with an efficient UI.

<img width="297" height="536" alt="image" src="https://github.com/user-attachments/assets/5f07d401-72f7-405d-99d3-33508ab34d1e" />

## Features

- Transfer any attributes from any Maya nodes to another (even locked and non keyable attributes).
- Ability to transfer all attributes by using a snippet of the code (featured below) or selecting the attributes you want to transfer by launching the tool's UI.
- You can also Import and Export your custom attributes templates (fingers attributes for example).
- User-friendly UI built with Qt.

## Project Structure

```
TransferAttrs/
├── data/             # Data saved by the user
├── config/           # Configuration and settings
├── config/           # Configuration and settings
├── maya_logic/       # Maya attribute operations
├── resources/        # Icons and stylesheets
├── ui/               # Qt-based user interface
```

## Installation

1. Place this folder in your Maya scripts directory.
2. Run the script from Maya's Script Editor or from one of your shelves.

## Usage

1. Launche the UI to select which attributes you want to transfer.
```python
from TransferAttrs.ui import main
main.launch()
```

2. If you want the ability described above, you can add a double click feature to your shelf button by following the TUTORIAL on my youtube channel and pasting this code:

```python
from TransferAttrs.maya_logic import attribute_tools as at
from TransferAttrs.maya_logic import get_maya_items as gmi

source_node = gmi.get_selected_node()
if source_node is None:
    cmds.error("No source item selected")

attrs_list = at.get_custom_non_hidden_attributes()
attrs_data_dict = at.get_attributes_data(attrs_list)
at.transfer_attributes(attrs_data_dict)
```

## Requirements

- Autodesk Maya (up to 2025, go to my [gumroad](https://redfoxx.gumroad.com/l/reorder-maya-attributes) for 2026 version and above).
- PySide2/PyQt5.

## Contact

For issues, questions, or contributions, reach out at [rvillier99@gmail.com](mailto:rvillier99@gmail.com).
