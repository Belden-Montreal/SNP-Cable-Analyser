"mymodule.py implements example plug-in functionality for rml2pdf"
from reportlab.lib.utils import safer_globals,  pickle, base64_encodebytes, asNative, isStr
from reportlab.pdfbase.pdfmetrics import stringWidth, getAscentDescent
from reportlab.lib.colors import toColor

# <plugInGraphic module="mymodule" function="myfunction">example data</plugInGraphic>

def myfunction(canv, data):
    print("myfunction", (canv, data))
    canv.line(0,0, 100, 100)

# <plugInFlowable module="mymodule" function="myFlowable">this data</plugInFlowable>

# note: this is wrapped in a "real" flowable so it doesn't need to inherit from platypus.Flowable
class myFlowable:
    def __init__(self, data=''):
        print("myFlowable init", data)
    def wrap(self, w, h):
        print("myFlowable wrap", w, h)
        self.width = w
        self.height = h
        return (0,0)
    def draw(self):
        canv = self.canv
        canv.saveState()
        canv.setFillColorRGB(1,0,0)
        canv.rect(0,0,self.width,self.height,fill=1,stroke=0)
        self.canv.line(0,0,100,0)
        canv.restoreState()
        print("myFlowable drew a line", (0,0,100,0))

from reportlab.platypus.xpreformatted import XPreformatted
from reportlab.platypus.flowables import Flowable
from reportlab.lib.styles import getSampleStyleSheet
class myPreformatted(XPreformatted):
    """This is used by test_009_splitting under the test directory. It
    has been placed here to make sure that it is available in any
    standard installation of RML."""
    def __init__(self, text=None, style=getSampleStyleSheet()["Normal"],bulletText = None, dedent=0, frags=None):
        if text is None: text = """This page tests splitting - this is a pluginFlowable from
mymodule.py, using XPreformatted a reportlab style 'Normal' . It
should split between the two frames on this page. These frames should
be ON A NEW PAGE, otherwise this test has FAILED. This page tests
splitting - this XPreformatted should split between the two frames on
this page. This page tests splitting - this XPreformatted should split
between the two frames on this page. This page tests splitting - this
XPreformatted should split between the two frames on this page. This
page tests splitting - this XPreformatted should split between the two
frames on this page."""
        XPreformatted.__init__(self,text,style,bulletText,frags,dedent)

class linkURL(Flowable):
    _fixedWidth = True

    def __init__(self, URL, text=None):
        self._URL = URL
        self._text = text or URL

    def wrap(self, w, h):
        c = self.canv
        fs = c._fontsize
        w = c.stringWidth(self._text,c._fontname,fs)
        self._width, self._height = w, 1.2*fs
        return (w,self._height)

    def __styledWrap__(self, style):
        fontName = getattr(style,'fontname',None)
        if fontName is None:
            fontName = style.fontName
        fontSize = getattr(style,'fontsize',None)
        if fontSize is None:
            fontSize = style.fontSize
        leading = getattr(style,'leading',1.2*fontSize)
        if fontSize is None:
            fontSize = style.fontSize
        L = asNative(self._text).split('\n')
        self._width = max([stringWidth(_, fontName, fontSize) for _ in L])
        self._height = len(L)*leading
        return self._width, self._height

    def draw(self):
        c = self.canv
        w, h = self._width, self._height
        c.drawString(0,h/6.,self._text)
        c.linkURL(self._URL,(0,0,w,h),relative=1,color=None,dashArray=None)

def _getArgs(*args,**kw):
    return args, kw

def _evalArgs(data):
    if data[0]!='(': data = '(%s)' % data
    return eval('_getArgs'+data,safer_globals())

def linkRect(canv,data):
    args, kw = _evalArgs(data)
    canv.linkRect(*args,**kw)

def bookmarkPage(canv,name):
    canv.bookmarkPage(name)

def _toColor(s):
    if s in ['','none','None',None]:
        return None
    try:
        return toColor(s)
    except:
        raise ValueError('Bad color value %r' % s)

def symbols(canv,data):
    '''
    produces filled symbols

    arguments
    n   number of points default 5
    x,y     initial symbol location
    dx      delta x for each new symbol
    dy      delta y for each symbol
    name    symbol name (suitable for makeMarker)
    fillColor   symbol fill colour
    strokeColor symbol stroke colour
    strokeWidth symbol stroke width
    angle   symbol angle
    '''
    args, kw = _evalArgs(data)
    if args:
        raise TypeError('Symbols takes no positional arguments')
    params = dict(
            n=5,
            x='72',
            y='72',
            dx='None',
            dy='0',
            name='StarFive',
            fillColor='yellow',
            strokeColor=None,
            strokeWidth='1',
            angle=0,
            )
    params.update(kw)

    from reportlab.graphics.shapes import Drawing
    from reportlab.graphics.widgets.markers import makeMarker
    from rlextra.rml2pdf.rml2pdf import readLengthOrNone

    name = params['name']
    n = int(params['n'])
    x0 = readLengthOrNone(params['x'])
    y0 = readLengthOrNone(params['y'])
    angle = float(params['angle'])
    size = readLengthOrNone(params['size'])
    strokeWidth = readLengthOrNone(params['strokeWidth'])
    dx = readLengthOrNone(params['dx'])
    if dx is None: dx = 2+1.5*size
    dy = readLengthOrNone(params['dy'])
    strokeColor = _toColor(params['strokeColor'])
    fillColor = _toColor(params['fillColor'])

    D = Drawing()
    for i in range(n):
        m = makeMarker(name)
        m.x = dx*i
        m.y = dy*i
        m.angle = angle
        m.size = size
        m.strokeWidth = strokeWidth
        m.strokeColor = strokeColor
        m.fillColor = fillColor
        D.add(m)

    D.drawOn(canv,x0,y0)

_Index=None
def getIndex(style=None, dot=None, tableStyle=None, indexClass=None, offset=0, format='123'):
    global _Index
    if not _Index:
        _Index = indexClass(style=style, dot=dot, tableStyle=tableStyle, offset=offset, format=format)
    return _Index

class IndexStarter(Flowable):
    def __init__(self, style=None, dot=None, tableStyle=None, indexClass='SimpleIndex', format='123', offset=0):
        self.style = style
        self.dot = dot
        self.tableStyle = tableStyle
        self.format = format
        self.offset = int(offset)

        def importFrom(mod, cls):
            return getattr(__import__(mod, globals(), locals(), [cls]), cls)

        try:
            self.indexClass = importFrom('reportlab.platypus.tableofcontents', indexClass)
        except (ImportError, AttributeError):
            mod, indexClass = indexClass.rsplit('.', 1)
            self.indexClass = importFrom(mod, indexClass)

    def wrap(self, w, h):
        rmlcontext = self._doctemplateAttr('_nameSpace')['rmlcontext']
        if rmlcontext:
            def checkStyle(s):
                try:
                    return rmlcontext.names[s]
                except KeyError:
                    raise KeyError('Style %s not found in IndexStarter.' % s)
            def getStyle(s,tAllowed=False):
                if not s: return None
                if tAllowed and isinstance(s,tuple):
                    return tuple(map(checkStyle,s))
                return checkStyle(s)
            style = getStyle(self.style,1)
            tableStyle = getStyle(self.tableStyle)
        _Index = getIndex(style, self.dot, tableStyle, self.indexClass, offset=self.offset,format=self.format)
        _Index.clearEntries()
        def _indexAdd(canv,kind,label):
            _Index(canv,kind,base64_encodebytes(pickle.dumps((label,None,None))).strip())
        self.canv._indexAdd=_indexAdd
        return 0,0

    def draw(self):
        pass

class IndexFinisher(Flowable):
    _init = True
    def __init__(self):
        if self._init:
            x = getIndex()
            self.__dict__ = x.__dict__
            self.__class__ = x.__class__
            self._init = False

class MyExpandingText(Flowable):
    def __init__(self, text='', fontName='Helvetica', maxFontSize=36, fontColor='black', fillColor=None,
                        strokeColor=None, strokeWidth=1, strokeDashArray=None,
                        leftPad=0, rightPad=0, topPad=0, bottomPad=0):
        self.text = text
        self.fontName = fontName
        self.maxFontSize = maxFontSize
        self.fontColor = _toColor(fontColor)
        self.fillColor = _toColor(fillColor)
        self.strokeColor = _toColor(strokeColor)
        self.strokeWidth = strokeWidth
        self.strokeDashArray = strokeDashArray
        self.leftPad = leftPad
        self.rightPad = rightPad
        self.topPad = topPad
        self.bottomPad = bottomPad


    def wrap(self, w, h):
        self.width = w
        fontSize = self.maxFontSize
        aW = w - self.leftPad - self.rightPad
        sw0 = stringWidth(self.text,self.fontName,self.maxFontSize)
        if sw0 > aW:
            fontSize *= float(aW)/sw0
        self.fontSize = fontSize
        ad = getAscentDescent(self.fontName,fontSize)
        self.height = self.topPad+self.bottomPad+ad[0]-ad[1]
        self._ascent = ad[0]
        self._descent = ad[1]
        return w, self.height

    def draw(self):
        canv = self.canv
        canv.saveState()
        sC = self.strokeColor
        fC = self.fillColor
        if sC is not None or fC is not None:
            if fC: canv.setFillColor(fC)
            if sC:
                canv.setStrokeColor(sC)
                canv.setLineWidth(self.strokeWidth)
                if self.strokeDashArray:
                    canv.setDash(self.strokeDashArray)
            canv.rect(0,0,self.width,self.height,fill=fC is not None,stroke=sC is not None)

        if self.fontColor:
            canv.setFillColor(self.fontColor)
        canv.setFont(self.fontName,self.fontSize)
        canv.drawCentredString(self.width*0.5,self.bottomPad-self._descent,self.text)
        canv.restoreState()

def _getLength(aL,l):
    try:
        if isStr(l):
            l = l.strip()
            if l.endswith('%'):
                return float(l[:-1])*0.01*aL
            else:
                return float(l)
    except:
        pass
    return aL

class MyTab(Flowable):
    def __init__(self, text='', fontName='Helvetica', fontSize=12, fontColor='white', fillColor='lightblue',
                        strokeColor=None, strokeWidth=1, strokeDashArray=None,
                        leftPad=0, rightPad=0, topPad=0, bottomPad=0, width=None, height=None, textDy=None):
        self.text = text
        self.fontName = fontName
        self.fontSize = fontSize
        self.fontColor = _toColor(fontColor)
        self.fillColor = _toColor(fillColor)
        self.strokeColor = _toColor(strokeColor)
        self.strokeWidth = strokeWidth
        self.strokeDashArray = strokeDashArray
        self.leftPad = leftPad
        self.rightPad = rightPad
        self.topPad = topPad
        self.bottomPad = bottomPad
        self._specHeight = height
        self._specWidth = width
        self.textDy = textDy

    def wrap(self, aW, aH):
        self._ascent, self._descent = getAscentDescent(self.fontName,self.fontSize)
        needHeight = self._ascent - self._descent + self.topPad + self.bottomPad
        needWidth = stringWidth(self.text,self.fontName,self.fontSize) + self.leftPad + self.rightPad + 0.5*needHeight
        specWidth = _getLength(aW,self._specWidth)
        self.width = needWidth if needWidth>specWidth else specWidth
        self.height = needHeight
        return self.width, self.height

    def draw(self):
        canv = self.canv
        canv.saveState()
        sC = self.strokeColor
        fC = self.fillColor
        h = self.height
        hh = h*0.5
        if sC is not None or fC is not None:
            if fC: canv.setFillColor(fC)
            if sC:
                canv.setStrokeColor(sC)
                canv.setLineWidth(self.strokeWidth)
                if self.strokeDashArray:
                    canv.setDash(self.strokeDashArray)
            w = self.width
            p = canv.beginPath()
            p.moveTo(0,0)
            p.lineTo(w,0)
            p.lineTo(w,hh)
            p.lineTo(w-hh,h)
            p.lineTo(0,h)
            p.close()
            canv.drawPath(p,fill=fC is not None,stroke=sC is not None)

        if self.fontColor:
            canv.setFillColor(self.fontColor)
        canv.setFont(self.fontName,self.fontSize)
        y = hh - 0.5*self._ascent-0.5*self._descent
        canv.drawString(self.leftPad,y+(self.textDy or 0),self.text)
        canv.restoreState()

def myTab(content):
    args, kwds = _evalArgs(content)
    return MyTab(*args,**kwds)
