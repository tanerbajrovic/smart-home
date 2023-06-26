class AlarmState:
    
    # Constructor
    def __init__(self, locked: bool):
        self.code = None
        self.locked = locked
    
    # Is the code set?
    def hasCode(self) -> bool:
        return self.code is not None
    
    # Is the alarm on?
    def isLocked(self) -> bool:
        return self.locked
    
    # Unlock
    def unlock(self, code: str) -> None:
        if self.code is None or self.code == code:
            self.locked = False
        
    # Lock
    def lock(self) -> None:
        self.locked = True
        
    # Set code
    def setCode(self, newCode: str) -> None:
        self.code = newCode
      

