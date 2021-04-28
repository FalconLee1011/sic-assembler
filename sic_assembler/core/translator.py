from copy import deepcopy

from ..instructions.sic import INSTRUCTIONS


class Translator:
    def __init__(self, tokens, type_):
        self.tokens = tokens
        self.START = 0
        self.LEN = 0
        self.symbolTable = dict()
        self.type = type_
        self.output = ""
        self.header = ""
        self.end = ""

    def translate(self):
        self._pass1(self.tokens)
        self._pass2(self.tokens)
        return self._construct(self.header, self.output, self.end)
        

    def _construct(self, header, text, end):
        opt = f"H{header.upper()}\n"
        len_ = hex(int(len(text)/2))[2:]
        opt += f"T{'{0:0{1}x}'.format(self.START, 6)}{len_}"
        opt += f"{text.upper()}\n"
        opt += f"E{end.upper()}\n"
        return opt

    def _pass1(self, tokens):
        tokens = deepcopy(tokens)

        self.DebugPrintTokens(tokens)

        locctr = 0
        if tokens[0].type == "directive" and tokens[0].ins == "START":
            locctr = int(tokens[0].operand[0], 16)
            tokens.pop(0)
        self.START = locctr

        for token in tokens:
            if token.label in self.symbolTable:
                raise Exception(f"Duplicate label on line {token.line}")
            if token.label is not None:
                self.symbolTable[token.label] = locctr

            if token.type == "directive":
                if token.ins == "END":
                    self.LEN = locctr - self.START
                    break
                else:
                    locctr = self._pass1ProcessDirective(token, locctr)
            elif token.type == self.type:
                locctr += 3
        
        print(self.symbolTable)

    def _pass2(self, tokens):
        print(
            "\n\n----------------------------------------------------------------------------------------------------------------------------"
        )
        print("Entering pass2")
        print(
            "----------------------------------------------------------------------------------------------------------------------------\n\n"
        )
        tokens = deepcopy(tokens)

        locctr = 0
        if tokens[0].type == "directive" and tokens[0].ins == "START":
            locctr = int(tokens[0].operand[0], 16)
            self.START = locctr
            self._write_start(tokens[0].label)
            tokens.pop(0)

        for token in tokens:
            if token.ins == "END":
                if token.operand[0]:
                    self._write_end(self.symbolTable[token.operand[0]])
                else:
                    self._write_end(self.LEN)
            elif token.type == "directive":
                locctr = self._pass2ProcessDirective(token, locctr)
            elif token.type == self.type:
                locctr = self._pass2ProcessInstruction(token, locctr)
            print("{:^10} {:^10} {:^10}".format("LINE RESULT", locctr, self.output))

    def _write_start(self, progname):
        print("write start")
        output = f"{progname} "
        output += self._extendHexLen(self.START)
        output += self._extendHexLen(self.LEN)
        self.header += output

    def _write_end(self, addr):
        print("write end")
        self.end += self._extendHexLen(addr)

    def _extendHexLen(self, hex_):
        hex_ = hex(hex_).upper()
        hex_ = hex_[2:]
        n = 6 - len(hex_)
        for i in range(0, n):
            hex_ = "0" + hex_
        return hex_

    def _processBYTEC(self, operand):
        constant = ""
        for i in range(2, len(operand) - 1):
            tmp = hex(ord(operand[i]))
            tmp = tmp[2:]
            if len(tmp) == 1:
                tmp = "0" + tmp
            tmp = tmp.upper()
            constant += tmp
        return constant

    def _pass1ProcessDirective(self, token, locctr):
        print("Processing Directive... (Pass 1)")
        print(token)
        print(
            "----------------------------------------------------------------------------------------------------------------------------"
        )
        if token.ins == "WORD":
            return locctr + 3
        elif token.ins == "BYTE":
            return locctr + 3
        elif token.ins == "RESB":
            return locctr + int(token.operand[0])
        elif token.ins == "RESW":
            return locctr + (int(token.operand[0]) * 3)
        else:
            raise Exception(f'Unknown directive "{token.ins}" on line {token.line}')

    def _pass2ProcessInstruction(self, token, locctr):
        print("Processing Instruction... (Pass 2)")
        print(token)
        if(token.ins == "RSUB"):
            self.output += hex(token.op)[2:] + "0000"
            return locctr + 3
        print(f"{token.ins} -> {hex(token.op)}")
        print(f"Adding {hex(token.op)[2:]}")
        opcode = hex(token.op)[2:]
        print(f"operand[0] = {token.operand[0]}")
        print(f"label = {token.label}")
        print(f"symbol table = {self.symbolTable}")
        print(f"from symbol table = {self.symbolTable.get(token.operand[0])}")
        operand = str( token.operand[0] if(self.symbolTable[token.operand[0]] is None) else self.symbolTable[token.operand[0]] )
        self.output += self._generateCode(opcode, operand)
        print(self.output)
        print(
            "----------------------------------------------------------------------------------------------------------------------------"
        )
        return locctr + 3

    def _pass2ProcessDirective(self, token, locctr):
        print("Processing Directive... (Pass 2)")
        print(token)
        print(
            "----------------------------------------------------------------------------------------------------------------------------"
        )
        if token.ins == "WORD":
            if locctr + 3 - self.START > 30:
                self.START = locctr
                self.output = self._extendHexLen(int(token.operand[0]))
            else:
                self.output += self._extendHexLen(int(token.operand[0]))
            return locctr + 3
        elif token.ins == "BYTE":
            operandlen = 0
            context = ""
            if token.operand[0] == "X":
                operandlen = int((len(token.operand[0] - 3) / 2))
                context = token.operand[0][2 : len(token.operand[0]) - 1]
            elif token.operand[0] == "C":
                operandlen = int(len(token.operand[0]) - 3)
                context = self._processBYTEC(token.operand[0])
            if locctr + 3 - self.START > 30:
                self.START = locctr
                self.output = context
            else:
                self.output += context
            return locctr + 3
        elif token.ins == "RESB":
            return locctr + int(token.operand[0])
        elif token.ins == "RESW":
            return locctr + (int(token.operand[0]) * 3)
        else:
            raise Exception(f'Unknown directive "{token.ins}" on line {token.line}')

    def _generateCode(self, opcode, operand):
        instruction = 0
        print("Generating opcode")
        convertedOpcode = int(opcode, 16) * 65536
        print(f"Got code {opcode} -> {convertedOpcode}")
        print(f"Got operand[0] {operand} -> {int(operand)}")
        instruction = int(convertedOpcode) + int(operand)
        insConverted = "{0:0{1}x}".format(instruction, 6)
        print(f"Done generate code -> {instruction} -> {insConverted}")
        return insConverted

    def DebugPrintTokens(self, tokens):
        print(
            "---------------------------------------------------------- TOKENS ----------------------------------------------------------"
        )
        for t in tokens:
            print(t)
        print(
            "----------------------------------------------------------------------------------------------------------------------------"
        )