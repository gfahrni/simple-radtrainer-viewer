# === main.py ===
# Entry point of the RadTrainer application
# This file initializes the app, loads the KV files (UI layouts),
# and manages the screen transitions between MainScreen and DicomScreen.

import os
import sys
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, NoTransition

from config import DATA_FOLDER
from screens.main_screen import MainScreen
from screens.dicom_screen import DicomScreen


def resource_path(relative_path):
    """
    Return absolute path to resource, works for dev and PyInstaller.
    """
    try:
        # PyInstaller creates a temporary folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # Development mode, use current folder
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class RadTrainer(App):
    """
    Main application class for RadTrainer.

    Responsibilities:
    - Load KV layout files
    - Initialize shared application state (selected dataset, data folder)
    - Create the screen manager and add screens
    """
    # -------------------------------
    #   SHARED APPLICATION STATE
    # -------------------------------
    DATA_FOLDER = DATA_FOLDER
    selected_file = ""

    @property
    def selected_file_name(self):
        """
        Returns the name of the selected dataset folder (not the full path).
        """
        return os.path.basename(self.selected_file) if self.selected_file else ""

    # -------------------------------
    #   BUILD THE APPLICATION UI
    # -------------------------------
    def build(self):
        """
        Kivy calls this method automatically to build the app UI.
        """
        # Load KV files with resource_path (dev + PyInstaller compatible)
        Builder.load_file(resource_path("screens/main_screen.kv"))
        Builder.load_file(resource_path("screens/dicom_screen.kv"))

        # Initialize selected_file to empty
        self.selected_file = ""

        # Create ScreenManager
        sm = ScreenManager(transition=NoTransition())
        sm.add_widget(MainScreen(name="main"))
        sm.add_widget(DicomScreen(name="dicom"))

        return sm


# -------------------------------
#   START THE APPLICATION
# -------------------------------
if __name__ == "__main__":
    RadTrainer().run()
