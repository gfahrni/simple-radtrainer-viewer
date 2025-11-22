# === main.py ===
# Entry point of the RadTrainer application
# This file initializes the app, loads the KV files (UI layouts),
# and manages the screen transitions between MainScreen and DicomScreen.

import os  # import the os module to work with filesystem paths
from kivy.app import App  # import the base App class from Kivy
from kivy.lang import Builder  # import Builder to load .kv layout files
from kivy.uix.screenmanager import ScreenManager, NoTransition  # manage multiple screens

from config import DATA_FOLDER  # import the dataset folder path defined in config.py
from screens.main_screen import MainScreen  # import the main screen (dataset selection)
from screens.dicom_screen import DicomScreen  # import the DICOM viewer screen


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
    DATA_FOLDER = DATA_FOLDER  # store the dataset folder path for access across screens
    selected_file = ""  # store the path of the dataset folder selected by the user

    @property
    def selected_file_name(self):
        """
        Returns the name of the selected dataset folder (not the full path).

        This is used in KV files to display the selected dataset in the UI.
        """
        # os.path.basename extracts the last part of the path (folder name)
        return os.path.basename(self.selected_file) if self.selected_file else ""

    # -------------------------------
    #   BUILD THE APPLICATION UI
    # -------------------------------
    def build(self):
        """
        Kivy calls this method automatically to build the app UI.

        Responsibilities:
        - Load KV files
        - Create a ScreenManager
        - Add MainScreen and DicomScreen
        - Return the root widget (ScreenManager)
        """

        # Load the main screen layout from KV
        Builder.load_file("screens/main_screen.kv")
        # Load the DICOM screen layout from KV
        Builder.load_file("screens/dicom_screen.kv")

        # Initialize selected_file to empty (no dataset selected initially)
        self.selected_file = ""

        # Create a ScreenManager to handle multiple screens
        # NoTransition disables animations between screens
        sm = ScreenManager(transition=NoTransition())

        # Add MainScreen to the ScreenManager
        sm.add_widget(MainScreen(name="main"))  # 'name' is used to switch screens
        # Add DicomScreen to the ScreenManager
        sm.add_widget(DicomScreen(name="dicom"))

        # Return the ScreenManager as the root widget of the app
        return sm


# -------------------------------
#   START THE APPLICATION
# -------------------------------
if __name__ == "__main__":
    # When this script is executed directly, create a RadTrainer instance and run it
    RadTrainer().run()  # run() starts the Kivy event loop
