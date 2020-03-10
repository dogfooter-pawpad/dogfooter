# -*- mode: python -*-

block_cipher = None

a = Analysis(['main.py'],
             pathex=['D:\\dogfooter'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

a.datas += [ ('sample.lyb', '.\\sample.lyb', 'DATA')]
a.datas += [ ('.\\images\\t_logo.png', '.\\images\\t_logo.png', 'DATA')]
a.datas += [ ('.\\images\\dogfooterbot_icon.ico', '.\\images\\dogfooterbot_icon.ico', 'DATA')]
a.datas += [ ('.\\host', '.\\host', 'DATA')]

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='dogfooter',
          debug=False,
          strip=False,
          upx=True,
          console=False, icon='.\\images\\dogfooterbot_icon.ico' )

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='dogfooter')
