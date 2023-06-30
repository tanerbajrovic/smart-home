class AlarmState:
    
    # Constructor
    def __init__(self, locked: bool):
        self.code = None
        self.resetCode = "9999"
        self.locked = locked
    
    # Is the code set?
    def hasCode(self) -> bool:
        return self.code is not None
    
    # Is the alarm on?
    def isLocked(self) -> bool:
        return self.locked
    
    # Unlock
    def unlock(self, code: str) -> bool:
        if not self.hasCode() or self.code == code:
            self.locked = False
            return not self.locked
        
    # Lock
    def lock(self) -> None:
        self.locked = True
        
    # Set code
    def setCode(self, new_code: str) -> None:
        self.code = new_code
        
      

