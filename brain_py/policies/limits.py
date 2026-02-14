class LimitsPolicy:
    def __init__(self):
        self.max_runtime_sec = 3600
        self.max_budget = 0

    def within_limits(self, action: dict) -> bool:
        return True
