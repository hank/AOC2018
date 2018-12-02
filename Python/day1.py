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
    def __init__(self, initial_value=0, **kwargs):
        super().__init__(**kwargs)
        self.initial_value=initial_value
    def visit_number(self, node, children):
        return int(node.value)
    def visit_operation(self, node, children):
        return node.value
    def visit_expression(self, node, children):
        if "-" == children[0]:
            print("Subtracting {}".format(children[1]))
            res = -1 * children[1]
        else:
            print("Adding {}".format(children[1]))
            res = children[1]
        return res
    def visit_calc(self, node, children):
        res = self.initial_value
        for c in children:
            res += c
        return res

if __name__ == "__main__":
    with open(sys.argv[1], 'r') as f:
        parser = ParserPython(calc)
        parse_tree = parser.parse(f.read())
        result = visit_parse_tree(parse_tree, FrequencyVisitor(initial_value=0))
        print(result)