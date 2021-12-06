__all__ = ('svg2rlg',)
__svg2rlg__ = None
def svg2rlg(path, resolve_entities=False, **kwds):
    global __svg2rlg__
    if not __svg2rlg__:
        try:
            from svglib.svglib import svg2rlg as __svg2rlg__
        except ImportError:
            raise RuntimeError('Cannot import svglib.svglib.svg2rlg, perhaps you need to install svglib')
    return __svg2rlg__(path, resolve_entities, **kwds)

def main():
    import glob, traceback, sys, os, logging
    from reportlab.lib.boxstuff import aspectRatioFix
    from svglib.svglib import logger

    argv = sys.argv[1:]
    outDir = os.getcwd()
    formats = ['pdf']
    autoSize = False
    verbose = logging.CRITICAL
    handling = False
    for arg in argv:
        if arg.startswith('--outdir='):
            outDir = arg[9:]
            if not os.path.isabs(outDir):
                outDir = os.path.abspath(outDir)
            continue
        elif arg.startswith('--formats='):
            formats = [_.strip() for _ in arg[10:].split(',')]
            continue
        elif arg.startswith('--verbose='):
            verbose = max(int(arg[10:]),logging.CRITICAL)
            continue
        elif arg=='--verbose':
            verbose = logging.DEBUG
            continue
        elif arg=='--autoSize':
            autoSize = True
            continue
        elif arg.startswith('--'):
            raise ValueError('unknown option %r' % arg)
        if verbose!=None:
            if not handling:
                logger.addHandler(logging.StreamHandler(sys.stdout))
                handling = True
            logger.setLevel(verbose)
        for fn in glob.glob(arg):
            try:
                d = svg2rlg(fn)
                if d:
                    if autoSize:
                        preserveAspectRatio = False
                        anchor = 'sw'
                        width = float(d.width)
                        height = float(d.height)
                        x0,y0,x1,y1 = d.getBounds()
                        wo = x1 - x0
                        ho = y1 - y0
                        xn,yn,wn,hn,scaled = aspectRatioFix(preserveAspectRatio,anchor,0,0,width,height,wo,ho)
                        sx = wn/d.width
                        sy = hn/d.height
                        d.transform = [sx,0,0,sy,-sx*x0,-sy*y0]
                        d.width = wn
                        d.height = hn
                    fnRoot=os.path.splitext(os.path.basename(fn))[0]
                    d.save(formats=formats,verbose=verbose,fnRoot=fnRoot,outDir=outDir)
            except:
                traceback.print_exc()

if __name__=='__main__':
    main()
