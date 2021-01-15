# -*- mode: python -*-

block_cipher = None
user = 'User'


a = Analysis(
    ['__main__.py'],
    pathex=[f'C:\\Users\\{user}\\Desktop\\Proxier'],
    binaries=[],
    datas=[
        ('proxier/utils/GeoIP.mmdb', 'proxier/utils/'), 
        ('proxier/gui/mainwindow.ui', 'proxier/gui/'),
        ('proxier/gui/resource.qrc', 'proxier/gui/'),
        ('proxier/assets/*', 'proxier/assets/'),
        ('proxier/assets/sound/*', 'proxier/assets/sound/'),
        ('proxier/assets/ico/*', 'proxier/assets/ico/')
    ],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
    a.scripts,
    [],
    icon='proxier/assets/favicon.ico',
    exclude_binaries=True,
    name='Proxier',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name='Proxier'
)

