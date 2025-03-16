class TimeSystem:
    def __init__(self):
        self.phases = ["Morning", "Noon", "Evening", "Night"]
        self.current_phase_index = 0
        self.day = 1
    def current_phase(self):
        return self.phases[self.current_phase_index]
    def next_turn(self):
        self.current_phase_index += 1
        if self.current_phase_index >= len(self.phases):
            self.current_phase_index = 0
            self.day += 1
        return self.current_phase()

class Calendar:
    def __init__(self):
        self.hour = 10
        self.minute = 00
        self.day = 1
        self.month = 1
        self.year = 1
        self.days_in_month = 30
        self.months_in_year = 15
    def advance_time(self, hours):
        self.hour += hours
        while self.hour >= 24:
            self.hour -= 24
            self.day += 1
            if self.day > self.days_in_month:
                self.day = 1
                self.month += 1
                if self.month > self.months_in_year:
                    self.month = 1
                    self.year += 1
    def current_time(self):
        return f"{self.hour:02}:{self.minute:02} – Day {self.day}, Month {self.month}, Year {self.year}"

class GameTime:
    def __init__(self):
        self._calendar = Calendar()

    def wait_turn(self):
        self._calendar.advance_time(1)
        hour = self._calendar.hour
        if 6 <= hour < 12:
            phase = "Morning"
        elif 12 <= hour < 18:
            phase = "Noon"
        elif 18 <= hour < 24:
            phase = "Evening"
        else:
            phase = "Night"
        return phase, self._calendar.current_time()
