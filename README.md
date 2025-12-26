modlk 🔧

Hex-patch LK images to remove boot warnings ⚠️ and flash via fastboot 🚀 — optimized for MTK devices 📱.


---

Features ✨

Automatically patches lk.img to remove Orange/Red State boot warnings.

Saves the patched image as lkmod.img (or custom output).

Reboots device into bootloader and flashes patched image via fastboot.

Fully Windows-friendly, downloads platform-tools automatically if missing.

Especially useful for MTK devices 📱.


Installation 🛠️

1. Make sure you have Python 3 installed.


2. Clone this repository:



git clone https://github.com/yourusername/modlk.git
cd modlk

3. Optionally, add the folder to your PATH to run modlk from anywhere.



Usage 🚀

python modlk.py [src_image] [--output OUTPUT]

src_image (optional) - Source LK image (default: lk.img).

--output / -o (optional) - Output patched image name (default: lkmod.img).


Examples 💡

Patch default lk.img:

python modlk.py

Patch a custom LK image and set output name:

python modlk.py mylk.img --output mylkmod.img

Notes ⚠️

Requires a connected device with USB debugging enabled.

Automatically reboots your device into bootloader and flashes patched image.

Ensure adb/fastboot are working or let the script download platform-tools.

Use at your own risk. Make sure you have backups of original images.


License 📄

MIT License
