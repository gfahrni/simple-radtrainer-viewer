# === dicom_viewer/mouse_controller.py ===
# This file handles mouse interactions in the DICOM viewer.
# It supports:
# - Right-click dragging to navigate slices
# - Mouse wheel scrolling to move through slices

class MouseController:
    """
    Handles mouse input for the DICOM viewer.

    Responsibilities:
    - Track right-click state for dragging
    - Detect scroll up/down events
    """

    def __init__(self):
        """
        Initialize the MouseController.

        Attributes:
        - is_right_click: True if the right mouse button is currently pressed
        - last_pos: last recorded mouse position (x, y)
        """
        self.is_right_click = False  # right-click is not active initially
        self.last_pos = (0, 0)  # initial mouse position

    def touch_down(self, widget, touch):
        """
        Handle mouse button press events.

        Parameters:
        - widget: the Kivy widget receiving the touch
        - touch: Kivy touch object containing position, button info, scroll

        Returns:
        - 'up'/'down' for scroll events (used by DicomScreen)
        - True if right-click started
        - False otherwise
        """
        if not widget.collide_point(*touch.pos):
            # Ignore touches outside the widget
            return False

        if touch.is_mouse_scrolling:
            # If user scrolls, return the scroll direction
            return touch.button  # 'scrolldown' or 'scrollup'

        if touch.button == 'right':
            # If right-click pressed, start drag mode
            self.is_right_click = True
            self.last_pos = touch.pos  # store initial click position
            return True  # indicate right-click handled

        return False  # all other touches are ignored

    def touch_move(self, widget, touch):
        """
        Handle mouse movement while pressing buttons.

        Parameters:
        - widget: the widget receiving the touch
        - touch: Kivy touch object

        Returns:
        - 'up' if dragging upwards
        - 'down' if dragging downwards
        - None if no action
        """
        if self.is_right_click and widget.collide_point(*touch.pos):
            # Calculate vertical movement (dy)
            dy = touch.pos[1] - self.last_pos[1]

            if abs(dy) > 5:  # threshold to avoid small jitters
                self.last_pos = touch.pos  # update last known position
                return "up" if dy > 0 else "down"  # return movement direction

        return None  # no significant movement

    def touch_up(self, touch):
        """
        Handle mouse button release events.

        Parameters:
        - touch: Kivy touch object

        Returns:
        - True if right-click was released
        - False otherwise
        """
        if touch.button == 'right':
            self.is_right_click = False  # end drag mode
            return True
        return False
