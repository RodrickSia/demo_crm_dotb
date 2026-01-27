import sys
from pathlib import Path

# Add frontend root to path
root_path = Path(__file__).resolve().parent.parent
if str(root_path) not in sys.path:
    sys.path.append(str(root_path))

from src.modules.profile.view import render_profile_page

if __name__ == "__main__":
    render_profile_page()
