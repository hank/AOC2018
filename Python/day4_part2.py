from pprint import PrettyPrinter
import sys, re
from collections import defaultdict
from datetime import datetime, timedelta
from arpeggio import OneOrMore, EOF
from arpeggio import RegExMatch as _
from arpeggio import ParserPython
from arpeggio import PTNodeVisitor, visit_parse_tree

# [1518-11-01 00:00] Guard #10 begins shift

def time(): return _(r"\d{2}"), ":", _(r"\d{2}")
def date(): return _(r"\d{4}"), "-", _(r"\d{2}"), "-", _(r"\d{2}")
def tstamp(): return "[", date, time, "]"
def word(): return _(r"[#\w]+")
def logentry(): return tstamp, OneOrMore(word)
def log(): return OneOrMore(logentry), EOF

class LogEntryVisitor(PTNodeVisitor):
    def __init__(self):
        super().__init__()
        self.guards = defaultdict(dict)
    def visit_date(self, node, children):
        # YMD already
        return datetime(*[int(x) for x in children])
    def visit_time(self, node, children):
        c = [int(x) for x in children]
        return timedelta(hours=c[0], minutes=c[1])
    def visit_tstamp(self, node, children):
        return children[0] + children[1]
    def visit_logentry(self, node, children):
        return children[0], " ".join(children[1:])
    def visit_log(self, node, children):
        # Sort and return
        sorted_entries = sorted(children, key=lambda t: t[0])
        return sorted_entries

if __name__ == "__main__":
    pp = PrettyPrinter()
    with open(sys.argv[1], 'r') as f:
        parser = ParserPython(log)
        parse_tree = parser.parse(f.read())
        result = visit_parse_tree(parse_tree, LogEntryVisitor())
        guards = defaultdict(dict)
        current_id = 0
        for r in result:
            # Process the entry
            dt = r[0]
            entry = r[1]
            if re.match(r"falls", entry):
                guards[current_id]['sleep_start'] = dt
            elif re.match(r"wakes", entry):
                guards[current_id]['minutes_asleep'] += (dt - guards[current_id]['sleep_start']).total_seconds()
                # Also track minutes for this guard

                mins_start = guards[current_id]['sleep_start'].timetuple()[4]
                mins_end = dt.timetuple()[4]
                for m in range(mins_start, mins_end):
                    guards[current_id]['minutes'][m] += 1
                del(guards[current_id]['sleep_start'])
            else:
                m = re.match(r"Guard #(\d+) begins shift", entry)
                if m:
                    gid = m.group(1)
                    if 'minutes_asleep' not in guards[gid]:
                        guards[gid]['minutes_asleep'] = 0
                    if 'minutes' not in guards[gid]:
                        guards[gid]['minutes'] = defaultdict(int)
                    current_id = gid
        # Find guard most asleep on the same minute
        # First, find the max count for a minute over all guards
        max_minute_guard = 0
        max_minute = 0
        max_minutes = 0
        for g in guards.items():
            if len(g[1]['minutes']) > 0:
                x = max(g[1]['minutes'].items(), key=lambda l: l[1])
                if x[1] > max_minutes:
                    max_minutes = x[1]
                    max_minute = x[0]
                    max_minute_guard = g[0]

        print("Max was guard {} with {} on minute {}, final: {}".format(
            max_minute_guard, max_minutes, max_minute, max_minute*int(max_minute_guard)))