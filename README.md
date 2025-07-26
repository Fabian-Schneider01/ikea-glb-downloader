# IKEA 3D Model Downloader

This Python script automatically downloads the 3D `.glb` models from IKEA product pages.

---

## Requirements

Playwright Python package

---

## Installation

1. Clone or download this repository.

2. Install required Python packages:

```bash
pip install -r requirements.txt
````

3. Install Playwright browser binaries:

```bash
python -m playwright install
```

---

## How to run the script

Open your terminal or command prompt and run:

```bash
python main.py <ikea_product_url>
```

Replace `<ikea_product_url>` with the full URL of the IKEA product page.

Example:

```bash
python main.py https://www.ikea.com/de/de/p/nissedal-spiegel-weiss-10320317/
```

The script will open the page, detect the 3D model URL, download the `.glb` file, and save it in the `models` directory.

---

## Output

The downloaded 3D model file will be saved inside a folder named `models` in the current directory.

---

## Troubleshooting

* Ensure the IKEA URL is correct and the product has a 3D model.
* Internet connection is required.
* If no model is found, try increasing the wait time inside the script.

---
