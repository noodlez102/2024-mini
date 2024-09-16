#!/usr/bin/env python3
"""
PWM Tone Generator

based on https://www.coderdojotc.org/micropython/sound/04-play-scale/
"""

import machine
import utime

# GP16 is the speaker pin
SPEAKER_PIN = 16

# create a Pulse Width Modulation Object on this pin
speaker = machine.PWM(machine.Pin(SPEAKER_PIN))


def playtone(frequency: float, duration: float) -> None:
    speaker.duty_u16(1000)
    speaker.freq(frequency)
    utime.sleep(duration)


def quiet():
    speaker.duty_u16(0)


freq: float = 262
duration: float = 0.5  # seconds

print("Playing frequency (Hz):")

playtone(freq, duration)
playtone(freq, duration)

freq = 392
playtone(freq, duration)
playtone(freq, duration)
freq = 440
playtone(freq, duration)
playtone(freq, duration)
freq = 392
playtone(freq, duration)

    

# Turn off the PWM
quiet()
