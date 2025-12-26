import os
import subprocess
import urllib.request
import zipfile
import argparse

PLATFORM_TOOLS_URL = "https://dl.google.com/android/repository/platform-tools-latest-windows.zip"

def download_platform_tools():
    zip_path = "platform-tools-latest-windows.zip"
    if not os.path.exists(zip_path):
        print("Downloading latest platform-tools...")
        urllib.request.urlretrieve(PLATFORM_TOOLS_URL, zip_path)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(".")
    folders = [f for f in os.listdir(".") if os.path.isdir(f) and "platform-tools" in f]
    if not folders:
        raise RuntimeError("Failed to extract platform-tools")
    return os.path.abspath(folders[0])

def get_platform_tools_path():
    try:
        subprocess.run(["adb", "version"], capture_output=True, check=True)
        return ""
    except:
        return download_platform_tools()

def patch_lk_image(src_path, dst_path):
    warnings = [
        b"Orange State...Your device has been unlocked and can't be trusted...Your device will boot in 5 seconds...",
        b"Red State...Your device has failed verification and may not...Please download %s image with correct signature...or disable verified boot.....Your device will reboot in 5 seconds..."
    ]
    with open(src_path, "rb") as f:
        data = bytearray(f.read())
    for warning in warnings:
        idx = data.find(warning)
        if idx != -1:
            data[idx:idx+len(warning)] = b"\x00" * len(warning)
    with open(dst_path, "wb") as f:
        f.write(data)

def run_cmd(cmd, platform_tools_path=""):
    if platform_tools_path:
        cmd = os.path.join(platform_tools_path, cmd.split()[0]) + " " + " ".join(cmd.split()[1:])
    subprocess.run(cmd, shell=True, check=True)

def main():
    parser = argparse.ArgumentParser(description="Patch lk.img to remove boot warnings and flash via fastboot.")
    parser.add_argument("src_image", nargs="?", default="lk.img", help="Source LK image (default: lk.img)")
    parser.add_argument("--output", "-o", default="lkmod.img", help="Output patched image name (default: lkmod.img)")
    args = parser.parse_args()

    if not os.path.isfile(args.src_image):
        print(f"{args.src_image} not found in current directory")
        return

    platform_tools_path = get_platform_tools_path()
    patch_lk_image(args.src_image, args.output)
    print(f"Patched image saved as {args.output}")

    run_cmd("adb reboot bootloader", platform_tools_path)
    run_cmd(f"fastboot flash lk {args.output}", platform_tools_path)
    run_cmd("fastboot reboot", platform_tools_path)
    print("Done!")

if __name__ == "__main__":
    main()
  
