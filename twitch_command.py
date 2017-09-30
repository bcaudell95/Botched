class TwitchCommand:
    def __init__(self, command, *args, **kwargs):
        self._command = command

    def execute(self, sender, message, *args, **kwargs):
        raise NotImplementedError()