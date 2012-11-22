"""
Utility functions that will be used by lots of code.

"""

gDirs = {
  "mod" : "../data/mod",
  "map" : "../data/map",
}

# In case we miss out a / in the path
for key,itm in gDirs.iteritems():
  itm += "/"


