# -*- mode: python -*-

block_cipher = None

import germaniumdrivers

datas = [
    (germaniumdrivers.ensure_driver('chrome'), r'germaniumdrivers\binary\chrome\win\32\chromedriver.exe', 'DATA'),
    (germaniumdrivers.ensure_driver('ie'), r'germaniumdrivers\binary\ie\win\32\IEDriverServer.exe', 'DATA')
]

a = Analysis(['germaniumsb/main.py'],
             pathex=['./germaniumsb'],
             binaries=[],
             datas=datas,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='main',
          debug=False,
          strip=False,
          upx=True,
          console=True, )

#coll = COLLECT(exe,
#               a.binaries,
#               a.zipfiles,
#               a.datas,
#               strip=False,
#               upx=True,
#               name='main')

