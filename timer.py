class Timer:
    def __init__(self, endTime, completion):
        self.endTime = endTime
        self.completion = completion

        self.time = 0

    def update(self):
        if self.time == self.endTime:
            self.completion()
        else:
            self.time += 1
