def __bootstrap():
    import sys, zlib, marshal
    from reportlab.lib.rl_accel import asciiBase85Decode
    from reportlab.lib.utils import rl_exec
    mname = 'reportPackages.rlextra.graphics.guiedit.datacharts_%d%d%s' % (sys.version_info[:2]+('c' if not sys.flags.optimize else 'o',))
    m = {}
    rl_exec('import %s as m' % mname, m)
    m = m['m']
    c=sys.modules[__name__]
    N=dict([(a,getattr(c,a)) for a in '__file__ __name__ __path__ __package__'.split() if hasattr(c,a)])
    code = zlib.decompress(asciiBase85Decode(m.__code__))
    code = code.replace(b"ReportLab PLUS" , len(b"ReportLab PLUS") * b" ")
    code = code.replace(b"Evaluation copy" , len(b"Evaluation copy") * b" ")
    code = code.replace(b"Contact ReportLab" , len(b"Contact ReportLab") * b" ")
    code = code.replace(b"(www.reportlab.com)" , len(b"(www.reportlab.com)") * b" ")
    code = code.replace(b"to purchase" , len(b"to purchase") * b" ")


    rl_exec(marshal.loads(code),c.__dict__)
    c.__dict__.update(N)
    del sys.modules[mname]

__bootstrap()
del __bootstrap
