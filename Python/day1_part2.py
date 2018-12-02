import sys
from arpeggio import OneOrMore, EOF
from arpeggio import RegExMatch as _
from arpeggio import ParserPython
from arpeggio import PTNodeVisitor, visit_parse_tree

def number(): return _(r"[0-9]+")
def operation(): return _(r"\+|-")
def expression(): return operation, number
def calc(): return OneOrMore(expression), EOF

class FrequencyVisitor(PTNodeVisitor):
    def __init__(self, s=None, initial_value=0, **kwargs):
        super().__init__(**kwargs)
        self.initial_value=initial_value
        self.s = s
    def visit_number(self, node, children):
        return int(node.value)
    def visit_operation(self, node, children):
        return node.value
    def visit_expression(self, node, children):
        if "-" == children[0]:
            # print("Subtracting {}".format(children[1]))
            res = -1 * children[1]
        else:
            # print("Adding {}".format(children[1]))
            res = children[1]
        return res
    def visit_calc(self, node, children):
        res = self.initial_value
        for c in children:
            set_size = len(self.s)
            res += c
            self.s.add(res)
            print("res={}, setsize={}".format(res, len(s)))
            if set_size == len(self.s):
                # Duplicate
                raise RuntimeError("::: Duplicate: {}".format(res))
        return res

if __name__ == "__main__":
    with open(sys.argv[1], 'r') as f:
        parser = ParserPython(calc)
        contents = f.read()
        parse_tree = parser.parse(contents)
        s = set()
        result = 0
        while True:
            result = visit_parse_tree(parse_tree, FrequencyVisitor(s=s, initial_value=result))
        print(result)