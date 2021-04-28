class INSTRUCTIONS:
    @staticmethod
    def isInstruction(ins):
        return ins in INSTRUCTIONS.INSTRUCTIONS.keys()

    @staticmethod
    def isDirective(ins):
        return ins in INSTRUCTIONS.DIRECTIVES

    INSTRUCTIONS = {
        "ADD": {"format": "3/4", "opcode": 0x18},
        "AND": {"format": "3/4", "opcode": 0x40},
        "COMP": {"format": "3/4", "opcode": 0x28},
        "DIV": {"format": "3/4", "opcode": 0x24},
        "J": {"format": "3/4", "opcode": 0x3C},
        "JEQ": {"format": "3/4", "opcode": 0x30},
        "JGT": {"format": "3/4", "opcode": 0x34},
        "JLT": {"format": "3/4", "opcode": 0x38},
        "JSUB": {"format": "3/4", "opcode": 0x48},
        "LDA": {"format": "3/4", "opcode": 0x00},
        "LDCH": {"format": "3/4", "opcode": 0x50},
        "LDL": {"format": "3/4", "opcode": 0x08},
        "LDX": {"format": "3/4", "opcode": 0x04},
        "MUL": {"format": "3/4", "opcode": 0x20},
        "OR": {"format": "3/4", "opcode": 0x44},
        "RD": {"format": "3/4", "opcode": 0xD8},
        "RSUB": {"format": "3/4", "opcode": 0x4C},
        "STA": {"format": "3/4", "opcode": 0x0C},
        "STCH": {"format": "3/4", "opcode": 0x54},
        "STL": {"format": "3/4", "opcode": 0x14},
        "STSW": {"format": "3/4", "opcode": 0xE8},
        "STX": {"format": "3/4", "opcode": 0x10},
        "SUB": {"format": "3/4", "opcode": 0x1C},
        "TD": {"format": "3/4", "opcode": 0xE0},
        "TIX": {"format": "3/4", "opcode": 0x2C},
        "WD": {"format": "3/4", "opcode": 0xDC},
    }

    DIRECTIVES = ["START", "END", "WORD", "BYTE", "RESB", "RESW"]
