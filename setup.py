import sys
import os
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = dict(packages=["tkinter", "numpy", "bs4", "nltk", "PIL", "multiprocessing", 'gtts', 'playsound'
    , 'idna'],
                         includes=["multiprocessing.pool"],
                         include_files=["idf_en.txt", "stopwords_en.txt", "bbc_2.png",
                                        "nytimes_2.png", 'wapo_2.png', 'reuters.png',
                                        'guardian.png', 'apnews.png', 'newsweek.png', 'politico.png',
                                        'npr.png', 'latimes.png', 'huffpost.png', 'verge.png', 'texture.jpg',
                                        'tcl86t.dll', 'tk86t.dll', 'nltk_data/', 'vi.pickle',
                                        'config.py', 'frontpage.py', 'grabheadline.py', 'keyword_interface.py',
                                        'keyword_search.py', 'lxrTest.py', 'rake.py', 'sf.py', 'speaker_icon.png'],
                         excludes=['matplotlib', 'gensim', 'keras', 'sklearn', 'scipy', 'underthesea'])

os.environ['TCL_LIBRARY'] = "C:/Users/CUONG/AppData/Local/Programs/Python/Python36-32/tcl/tcl8.6"
os.environ['TK_LIBRARY'] = "C:/Users/CUONG/AppData/Local/Programs/Python/Python36-32/tcl/tk8.6"

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="QNews",
    version="0.2.0",
    description="QNEWS",
    options={"build_exe": build_exe_options},
    executables=[Executable("gui_30.py", base=base, icon='app.ico')])
