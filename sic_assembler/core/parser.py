from pprint import pprint
from re import split as reSplit, sub as reSub

from ..instructions.sic import INSTRUCTIONS
from ..instructions.line import Line


class Parser:
    def __init__(self, source, mode):
        self.source = source
        self.mode = mode

    def parse(self):
        parsedTokens = list()
        for (idx, l) in enumerate(self.source):
            if reSub(r"\t| ", "", l)[0] == ".":
                continue
            pl = [reSub(r"\n|\0|\r", "", ln) for ln in reSplit(r"\t", l) if len(ln)]
            if INSTRUCTIONS.isInstruction(pl[0]):
                parsedTokens.append(
                    Line(
                        idx,
                        pl,
                        pl[0],
                        None,
                        None
                        if len(pl) <= 1
                        else [
                            reSub(r"\n|\0|\r ", "", ln)
                            for ln in reSplit(r",", pl[1])
                            if len(ln)
                        ],
                    )
                )
            elif INSTRUCTIONS.isInstruction(pl[1]):
                parsedTokens.append(
                    Line(
                        idx,
                        pl,
                        pl[1],
                        None,
                        None
                        if len(pl) <= 2
                        else [
                            reSub(r"\n|\0|\r ", "", ln)
                            for ln in reSplit(r",", pl[2])
                            if len(ln)
                        ],
                        type_=self.mode,
                        label=pl[0],
                    )
                )
            else:
                if INSTRUCTIONS.isDirective(pl[0]):
                    parsedTokens.append(
                        Line(
                            idx,
                            pl,
                            pl[0],
                            None,
                            None
                            if len(pl) <= 1
                            else [
                                reSub(r"\n|\0|\r ", "", ln)
                                for ln in reSplit(r",", pl[1])
                                if len(ln)
                            ],
                            type_="directive",
                        )
                    )
                elif INSTRUCTIONS.isDirective(pl[1]):
                    parsedTokens.append(
                        Line(
                            idx,
                            pl,
                            pl[1],
                            None,
                            None
                            if len(pl) <= 2
                            else [
                                reSub(r"\n|\0|\r ", "", ln)
                                for ln in reSplit(r",", pl[2])
                                if len(ln)
                            ],
                            type_="directive",
                            label=pl[0],
                        )
                    )
                else:
                    parsedTokens.append(
                        Line(
                            idx,
                            pl,
                            pl[0],
                            None,
                            None
                            if len(pl) <= 1
                            else [
                                reSub(r"\n|\0|\r ", "", ln)
                                for ln in reSplit(r",", pl[1])
                                if len(ln)
                            ],
                            type_="directive",
                        )
                    )
        return parsedTokens
