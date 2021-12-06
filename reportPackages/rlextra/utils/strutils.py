'''utilities to aid string processing'''
__all__ = (
        'autoDecode',
        )
import codecs
bom_map = {
            codecs.BOM_UTF8: 'utf8',
            codecs.BOM_UTF16: 'utf_16',
            codecs.BOM_UTF16_BE: 'utf_16_be',
            codecs.BOM_UTF16_LE: 'utf_16_le',
            codecs.BOM_UTF32: 'utf_32',
            codecs.BOM_UTF32_BE: 'utf_32_be',
            codecs.BOM_UTF32_LE: 'utf_32_le',
            }
def autoDecode(s,encodings=('utf8','latin1','ascii'), fallback='ascii'):
    '''try to decode using one of the specified encodings'''
    if isinstance(s,str): return s
    if not isinstance(s,bytes):
        raise TypeError('autoDecode first argument has wrong type %r' % type(s))
    for bom, enc in bom_map.items():
        if s.startswith(bom):
            return s[len(bom):].decode(enc)
    for enc in encodings:
        try:
            return s.decode(enc)
        except UnicodeDecodeError:
            pass
    if fallback:
        return s.decode(fallback,'ignore')
    raise ValueError('autoDecode cannot decode bytes starting with %r' % s[:20])
