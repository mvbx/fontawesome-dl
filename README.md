# fontawesome-dl

`fontawesome-dl` is a command-line tool that allows you to download any FontAwesome icon (including Pro icons) for free. It fetches the latest version of an icon directly from FontAwesome's website, and all icon families and styles are supported.

## Features

- Download any FontAwesome icon (both free and Pro)
- Automatically fetches the icon from the latest FontAwesome version
- Supports all icon families: `classic`, `duotone`, `sharp`, `sharp-duotone`, and `brands`
- Supports all icon styles: `solid`, `regular`, `light`, and `thin`

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/mvbx/fontawesome-dl.git
    cd fontawesome-dl
    ```

2. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the script by providing the icon name, family, and style as arguments, or simply execute the script without any arguments to enter it interactively. The tool will then download the specified icon to the `output` directory, which will be created in the same location as the script.

```bash
python fontawesome-dl.py [icon_name] [icon_family] [icon_style]
```

**Example usage:** `python fontawesome-dl.py house sharp regular`