# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['C:\\Users\\PC\\Documents\\Descargas chrome\\NO TOCAR MALDITO IDIOTA!! ZZZZ\\kleiver\\Tesis\\Nueva tesis\\LaboratorioDeControl\\Main aplication'],
             binaries=[],
             datas=[('icono.ico', '.'), ('Esquemas', 'Esquemas')],
             hiddenimports=['qtconsole.client'],
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
          name='main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True , icon='icono.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='main')
