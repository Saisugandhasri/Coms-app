def calculate_wpm(text: str, duration: float):
    if duration == 0:
        return 0
    words = len(text.split())
    return round(words / (duration / 60), 2)


FILLERS = ["um", "uh", "like", "you know", "actually", "basically", "so", "right"]


def count_fillers(text: str):
    text = text.lower()
    return sum(text.count(f) for f in FILLERS)
