#copyright ReportLab Inc. 2000-2019
#see license.txt for license details
Version='3.6.3'

__version__=Version
__date__='20211118'
import sys

if sys.version_info<(3, 6):
    raise ImportError("""reportPackages.rlextra requires Python 3.6+; 3.0-3.5 are not supported.
If you want to try with other python versions edit line 10 of reportPackages.rlextra/__init__
to remove this error.""")

import reportlab

if tuple(map(int, (reportlab.Version.split("."))))[:3] < tuple(map(int, (Version.split("."))))[:3]:
	raise ImportError("""reportPackages.rlextra version %s requires at least reportlab %s, and you have reportlab %s; it is strongly recommended that you use the same versions""" % (Version,
		(Version if Version.count('.')==2 else Version.rsplit('.',1)[0]),
		reportlab.Version))
