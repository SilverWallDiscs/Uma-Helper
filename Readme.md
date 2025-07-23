Here's a `README.md` file for your GitHub repository:

```markdown
# Umamusume Support Card Options Viewer

This application displays the possible options for Umamusume support cards by detecting the card name on screen using OCR (Optical Character Recognition).

## Features

- Automatically detects support card names in a specified screen region
- Displays all possible options for the detected card
- Lightweight and unobtrusive overlay interface
- Click anywhere to close the options window

## Requirements

- Python 3.7+
- Tesseract OCR installed (see installation instructions below)
- Required Python packages (listed in requirements.txt)

## Installation

1. Install Tesseract OCR:
   - **Windows**: Download installer from [UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki)
   - **Mac**: `brew install tesseract`
   - **Linux**: `sudo apt install tesseract-ocr` (Debian/Ubuntu)

2. Clone this repository:
   ```bash
   git clone https://github.com/SilverWallDiscs/Uma-Helper.git
   cd umamusume-support-options
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```bash
   python support_options.py
   ```

2. The application will monitor the top-left third of your screen for support card names.

3. When a card is detected, the possible options will appear in a transparent overlay window.

4. Click anywhere to close the options window.

## Configuration

You can modify the following in the code:
- `REGION` variable to change the screen area monitored
- `OPCIONES_CARTAS` dictionary to add/edit card options
- Appearance of the overlay window in the `crear_rectangulo_redondeado` method

## Troubleshooting

- If text isn't being detected properly:
  - Ensure Tesseract is installed correctly
  - Adjust the `REGION` coordinates to better capture the card name
  - Try different screen resolutions

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Uses pytesseract for OCR
- Uses PIL/Pillow for image processing
- Uses pynput for mouse event handling


This README provides clear installation instructions, usage guidelines, and troubleshooting tips for your project. You may want to customize the license and acknowledgments sections as needed.