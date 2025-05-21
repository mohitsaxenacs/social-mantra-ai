"""Main entry point for the Social Mantra AI application."""
import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = str(Path(__file__).parent.absolute())
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Now import and run the app
from app import main

if __name__ == "__main__":
    main()
