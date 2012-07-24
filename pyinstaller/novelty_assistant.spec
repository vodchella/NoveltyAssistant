# -*- mode: python -*-
a = Analysis([os.path.join(HOMEPATH,'support\\_mountzlib.py'), os.path.join(HOMEPATH,'support\\useUnicode.py'), 'D:\\Twister\\Dropbox\\novelty_assistant\\novelty_assistant.py'],
             pathex=['D:\\Twister\\python\\pyinstaller'])
pyz = PYZ(a.pure)
exe = EXE( pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name=os.path.join('D:\\Projects\\build_novelty_assistant', 'Novelty Assistant.exe'),
		  icon='D:\\Projects\\novelty_assistant\\img\\ico\\main_64.ico',
          debug=False,
          strip=False,
          upx=True,
          console=False )
