# Implement python stdlib in statically typed python using FFI

This avoids C-API and breaks compatibility with CPython. But it has some benefits:

* Moves [py2many](http://github.com/py2many/py2many) forward
* Allows transpilation to compiled languages
* Could use function overloading 
  * `listdir(path: str) -> List[str]`
  * `listdir(path: pathlib.Path) -> List[pathlib.Path]`
* Help other similar projects in the python ecosystem that want to innovate

Targeting top 100 most used stdlib functions, heavily assisted by LLMs (both for identifying and
reimplementing)
