from .parser import Parser
from .translator import Translator


class Assembler:
    @staticmethod
    def assemble(args=None):
        path = args.s
        out = args.o or "a.obj"
        # mode = (args.mode or "sic").lower()
        mode = "sic"

        tokens = Parser(Assembler._readasm(path), mode).parse()
        translator = Translator(tokens, mode)
        res = translator.translate()
        Assembler._writeasm(out, res)
        print("=" * 60)
        print(res)
        print("=" * 60)

    @staticmethod
    def _readasm(path):
        try:
            with open(path) as f:
                raw = f.readlines()
                if len(raw) > 0:
                    return raw
                else:
                    raise Exception(f"Cannot open file {path} (File is empty)")
        except:
            raise Exception(f"Cannot open file {path} (File not found)")

    @staticmethod
    def _writeasm(path, code):
        with open(path, "w") as f:
            f.write(code.upper())
