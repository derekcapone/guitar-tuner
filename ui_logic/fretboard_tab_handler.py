from PySide6.QtCore import Signal
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QPushButton, QLabel
from ui_generated.fretboard_tab import Ui_fretboard_tab

FRETBOARD_IMAGE_PATH = "assets/fretboard.jpg"
NUM_STRINGS = 6
NUM_FRETS = 13  # 12 frets plus open position

class FretboardTab(QWidget, Ui_fretboard_tab):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.fretboard_image = FretboardHandler()
        self.fretboard_hlayout.addWidget(self.fretboard_image)
        self.fretboard_image.note_signal.connect(self.handle_note)

        self.note_converter = GuitarNoteConverter()

    def handle_note(self, string: int, fret: int):
        print(f"New note: string: {string}, fret: {fret}")

        note_received = self.note_converter.string_fret_to_note(string, fret)
        self.note_label.setText(note_received)


class FretboardHandler(QLabel):
    FRET_SPACING_OFFSET = -3
    FRET_POSITION_STATIC_OFFSET = -95

    STRING_SPACING_OFFSET = -10
    STRING_POSITION_STATIC_OFFSET = 11

    note_signal = Signal(int, int)  # <String (1-6 where 1 is high E string), Fret (0-12)>

    def __init__(self):
        super().__init__()

        # Set up the image
        pixmap = QPixmap(FRETBOARD_IMAGE_PATH)
        self.setPixmap(pixmap)
        self.setFixedSize(pixmap.size())

        self.overlay_buttons()

    def overlay_buttons(self):
        width = self.width()
        height = self.height()

        fret_spacing = width / (NUM_FRETS + 1) + self.FRET_SPACING_OFFSET
        string_spacing = height / (NUM_STRINGS + 1) + self.STRING_SPACING_OFFSET

        for s in range(NUM_STRINGS):
            for f in range(NUM_FRETS):
                x = (f + 1) * fret_spacing + self.FRET_POSITION_STATIC_OFFSET
                y = (s + 1) * string_spacing + self.STRING_POSITION_STATIC_OFFSET
                btn = QPushButton("", self)
                btn.setGeometry(int(x), int(y), 20, 20)
                btn.setStyleSheet("background-color: rgba(0, 0, 255, 60);")
                btn.clicked.connect(self.make_note_handler(s, f))

    def make_note_handler(self, string, fret):
        def handler():
            self.note_signal.emit( string + 1, fret)
        return handler


class GuitarNoteConverter:
    def __init__(self, tuning=None):
        # Default standard tuning (EADGBE from low to high)
        self.tuning = tuning or ['E2', 'A2', 'D3', 'G3', 'B3', 'E4']

        # Chromatic scale
        self.chromatic_notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

        # MIDI note numbers (C4 = 60)
        self.note_to_midi = {}
        for octave in range(0, 9):
            for i, note in enumerate(self.chromatic_notes):
                midi_number = (octave + 1) * 12 + i
                self.note_to_midi[f"{note}{octave}"] = midi_number

    def string_fret_to_note(self, string_number, fret_number):
        """Convert string number (1-6) and fret (0-24) to note name"""
        if string_number < 1 or string_number > 6:
            raise ValueError("String number must be between 1 and 6")

        # Convert to 0-based index (string 6 = index 0, string 1 = index 5)
        string_index = 6 - string_number

        # Get open string note
        open_note = self.tuning[string_index]
        note_name = open_note[:-1]
        octave = int(open_note[-1])

        # Calculate new note
        start_index = self.chromatic_notes.index(note_name)
        new_index = (start_index + fret_number) % 12
        new_note = self.chromatic_notes[new_index]

        # Calculate octave
        octave_increase = (start_index + fret_number) // 12
        new_octave = octave + octave_increase

        return f"{new_note}{new_octave}"

    def string_fret_to_midi(self, string_number, fret_number):
        """Convert to MIDI note number"""
        note = self.string_fret_to_note(string_number, fret_number)
        return self.note_to_midi.get(note, None)

    def string_fret_to_frequency(self, string_number, fret_number):
        """Convert to frequency in Hz (A4 = 440Hz)"""
        midi_note = self.string_fret_to_midi(string_number, fret_number)
        if midi_note is None:
            return None

        # Formula: f = 440 * 2^((n-69)/12) where n is MIDI note number
        return 440.0 * (2 ** ((midi_note - 69) / 12))