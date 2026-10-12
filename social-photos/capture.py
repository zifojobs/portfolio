import subprocess
import os
import time

# Chemin vers Chrome
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
DELAY = 5  # secondes pour que les polices se chargent

files = [
    {"html": "article1-instagram-post.html", "width": 1080, "height": 1080},
    {"html": "article1-linkedin-post.html", "width": 1200, "height": 627},
    {"html": "article1-whatsapp-status.html", "width": 1080, "height": 1920},
    {"html": "article2-instagram-post.html", "width": 1080, "height": 1080},
    {"html": "article2-linkedin-post.html", "width": 1200, "height": 627},
    {"html": "article2-whatsapp-status.html", "width": 1080, "height": 1920},
    {"html": "article3-instagram-post.html", "width": 1080, "height": 1080},
    {"html": "article3-whatsapp-status.html", "width": 1080, "height": 1920},
]

script_dir = os.path.dirname(os.path.abspath(__file__))

for file in files:
    html_path = os.path.join(script_dir, file["html"])
    output_path = os.path.join(script_dir, file["html"].replace(".html", ".png"))

    print(f"Processing {file['html']}...")

    cmd = [
        CHROME,
        "--headless",
        "--disable-gpu",
        "--no-sandbox",
        "--hide-scrollbars",
        f"--window-size={file['width']},{file['height']}",
        f"--virtual-time-budget={DELAY * 1000}",
        f"--screenshot={output_path}",
        f"file:///{html_path.replace(chr(92), chr(47))}"
    ]

    try:
        subprocess.run(cmd, check=True, capture_output=True)
        print(f"[OK] Created {os.path.basename(output_path)}")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Error processing {file['html']}: {e}")

print("\nAll screenshots captured successfully!")
