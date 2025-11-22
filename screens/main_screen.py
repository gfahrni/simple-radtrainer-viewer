# === screens/main_screen.py ===

import os  # work with folder paths
from kivy.uix.screenmanager import Screen  # base Screen class
from kivy.app import App  # access global app state
from kivy.uix.button import Button  # create dynamic buttons
from config import DATA_FOLDER  # root data folder


class MainScreen(Screen):
    """
    Main screen containing:
    - Left column: list of folders
    - Right column: datasets inside selected folder

    This version now supports a 2-level structure:
    DATA_FOLDER/
        ├── Folder_1/
        │       ├── Dataset_A/
        │       ├── Dataset_B/
        ├── Folder_2/
                ├── Dataset_C/
                ├── Dataset_D/
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_folder = None  # store selected folder (None until user clicks)

    def on_pre_enter(self):
        """
        Called each time we return to this screen.
        Refresh the folder list.
        If a folder was previously selected, reload its datasets.
        """
        self.load_folder_list()

        if self.current_folder:
            self.load_dataset_list(self.current_folder)
        else:
            # Clear dataset list if no folder selected yet
            self.ids.dataset_list.clear_widgets()

    # -------------------------------------------------------------------------
    #   FOLDER LIST (LEFT COLUMN)
    # -------------------------------------------------------------------------
    def load_folder_list(self):
        """Populate the folder list with subfolders inside DATA_FOLDER."""

        folder_list = self.ids.folder_list
        folder_list.clear_widgets()

        app = App.get_running_app()
        root_folder = app.DATA_FOLDER

        if not os.path.isdir(root_folder):
            print("DATA_FOLDER not found:", root_folder)
            return

        # Loop over subfolders inside DATA_FOLDER
        for item in sorted(os.listdir(root_folder)):
            full_path = os.path.join(root_folder, item)

            if os.path.isdir(full_path):
                # Create a folder button
                btn = Button(
                    text=item,
                    size_hint_y=None,
                    height=50,
                    background_normal="",               # remove default style
                    background_color=(0.12, 0.12, 0.13, 1),
                    color=(1, 1, 1, 1),                 # white text
                    on_release=lambda b, p=full_path: self.select_folder(p)
                )
                folder_list.add_widget(btn)

    def select_folder(self, folder_path):
        """
        Called when a folder button is clicked.
        - Store the selected folder
        - Load datasets from inside this folder
        - Clear selected dataset
        """
        self.current_folder = folder_path

        # Clear selected dataset in global state
        App.get_running_app().selected_file = ""
        self.ids.selected_label.text = "Selected dataset: "

        self.load_dataset_list(folder_path)

    # -------------------------------------------------------------------------
    #   DATASET LIST (MIDDLE COLUMN)
    # -------------------------------------------------------------------------
    def load_dataset_list(self, folder_path):
        """Load datasets that exist inside the selected folder."""

        dataset_list = self.ids.dataset_list
        dataset_list.clear_widgets()

        if not os.path.isdir(folder_path):
            print("Folder not found:", folder_path)
            return

        # Loop through subdirectories inside the selected folder
        for item in sorted(os.listdir(folder_path)):
            full_path = os.path.join(folder_path, item)

            if os.path.isdir(full_path):
                # Create a dataset button
                btn = Button(
                    text=item,
                    size_hint_y=None,
                    height=50,
                    on_release=lambda b, p=full_path: self.select_dataset(p),
                )
                dataset_list.add_widget(btn)

    def select_dataset(self, path):
        """
        Store selected dataset in the global app state and update label.
        """
        app = App.get_running_app()
        app.selected_file = path  # full path to dataset

        self.ids.selected_label.text = f"Selected dataset: {os.path.basename(path)}"
        print("Selected dataset:", path)

    # -------------------------------------------------------------------------
    #   START BUTTON
    # -------------------------------------------------------------------------
    def go_to_dicom(self):
        """Go to DICOM viewer only if a dataset is selected."""
        if App.get_running_app().selected_file:
            self.manager.current = "dicom"
        else:
            print("No dataset selected.")
