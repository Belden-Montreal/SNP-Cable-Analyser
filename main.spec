# -*- mode: python -*-

block_cipher = None

added_files = [
        ('C:/Users/cedryk/AppData/Local/Programs/Python/Python37/Lib/site-packages/skrf/data/*.s*p', 'skrf/data/'),
        ('C:/Users/cedryk/Documents/SNP-Cable-Analyser/limits/limits.xml', 'limits/'),
]

a = Analysis(['main.py'],
             pathex=['C:\\Users\\cedryk\\Documents\\SNP-Cable-Analyser'],
             binaries=[],
             datas=added_files,
             hiddenimports=["skrf", "matplotlib.backends.backend_tkagg"],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='SNPAnalyzer',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='main')
