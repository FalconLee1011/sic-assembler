class Line:
    def __init__(self, idx, raw, ins, x, operand, type_="sic", label=None):
        self.type = type_
        self.raw = raw
        self.line = idx + 1
        if type_ == "sic":
            from .sic import INSTRUCTIONS

            _op = INSTRUCTIONS.INSTRUCTIONS[ins]
            if _op is None:
                raise Exception(f"Unknown instruction {ins} on line {self.line}")

            self.op = _op.get("opcode")
            self.format = _op.get("format")
            self.ins = ins
            self.x = x
            self.operand = operand
            self.label = label
        elif type_ == "directive":
            self.ins = ins
            self.operand = operand
            self.label = label

        # * RESERVED FOR SIC/XE
        # self.n = n
        # self.i = i
        # self.x = x
        # self.b = b
        # self.p = p
        # self.e = e
        # self.addr = addr

    def __str__(self):
        def _operand2str(operand):
            if operand is None or len(operand) == 0:
                return "None"
            operandStr = ""
            for (i, o) in enumerate(operand):
                if o.isdigit():
                    print(f'{o}({hex(int(o))})')
                    operandStr += f'{o}({hex(int(o))})'
                else: 
                    operandStr += o
                if(i + 1 != len(operand)): 
                    operandStr += ", "
            return operandStr

        _f = "{:^15} {:^15} {:^15} {:^15} {:^15} {:^15} {:^15}"
        print(_f.format("type", "label", "op", "ins", "x", "operand", "raw"))
        operand = _operand2str(self.operand)
        if self.type == "sic":
            _f += "\n"
            return _f.format(
                f"[{self.type}]",
                f"{self.label}",
                f"{hex(self.op)}",
                f"{self.ins}",
                f"{self.x}",
                f"{operand}",
                f"{self.raw}",
            )
        if self.type == "directive":
            _f += "\n"
            return _f.format(
                f"[{self.type}]",
                f"{self.label}",
                "-",
                f"{self.ins}",
                "-",
                f"{operand}",
                f"{self.raw}",
            )
