
class _Warning:
    Counter = 0
    def __init__(self, content):
        _Warning.Counter += 1
        print('Warning: ' + content)

class Error:
    Counter = 0
    def __init__(self, content):
        Error.Counter += 1
        print('Error: ' + content)
