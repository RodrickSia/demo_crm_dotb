import sys
from pathlib import Path

# Add frontend root to path
root_path = Path(__file__).resolve().parent
if str(root_path) not in sys.path:
    sys.path.append(str(root_path))

from src.main_view import render_main

if __name__ == "__main__":
    render_main()
