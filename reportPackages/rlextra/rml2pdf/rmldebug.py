__all__ = ()    #everything should be expolicitly imported
class RmlDebug(object):
    '''
    Horrible hacky code to debug rml2pdf; when setup_debug is called it looks at
    the globals dict it is given and messes with a bunch of klasses to get them
    to annotate their instances with suitable information from the parse.

    At the end of setup_debug the sys exception hook is overridden and the old one
    returned so the class can store it.

    When called without a dict the cleanup action is performed if needed.
    '''
    @staticmethod
    def setup_debug(G):
        Controller = G['Controller']
        MapController = G['MapController']
        Flowable = G['Flowable']
        DeferredInitialization = G['DeferredInitialization']
        import sys, inspect
        from reportPackages.reportlab.lib.utils import flatten
        from reportPackages.reportlab.lib.rl_accel import fp_str
        from reportPackages.reportlab.platypus.tables import Table
        isclass = inspect.isclass
        hacked_klasses = {}
        def get_nodemappers(L):
            aL = L.append
            for v in Controller.nodemappers.values():
                v = getattr(v,'__class__',None)
                if v and isclass(v):
                    aL(v)
            return L

        class TagAndObj(tuple): #tag with a name
            def __new__(cls, v, obj):
                t = tuple.__new__(cls,v)
                t.__obj = obj
                return t
            @property
            def obj(self):
                return self.__obj
            @property
            def name(self):
                obj = self.__obj
                try:
                    return obj.__name__
                except AttributeError:
                    try:
                        return obj.__class__.__name__
                    except:
                        return ''

        def get_klasses(L, target_klasses = Flowable):
            aL = L.append
            for v in G.values():
                if isclass(v) and issubclass(v, target_klasses):
                    aL(v)
            return L

        def make_init(klass):
            def __init__(self,*args,**kwds):
                init_annotation(self)
                klass.__rml2pdf_old_init__(self,*args,**kwds)
            return __init__

        class FuncWrap:
            '''make a callable from a function; instances can be annotated'''
            def __init__(self, func):
                self.func = func
            def __call__(self, *args, **kwds):
                return self.func(*args,**kwds)

        def best_tag(tag,tagr):
            if tagr is None:
                tagr = tag
            else:
                t = tag[3][0][1:]
                tr = tagr[3][0][1:]
                if t>=tr: tagr = tag
            return tagr

        def set_best_tag(tag, r, func=False):
            if hasattr(r,'__dict__') and (r.__class__.__name__ in hacked_klasses or func):
                r.__dict__['__rml2pdf_tag_annotation__'] = best_tag(tag, r.__dict__.get('__rml2pdf_tag_annotation__',None))
            else:
                if isinstance(r,list):
                    for r1 in r:
                        set_best_tag(tag,r1)
                #elif callable(r):
                #   r = FuncWrap(r)
                #   r.__dict__['__rml2pdf_tag_annotation__'] = tag
            return r

        def whereFromSeq(v):
            if v:
                v = flatten(v)
                tag0 = next((_ for _ in v if hasattr(_,'__rml2pdf_tag_annotation__')),None)
                if not tag0: return
                tag0 = tag0.__rml2pdf_tag_annotation__[3]
                if len(v)==1:
                    return tag0
                else:
                    tagn = next((_ for _ in reversed(v) if hasattr(_,'__rml2pdf_tag_annotation__')),None)
                    if not tagn: return tag0
                    tagn = tagn.__rml2pdf_tag_annotation__[3]
                    if tagn is tag0: return tag0
                    t0 = (tag0[1] or tag0[2]) if tag0 else None
                    tn = (tagn[2] or tagn[1]) if tagn else None
                    return (tag0[0],t0,tn)

        def make_initialize(klass):
            def initialize(self,*args,**kwds):
                r = klass.__rml2pdf_old_initialize__(self,*args,**kwds)
                tag = self.__dict__.get('__rml2pdf_tag_annotation__',None)
                if tag:
                    set_best_tag(tag,r)
                else:
                    init_annotation(r)
                return r
            return initialize

        def make_evaluate(klass):
            def evaluate(self, tagname, sdict, pcontent, extra, context, *args, **kwds):
                r = klass.__rml2pdf_old_evaluate__(self, tagname, sdict, pcontent, extra, context, *args,**kwds)
                tag = self.__dict__.get('__rml2pdf_tag_annotation__',None)
                if not tag:
                    tag = (tagname, sdict, None, extra)
                set_best_tag(tag,self)
                return set_best_tag(tag,r,True)
            return evaluate

        def make_processTuple(klass):
            def processTuple(self, e, *args, **kwds):
                self.__rml2pdf_tuple_stack__.append(e)
                r = klass.__rml2pdf_old_processTuple__(self, e, *args,**kwds)
                self.__rml2pdf_tuple_stack__.pop()
                return r
            return processTuple

        def make_tableSplit(klass):
            def split(self, *args, **kwds):
                r = klass.__rml2pdf_old_split__(self, *args,**kwds)
                if r:
                    T0, T1 = r
                    T1.__rml_initial_row__ = T0._nrows+getattr(T0,'__rml_initial_row__',0)
                return r
            return split

        def setup():
            for v in get_nodemappers(
                            get_klasses([],
                                target_klasses=(Flowable,DeferredInitialization))):
                k = v.__name__
                if k in hacked_klasses: continue
                invdict = lambda m: m in v.__dict__
                if invdict('__init__') and not invdict('__rml2pdf_old_init__'):
                    v.__rml2pdf_old_init__ = v.__init__
                    v.__init__ = make_init(v)
                if invdict('initialize') and not invdict('__rml2pdf_old_initialize__'):
                    v.__rml2pdf_old_initialize__ = v.initialize
                    v.initialize = make_initialize(v)
                if invdict('evaluate'):
                    v.__rml2pdf_old_evaluate__ = v.evaluate
                    v.evaluate = make_evaluate(v)

                hacked_klasses[k] = v
                
            MapController.__rml2pdf_tuple_stack__ = []
            MapController.__rml2pdf_old_processTuple__ = MapController.processTuple
            MapController.processTuple = make_processTuple(MapController)
            Table.__rml2pdf_old_split__ = Table.split
            Table.split = make_tableSplit(Table)
            old_hook = sys.excepthook
            sys.excepthook = process_exception
            return old_hook

        def find_annotation(F, deep=False):
            if MapController.__rml2pdf_tuple_stack__:
                return MapController.__rml2pdf_tuple_stack__[-1]
            tag = None
            for frame, fn, lnum, func, lines, index in F:
                f_locals = frame.f_locals
                self = f_locals.get('self', None)
                if self is not None:
                    tag1 = self.__dict__.get('__rml2pdf_tag_annotation__',None)
                    if tag1:
                        tag1 = TagAndObj(tag1,self)
                        tag = best_tag(tag1,tag)
                    if 'rml2pdf' in fn and self.__class__.__name__=='CanvasOps':
                        obj = f_locals.get('op',None)
                        if obj  is not None and hasattr(obj,'__dict__'):
                            tag1 = obj.__dict__.get('__rml2pdf_tag_annotation__',None)
                            if tag1:
                                tag1 = TagAndObj(tag1,obj)
                                tag = best_tag(tag1,tag)

                if 'doctemplate' in fn and func=='handle_flowable':
                    obj = f_locals.get('f',None)
                    if obj is not None:
                        tag1 = obj.__dict__.get('__rml2pdf_tag_annotation__',None)
                        if tag1:
                            tag1 = TagAndObj(tag1,obj)
                            tag = best_tag(tag1,tag)
                if tag and not deep: return tag
            return tag

        def init_annotation(self):
            tag = find_annotation(inspect.stack(1))
            if tag: set_best_tag(tag,self)

        def whereFormat(where):
            if where:
                if where[1] is None:
                    where = ' @ %d:%d' % (where[0][1]+1,where[0][2])
                else:
                    where = ' @ %d:%d - %d:%d' % (where[0][1]+1,where[0][2],where[1][1]+1,where[1][2])
            else:
                where = ''
            return where

        def tag_format(ttag):
            tag, attrs, content, where = ttag
            b = '\n!!!!! ' + (len(tag)+2)*'\x20'
            if attrs:
                attrs = b + b.join(('%s=%r' % (k,v) for k,v in sorted(attrs.items())))
            else:
                attrs = ''
            haveObj = isinstance(ttag,TagAndObj)
            objName = ttag.name if haveObj else ''
            if objName: objName = ' (%s)' % objName
            xtra = [].append
            if haveObj:
                if isinstance(ttag.obj,Table):
                    irow = getattr(ttag.obj,'__rml_initial_row__',0)
                    rowH = [(h,i) for i,h in enumerate(ttag.obj._rowHeights) if h is not None and h>0]
                    rowH.sort(reverse=True)
                    if rowH:
                        xtra(b+'largest row heights = [%s]'
                                % ', '.join(('|%d|=%s%s' % (irow+i+1,fp_str(h),whereFormat(whereFromSeq(ttag.obj._cellvalues[i]))) for h,i in rowH[:5])))
            xtra = xtra.__self__
            if xtra: xtra = '\n'.join(xtra)
            return '\n!!!!! <%s%s>%s%s%s' % (tag, attrs, objName, whereFormat(where), xtra)

        def process_exception(t,v,s):
            sys.__excepthook__(t,v,s)
            tag = find_annotation(tuple(reversed(inspect.getinnerframes(s, 1))), deep=True)
            if tag:
                sys.stderr.write('!!!!! tag leading to the problem was%s\n' % tag_format(tag))

        def cleanup(old_hook):
            sys.excepthook = old_hook
            MapController.processTuple = MapController.__rml2pdf_old_processTuple__
            del MapController.__rml2pdf_old_processTuple__
            del MapController.__rml2pdf_tuple_stack__
            Table.split = Table.__rml2pdf_old_split__
            del Table.__rml2pdf_old_split__
            for name, klass in hacked_klasses.items():
                if '__rml2pdf_old_init__' in klass.__dict__:
                    klass.__init__ = klass.__rml2pdf_old_init__
                    del klass.__rml2pdf_old_init__
                if '__rml2pdf_old_initialize__' in klass.__dict__:
                    klass.initialize = klass.__rml2pdf_old_initialize__
                    del klass.__rml2pdf_old_initialize__
                if '__rml2pdf_old_evaluate__' in klass.__dict__:
                    klass.evaluate = klass.__rml2pdf_old_evaluate__
                    del klass.__rml2pdf_old_evaluate__
            hacked_klasses.clear()

        return setup, cleanup

    __internals = []

    @classmethod
    def __call__(cls,G):
        if G and not cls.__internals:
            setup, cleanup = cls.setup_debug(G)
            old_hook = setup()
            cls.__internals.append((cleanup,old_hook))
        elif cls.__internals:
            cleanup,old_hook = cls.__internals.pop()
            cleanup(old_hook)

RmlDebug = RmlDebug()
