# -*- mode: python -*-
a = Analysis(['D:\\Projects2\\novelty_assistant\\novelty_assistant.py'])
pyz = PYZ(a.pure)
exe = EXE( pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name=os.path.join('D:\\Projects2\\build_novelty_assistant', 'Novelty Assistant.exe'),
		  icon='D:\\Projects2\\novelty_assistant\\img\\ico\\main_64.ico',
          debug=False,
          strip=False,
          upx=True,
          console=False )
