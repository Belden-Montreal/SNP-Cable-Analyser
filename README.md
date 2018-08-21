# SNP-Cable-Analyser

# Coding Style

The code should follow as much as possible the [PEP 8](https://www.python.org/dev/peps/pep-0008/) coding style, that is

* we use spaces and not tabs
* python modules (filenames) should have _short_, _all lowercase_ names and may contain underscores
* python packages (directories) should have _short_, _all lowercase_ names and preferably without underscores
* classes names should follow the _CapWords_ convention

We diverge from the [standard](https://www.python.org/dev/peps/pep-0008/#id45) for the variable and function names. These names should follow the _camelCase_ convention.

Classes should try to encapsulate their members and methods as much as possible, that is

* `self.name` for a public member/method
* `self._name` for a protected member/method
* `self.__name` for a private member/method
