from machine import Pin
import time
import random
import json
import urequests
import network

FIREBASE_URL = "https://mini-85070-default-rtdb.firebaseio.com/scores.json"

SSID = "BU Guest (unencrypted)"

N = 10
sample_ms = 10.0
on_ms = 500

def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    print(wlan.ifconfig())

def random_time_interval(tmin: float, tmax: float) -> float:
    return random.uniform(tmin, tmax)


def blinker(N: int, led: Pin) -> None:
    for _ in range(N):
        led.high()
        time.sleep(0.1)
        led.low()
        time.sleep(0.1)


def write_json(json_filename: str, data: dict) -> None:
    with open(json_filename, "w") as f:
        json.dump(data, f)


def upload_to_firebase(data: dict) -> None:
        response = urequests.post(FIREBASE_URL, json=data)
        print(f"Firebase response: {response.text}")
        response.close()

def scorer(t: list[int | None]) -> None:
    # Collate results
    misses = t.count(None)
    print(f"You missed the light {misses} / {len(t)} times")

    t_good = [x for x in t if x is not None]

    # Add key, value to this dict to store the minimum, maximum, average response time
    data = {
        "min_time": min(t_good) if t_good else None,
        "max_time": max(t_good) if t_good else None,
        "avg_time": sum(t_good) / len(t_good) if t_good else None,
        "score": (len(t_good) / len(t)) if t else 0
    }

    # Make dynamic filename and write JSON
    now = time.localtime()
    now_str = "-".join(map(str, now[:3])) + "T" + "_".join(map(str, now[3:6]))
    filename = f"score-{now_str}.json"

    print("Writing to", filename)
    write_json(filename, data)

    upload_to_firebase(data)

    upload_to_firebase({"data_points": t})


if __name__ == "__main__":
    connect()

    led = Pin("LED", Pin.OUT)
    button = Pin(16, Pin.IN, Pin.PULL_UP)

    t = []

    blinker(3, led)

    for i in range(N):
        time.sleep(random_time_interval(0.5, 5.0))

        led.high()

        tic = time.ticks_ms()
        t0 = None
        while time.ticks_diff(time.ticks_ms(), tic) < on_ms:
            if button.value() == 0:
                t0 = time.ticks_diff(time.ticks_ms(), tic)
                led.low()
                break
        t.append(t0)

        led.low()

    blinker(5, led)

    scorer(t)

