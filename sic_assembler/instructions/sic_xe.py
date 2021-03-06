class INSTRUCTIONS:
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
        "ADDF": {"format": "3/4", "opcode": 0x58},
        "ADDR": {"format": "2", "opcode": 0x90},
        "CLEAR": {"format": "2", "opcode": 0xB4},
        "COMPF": {"format": "3/4", "opcode": 0x88},
        "COMPR": {"format": "2", "opcode": 0xA0},
        "DIVF": {"format": "3/4", "opcode": 0x64},
        "DIVR": {"format": "2", "opcode": 0x9C},
        "FIX": {"format": "1", "opcode": 0xC4},
        "FLOAT": {"format": "1", "opcode": 0xC0},
        "HIO": {"format": "1", "opcode": 0xF4},
        "LDB": {"format": "3/4", "opcode": 0x68},
        "LDF": {"format": "3/4", "opcode": 0x70},
        "LDS": {"format": "3/4", "opcode": 0x6C},
        "LDT": {"format": "3/4", "opcode": 0x74},
        "LPS": {"format": "3/4", "opcode": 0xD0},
        "MULF": {"format": "3/4", "opcode": 0x60},
        "MULR": {"format": "2", "opcode": 0x98},
        "NORM": {"format": "1", "opcode": 0xC8},
        "RMO": {"format": "2", "opcode": 0xAC},
        "SHIFTL": {"format": "2", "opcode": 0xA4},
        "SHIFTR": {"format": "2", "opcode": 0xA8},
        "SIO": {"format": "1", "opcode": 0xF0},
        "SSK": {"format": "3/4", "opcode": 0xEC},
        "STB": {"format": "3/4", "opcode": 0x78},
        "STF": {"format": "3/4", "opcode": 0x80},
        "STI": {"format": "3/4", "opcode": 0xD4},
        "STS": {"format": "3/4", "opcode": 0x7C},
        "STT": {"format": "3/4", "opcode": 0x84},
        "SUBF": {"format": "3/4", "opcode": 0x5C},
        "SUBR": {"format": "2", "opcode": 0x94},
        "SVC": {"format": "2", "opcode": 0xB0},
        "TIO": {"format": "1", "opcode": 0xF8},
        "TIXR": {"format": "2", "opcode": 0xB8},
    }

    DIRECTIVES = ["WORD", "BYTE", "RESB", "RESW"]
