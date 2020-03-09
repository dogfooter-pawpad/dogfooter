# -*- mode: python -*-

block_cipher = None

a = Analysis(['dogfootermacro.py'],
             pathex=['C:\\workspace\\dogfooter'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

a.datas += [ ('dogfootermacro.ui', '.\\dogfootermacro.ui', 'DATA')]
a.datas += [ ('.\\image\\dogfootermacro_icon.png', '.\\dogfootermacro_icon.png', 'DATA')]

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='dogfootermacro',
          debug=False,
          strip=False,
          upx=True,
          console=False)
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='dogfootermacro')
