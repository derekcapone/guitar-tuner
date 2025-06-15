from dataclasses import dataclass


class NoteMessage:
    def __init__(self, frequency: float):
        self.frequency = frequency



# @dataclass
# class NoteMessage:
#     frequency: float