import math
from array import array
import pygame

# Simple sound effects generated in code, so no audio files are needed.
# Each effect is a list of (start_hz, end_hz, seconds) segments: a tone
# that slides from start to end pitch and fades out.
EFFECTS = {
    "jump": [(400, 800, 0.12)],                     # quick rising chirp
    "goal": [(660, 660, 0.10), (990, 990, 0.20)],   # two-note chime
    "death": [(400, 100, 0.45)],                    # falling "wah"
}


def _build(segments, rate, channels, volume=0.35):
    samples = array("h")
    phase = 0.0
    for start, end, duration in segments:
        n = int(rate * duration)
        for i in range(n):
            t = i / n
            phase += 2 * math.pi * (start + (end - start) * t) / rate
            value = int(32767 * volume * (1 - t) * math.sin(phase))
            samples.extend([value] * channels)
    return pygame.mixer.Sound(buffer=samples.tobytes())


class Sounds:
    def __init__(self):
        self.effects = {}
        mixer = pygame.mixer.get_init()  # None if there is no audio device
        if mixer is None or mixer[1] != -16:
            return  # stay silent rather than crash
        rate, _, channels = mixer
        try:
            for name, segments in EFFECTS.items():
                self.effects[name] = _build(segments, rate, channels)
        except pygame.error:
            self.effects = {}

    def play(self, name):
        sound = self.effects.get(name)
        if sound is not None:
            sound.play()