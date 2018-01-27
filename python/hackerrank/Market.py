class Market:

    def __init__(self, marketValue, hour, dayOfMonth):
        self.marketValue = float(marketValue)
        self.hour = int(hour)
        self.dayOfMonth = int(dayOfMonth)

    @property
    def hour(self):
        return self._hour

    @hour.setter
    def hour(self, hr):
        if hr not in range(8, 17, 1):
            raise Exception("Hour: '{}' must be between 8-16".format(hr))
        self._hour = hr

    @property
    def dayOfMonth(self):
        return self._dayOfMonth

    @dayOfMonth.setter
    def dayOfMonth(self, dayOM):
        if dayOM not in range(1, 31, 1):
            raise Exception("Month of data point must be between 8-16")
        self._dayOfMonth = dayOM
