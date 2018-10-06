# -*- mode: python -*-

block_cipher = None

import os
import germaniumdrivers

import germanium


ALLOWED_EXTENSIONS=['.js', '.html', '.png', '.chm', '.ico']


def add_module(m, module_name):
    for module_path in m.__path__:
        add_files(module_path, module_name)


def add_files(module_path, module_name):
    for root, dirs, files in os.walk(module_path):
        for name in files:
            _, file_extension = os.path.splitext(name)

            if file_extension not in ALLOWED_EXTENSIONS:
                continue

            full_path = os.path.join(root, name)
            #print(full_path)
            datas.append( (full_path, os.path.join(module_name + root[len(module_path):]) ) )


datas = [
    ('js/main.js', 'js'),
    (germaniumdrivers.ensure_driver('chrome'), r'germaniumdrivers\binary\chrome\win\32'),
    (germaniumdrivers.ensure_driver('ie'), r'germaniumdrivers\binary\ie\win\32'),
    (germaniumdrivers.ensure_driver('firefox'), r'germaniumdrivers\binary\firefox\win\64')
]

add_module(germanium, "germanium")
add_files("germaniumsb", "germaniumsb")

def add_files(m):
    for root, dirs, files in os.walk(m.__path__):
        for name in files:
            full_path = os.path.join(root, name)

a = Analysis(['germaniumsb/mainapp.py'],
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
          console=True,
          icon='germaniumsb/favicon.ico',
)

