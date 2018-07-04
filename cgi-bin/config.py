#!/usr/bin/env python3
windows = dict(
    color = 'blue',
    brand = 'ford',
)

linux = dict(
    cgi_file    = 'http://student.cryst.bbk.ac.uk/cgi-bin/cgiwrap/ro001/front_module.py',
    homepage    = 'http://student.cryst.bbk.ac.uk/~ro001/index.html',
    results     = 'http://student.cryst.bbk.ac.uk/~ro001/about.html'
)

    doors = 2,
)
and use it like that :

import config
print config.truck['color']  
