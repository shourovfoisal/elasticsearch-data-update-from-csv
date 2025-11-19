import os
import sys
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
VENV_DIR = BASE_DIR / "venv"
DEPENDENCIES_FILE = BASE_DIR / "core" / "dependencies.txt"

def create_venv():
  if VENV_DIR.exists():
    print("Virtual environment already exists")
    return
  
  print("Creating virtual environment")
  
  try:
    subprocess.check_call([sys.executable, "-m", "venv", str(VENV_DIR)])
  except subprocess.CalledProcessError as e:
    print("Failed to create venv. Trying to install the python3-venv package.")
    if sys.platform.startswith("linux"):
      python_version = f"python{sys.version_info.major}.{sys.version_info.minor}-venv"
      print(f"Detected python version {python_version}")
      

def get_pip_executable():
  pip_executable_name = "pip.exe" if os.name == "nt" else "pip"
  return VENV_DIR / ("Scripts" if os.name == "nt" else "bin") / pip_executable_name

def install_dependencies():
  if DEPENDENCIES_FILE.exists():
    print("Installing dependencies")
    subprocess.check_call([str(get_pip_executable()), "install", "-r", str(DEPENDENCIES_FILE)])

# def restart_in_venv():
#     """Restart the script inside the venv Python if not already."""
#     venv_python_executable = VENV_DIR / ("Scripts" if os.name == "nt" else "bin") / (
#         "python.exe" if os.name == "nt" else "python"
#     )
#     venv_python_executable = venv_python_executable.resolve()

#     current_python = Path(sys.executable).resolve()

#     if current_python != venv_python_executable:
#         write_log("Restarting inside virtual environment", True)
#         script_path = Path(sys.argv[0]).resolve()
#         # Change working directory to script location
#         os.chdir(script_path.parent)
#         os.execv(str(venv_python_executable), [str(venv_python_executable), str(script_path)] + sys.argv[1:])


def main():
  create_venv()
  install_dependencies()

if __name__ == "__main__":
  main()