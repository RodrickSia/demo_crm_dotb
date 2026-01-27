import sys
from pathlib import Path

# Add frontend root to path to verify we can import from src
# In Streamlit, running `streamlit run frontend/pages/Users.py` adds that dir to path?
# Typically one runs `streamlit run frontend/main.py`
# We need to make sure `d:\CRM_DOTB\frontend` is in sys.path so `src` can be resolved
root_path = Path(__file__).resolve().parent.parent
if str(root_path) not in sys.path:
    sys.path.append(str(root_path))

from src.modules.users.view import render_users_page

if __name__ == "__main__":
    render_users_page()
