# Implement python stdlib in typed python

This avoids C-API and breaks compatibility with CPython. But it has some benefits:

* Moves [py2many](http://github.com/py2many/py2many) forward
* Allows transpilation to compiled languages
* Could use multiple-dispatch where supported (Julia)
* Help other similar projects in the python ecosystem that want to innovate

Targeting top 100 most used stdlib functions, heavily assisted by LLMs (both for identifying and
reimplementing)
