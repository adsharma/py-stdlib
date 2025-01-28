from stdlib import time


class datetime:
    @classmethod
    def now(cls) -> "datetime":
        # Get the current time in seconds since the epoch
        seconds_since_epoch = time.time()

        # Convert seconds to a struct_time object
        struct_time_obj = time.localtime(seconds_since_epoch)

        # Create a datetime object from the struct_time object
        return cls(
            year=struct_time_obj.tm_year,
            month=struct_time_obj.tm_mon,
            day=struct_time_obj.tm_mday,
            hour=struct_time_obj.tm_hour,
            minute=struct_time_obj.tm_min,
            second=struct_time_obj.tm_sec,
            microsecond=int((seconds_since_epoch % 1) * 1e6),
        )

    def __init__(self, year, month, day, hour, minute, second, microsecond):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.second = second
        self.microsecond = microsecond

    def __str__(self):
        return f"{self.year}-{self.month:02d}-{self.day:02d} {self.hour:02d}:{self.minute:02d}:{self.second:02d}.{self.microsecond:06d}"
