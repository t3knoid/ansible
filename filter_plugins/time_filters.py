def seconds_to_dhms(seconds):
    seconds = int(seconds)
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    return f"{days}d {hours}h {minutes}m {seconds}s"

class FilterModule(object):
    def filters(self):
        return {
            'dhms': seconds_to_dhms
        }
