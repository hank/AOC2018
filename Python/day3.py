import sys
from collections import defaultdict
from arpeggio import OneOrMore, EOF
from arpeggio import RegExMatch as _
from arpeggio import ParserPython
from arpeggio import PTNodeVisitor, visit_parse_tree

# Format: #1 @ 1,3: 4x4
# #ID @ FromLeft, FromTop: WxH

def number(): return _(r"[0-9]+")
def cid(): return "#", number
def coords(): return number, ",", number
def dimension(): return number, "x", number
def claim(): return cid, _(r"\s*@\s*"), coords, _(":\s*"), dimension
def claims(): return OneOrMore(claim), EOF

class ClaimVisitor(PTNodeVisitor):
    def visit_cid(self, node, children):
        return int(children[0])
    def visit_coords(self, node, children):
        return int(children[0]), int(children[1])
    def visit_dimension(self, node, children):
        return int(children[0]), int(children[1])
    def visit_claim(self, node, children):
        return children[0], children[2], children[4]
    def visit_claims(self, node, children):
        # Entire set is done here.
        fabric = [[]]
        for c in children:
            # print(c)
            c_cid = c[0]
            c_coords = c[1]
            c_dim = c[2]
            # If there aren't enough columns, extend each row
            necessary_width = c_coords[0] + c_dim[0]
            # print("Necessary width = {}".format(necessary_width))
            if len(fabric[0]) < necessary_width:
                for row in fabric:
                    for i in range(len(row), necessary_width+1):
                        row.append(0)
                    # print(len(row))
            # If there aren't enough rows, extend rows
            necessary_height = c_coords[1] + c_dim[1]
            # print("Necessary height = {}".format(necessary_height))
            if len(fabric) < necessary_height:
                for i in range(len(fabric), necessary_height+1):
                    fabric.append([0] * len(fabric[0]))
                # print(len(fabric))
            # Increment values at offset with dims
            start_col = c_coords[0]
            start_row = c_coords[1]
            width = c_dim[0]
            height = c_dim[1]
            for i in range(start_row, start_row+height):
                for j in range(start_col, start_col+width):
                    # print("len {} {}, i={}, j={}".format(len(fabric), len(fabric[i]), i, j))
                    # print("Setting {}, {} to {}".format(i, j, fabric[i][j]+1))
                    fabric[i][j] += 1
        # Once complete, find number of values >=2
        total_count = 0
        for i in fabric:
            total_count += len([x for x in i if x >= 2])
        return total_count

if __name__ == "__main__":
    with open(sys.argv[1], 'r') as f:
        parser = ParserPython(claims)
        parse_tree = parser.parse(f.read())
        result = visit_parse_tree(parse_tree, ClaimVisitor())
        print(result)