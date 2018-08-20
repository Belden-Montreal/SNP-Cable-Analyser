from jinja2 import Template, Environment, FileSystemLoader, StrictUndefined
from os.path import abspath

def normalize(name):
    return name.lower().replace(' ', '-')

def latex(name):
    return name.replace('_', '\\_')

class DocumentObject(object):
    def __init__(self, prefix):
        # create prefix directory if it doesn't exist
        self._prefix = prefix
        self._prefix.mkdir(exist_ok=True, parents=True)
 
        # get the filename
        self._basename  = self.getBasename()
        self._extension = ".tex"
        self._filename  = self._basename+self._extension

        # create the path to this document object
        self._path = self._prefix.joinpath(self._filename)

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
        self._content = self._template.render(self.getTemplateArguments())

        # write the file
        with open(self.getFilePath(), "w") as output:
            output.write(self._content)

    def getPrefix(self):
        return self._prefix

    def getFilePath(self):
        return self._path

    def getBasename(self):
        raise NotImplementedError

    def getTemplateName(self):
        raise NotImplementedError

    def getTemplateArguments(self):
        raise NotImplementedError
