# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['C:\\Users\\PC\\Documents\\Descargas chrome\\NO TOCAR MALDITO IDIOTA!! ZZZZ\\kleiver\\Tesis\\Nueva tesis\\LaboratorioDeControl\\Main aplication'],
             binaries=[],
             datas=[],
             hiddenimports=['shiboken2'],
             hookspath=['hooks'],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

a.datas += [('icono.ico','C:\\Users\\PC\\Documents\\Descargas chrome\\NO TOCAR MALDITO IDIOTA!! ZZZZ\\kleiver\\Tesis\\Nueva tesis\\LaboratorioDeControl\\Main aplication\\icono.ico', 'Data')]

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True , icon='icono.ico')