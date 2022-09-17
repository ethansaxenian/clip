import json
import sys


class Clipboard:
    registers: dict[str, str]

    def __init__(self, _cache_file: str):
        self.cache_file = _cache_file

    def load_registers(self):
        try:
            with open(self.cache_file, "r") as buf_file:
                self.registers = json.load(buf_file)
        except FileNotFoundError:
            self.registers = {}

    def save_registers(self):
        with open(self.cache_file, "w+") as buf_file:
            json.dump(self.registers, buf_file, ensure_ascii=False)

    def is_empty(self) -> bool:
        return not bool(self.registers)

    def show_registers(self):
        if self.is_empty():
            print("Clipboard is empty.")
        else:
            print(
                json.dumps(self.registers, ensure_ascii=False, indent=2, sort_keys=True)
            )

    def reset_registers(self):
        print("Clearing registers...")
        self.registers.clear()

    def __getitem__(self, item):
        return self.registers[item]

    def __setitem__(self, key, value):
        self.registers[key] = value

    def __delitem__(self, key):
        del self.registers[key]

    def __enter__(self):
        self.load_registers()
        return self

    def __exit__(self, exc_type, exc_value, exc_tb) -> bool:
        if exc_type is KeyError:
            print(f"Buffer {exc_value} not found.", file=sys.stderr)
            return True

        self.save_registers()
