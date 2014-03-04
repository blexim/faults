#!/usr/bin/python

import re
import sys

measure_re = re.compile("def ([^(]*)")

f = open(sys.argv[1])
o = open(sys.argv[2], "w")

o.write("""
#!/usr/bin/python

import metrics

suite = {
""")

for l in f.readlines()[63:]:
  m = measure_re.match(l)

  if m:
    name = m.group(1)

    o.write("  '%s': metrics.%s,\n" % (name, name))

o.write("""
}
""")

f.close()
o.close()
