from copy import deepcopy
from re import sub as reSub

from ..instructions.sic import INSTRUCTIONS


class Translator:
    def __init__(self, tokens, type_):
        self.tokens = tokens
        self.START = 0
        self.LEN = 0
        self.symbolTable = dict()
        self.type = type_
        self.text = ""
        self.output = ""
        self.header = ""
        self.end = ""

    def translate(self):
        self._pass1(self.tokens)
        self._pass2(self.tokens)
        return self._construct(self.header, self.output, self.end)

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
                    print(f"\033[38;5;13m locctr -> {locctr} ({hex(locctr)})\033[0;0;0m")
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
            self._writeStart(tokens[0].label)
            tokens.pop(0)

        for token in tokens:
            if token.ins == "END":
                if token.operand[0]:
                    self._writeText()
                    self._writeEnd(self.symbolTable[token.operand[0]])
                else:
                    self._writeEnd(self.LEN)
            elif token.type == "directive":
                locctr = self._pass2ProcessDirective(token, locctr)
            elif token.type == self.type:
                locctr = self._pass2ProcessInstruction(token, locctr)
            print("{:^10} {:^10} {:^10}".format("LINE RESULT", locctr, self.text))

    def _writeStart(self, progname):
        print("write start")
        output = f"{progname} "
        output += "{0:0{1}x}".format(self.START, 6)
        output += "{0:0{1}x}".format(self.LEN, 6)
        self.header += output

    def _writeEnd(self, addr):
        print("write end")
        self.end += "{0:0{1}x}".format(addr, 6)


    def _construct(self, header, output, end):
        opt = f"H{header.upper()}\n"
        # len_ = hex(int(len(text)/2))[2:]
        # opt += f"T{'{0:0{1}x}'.format(self.START, 6)}{len_}"
        # opt += f"{text.upper()}\n"
        opt += f"{output}"
        opt += f"E{end.upper()}\n"
        return opt

    def _writeText(self):
        len_ = hex(int(len(self.text)/2))[2:]
        print(f"{'='*50}\n{'='*50}")
        self.output += f"T{'{0:0{1}x}'.format(self.START, 6)}{len_}"
        self.output += f"{self.text.upper()}\n"
        print(f"OUTPUT UPDATE -> {self.output}")
        print(f"{'='*50}\n{'='*50}")
        self.text = ""
        # self.output += f"T{'{0:0{1}x}'.format(self.START, 6)}{len_}"
        # self.output += f"{self.text.upper()}\n"

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
            print(f"\033[38;5;4mGOT DIRECTIVE BYTE\033[0;0;0m")
            print(f"\033[38;5;4m╰➤{token}\033[0;0;0m")
            if token.operand[0][0] == 'X':
                return locctr + int((len(token.operand[0]) - 3) / 2)
            elif token.operand[0][0] == 'C':
                print(f"\033[38;5;4m╰───➤{locctr} + {int(len(token.operand[0]) - 3)}\033[0;0;0m")
                return locctr + int(len(token.operand[0]) - 3)
            # else:
            #     return locctr + 3
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
            self.text += hex(token.op)[2:] + "0000"
            return locctr + 3
        
        print(f"\033[38;5;10m{token.ins} -> {hex(token.op)}\033[0;0;0m")
        print(f"Adding {hex(token.op)[2:]}")
        
        opcode = hex(token.op)[2:]
        
        print(f"operand[0] = {token.operand[0]}")
        print(f"label = {token.label}")
        print(f"symbol table = {self.symbolTable}")
        print(f"from symbol table = {self.symbolTable.get(token.operand[0])}")

        if locctr + 3 - self.START > 30:
            self._writeText()
            self.START = locctr
            self.text = self._generateCode(opcode, token.operand)
        else:
            self.text += self._generateCode(opcode, token.operand)
        
        print(self.text)
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
                self._writeText()
                self.START = locctr
                self.text = "{0:0{1}x}".format(int(token.operand[0]), 6)
            else:
                self.text += "{0:0{1}x}".format(int(token.operand[0]), 6)
            return locctr + 3
        elif token.ins == "BYTE":
            print(f"\033[38;5;4mGOT DIRECTIVE BYTE\033[0;0;0m")
            print(f"\033[38;5;4m╰➤{token}\033[0;0;0m")
            operandlen = 0
            context = ""
            if token.operand[0][0] == "X":
                operandlen = int((len(token.operand[0]) - 3) / 2)
                # context = token.operand[0][2 : len(token.operand[0]) - 1]
                context = reSub(r"'|X|x", "", token.operand[0])
                print(f"\033[38;5;4m╰──────➤{token.operand[0]}\033[0;0;0m")
            elif token.operand[0][0] == "C":
                operandlen = int(len(token.operand[0]) - 3)
                context = self._processBYTEC(token.operand[0])
            if locctr + 3 - self.START > 30:
                self._writeText()
                self.START = locctr
                self.text = context
            else:
                print("+"*30)
                print(context)
                print("+"*30)
                self.text += context
            return locctr + operandlen
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
        operand_0 = str( operand[0] if(self.symbolTable[operand[0]] is None) else self.symbolTable[operand[0]] )
        if len(operand) == 2:
            if operand[1] == 'X':
                instruction += 32768
        # print(f"\033[38;5;10m{out}\033[0;0;0m")
        print(f"\033[38;5;10mGot code {opcode} -> {convertedOpcode}\033[0;0;0m")
        print(f"Got operand[0] {operand_0} -> {int(operand_0)}")
        instruction = int(convertedOpcode) + int(operand_0)
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