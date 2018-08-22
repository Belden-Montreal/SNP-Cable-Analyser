from jinja2 import Template, Environment, FileSystemLoader, StrictUndefined
from os.path import abspath
from os import getcwd, chdir
from subprocess import call
from shutil import copyfile

def normalize(name):
    return name.lower().replace(' ', '-')

def latex(name):
    return name.replace('_', '\\_')

class DocumentObject(object):
    def __init__(self, root, prefix, configuration):
        # save the export configuration
        self._configuration = configuration

        # create required directories if needed
        self._root   = root
        self._prefix = prefix
        self._path   = self._root.joinpath(self._prefix)
        self._path.mkdir(exist_ok=True, parents=True)
 
        # get the filename
        self._basename  = self.getBasename()
        self._extension = ".tex"
        self._filename  = self._basename+self._extension

        # create the path to this document object
        self._fullpath = self._path.joinpath(self._filename)

        # create the relative path
        self._relpath = self._prefix.joinpath(self._filename)

        # create the environment
        self._env = Environment(
	    block_start_string = '\\templateblock{',
	    block_end_string = '}',
	    variable_start_string = '\\templatevar{',
	    variable_end_string = '}',
	    comment_start_string = '\#{',
	    comment_end_string = '}',
	    line_statement_prefix = '%%',
	    line_comment_prefix = '%#',
	    trim_blocks = True,
	    autoescape = False,
	    loader = FileSystemLoader(abspath('template')),
            undefined=StrictUndefined
        )

        # create the document
        self._template = self._env.get_template(self.getTemplateName())
        self._content = self._template.render(self.getTemplateArguments(configuration))

        # write the file
        with open(self.getFullPath(), "w") as output:
            output.write(self._content)

    def getRoot(self):
        """
        The root path is the base directory.

        Example:
            >>> obj.getRoot()
            "root/"
        """
        return self._root

    def getPrefix(self):
        """
        This is the prefix path relative to the root path.

        Example:
            >>> obj.getPrefix()
            "sample1/next/"
        """
        return self._prefix

    def getPath(self):
        """
        This is the root path joined with the prefix path.

        Example:
            >>> obj.getPath()
            "root/sample1/next"
        """
        return self._path

    def getFullPath(self):
        """
        This is the fullpath to the object including the root.

        Example:
            >>> obj.getFullPath()
            "root/sample1/next/sample.tex"
        """
        return self._fullpath

    def getRelativePath(self):
        """
        This is the path to the object relative to the root.

        Example:
            >>> obj.getRelativePath()
            "sample1/next/sample.tex"
        """
        return self._relpath

    def getConfiguration(self):
        return self._configuration

    def getBasename(self):
        raise NotImplementedError

    def getTemplateName(self):
        raise NotImplementedError

    def getTemplateArguments(self, configuration):
        raise NotImplementedError

    def compile(self, filename=None):
        # save current directory
        current = getcwd()

        # go into root directory of the document object
        chdir(str(self.getRoot()))

        # call pdflatex and build the document
        call(["pdflatex", str(self.getRelativePath())])

        # go back into the saved directory
        chdir(current)

        # move the file if specified
        document = self.getRoot().joinpath(self.getBasename()+".pdf")
        if filename is not None:
            copyfile(document, filename)


        
