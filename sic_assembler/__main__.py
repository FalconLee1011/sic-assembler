import argparse


from sic_assembler.core.assembler import Assembler


def initARG():
    parser = argparse.ArgumentParser(
        prog="SIC Assembler",
        description="A SIC Assembler by Falcon aka 草",
    )
    parser.add_argument("-s", help="Asm source code, required.", required=True)
    parser.add_argument("-o", help="Output")
    # parser.add_argument("--mode", help="Target platform [ sic (default) | sic/xe ]")
    args = parser.parse_args()
    return args


def main():
    args = initARG()
    Assembler.assemble(args=args)


if __name__ == "__main__":
    main()
