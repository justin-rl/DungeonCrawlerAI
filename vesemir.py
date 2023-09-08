import os
from swiplserver import PrologMQI

class Vesemir:
    def __init__(self) -> None:
        self._mqi = PrologMQI()
        self._prolog_thread = self._mqi.create_thread()
        for filename in os.listdir("knowledge"):
            if filename.endswith(".pl"):
                self._prolog_thread.query(f"[knowledge/{filename[:-3]}]")
    
    
