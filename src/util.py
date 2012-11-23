"""
Utility functions that will be used by lots of code.

"""

dirs = {
  "mod" : "../data/mod",
  "map" : "../data/map",
}

# In case we miss out a / in the path
for key,itm in dirs.iteritems():
  itm += "/"


