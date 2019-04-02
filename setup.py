import sys
import os
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = dict(packages=["tkinter", "numpy", "bs4", "nltk", "PIL", "multiprocessing"],
                         includes=["multiprocessing.pool"],
                         include_files=["lxrTest.py", "frontpage.py", "grabheadline.py", "idf_vi.txt",
                                        "idf_en.txt", "keyword_interface.py", "keyword_search.py", "keywords_gui.py",
                                        "lexy.py", "rake.py",
                                        "sf.py", "sfk.py", "stopwords_en.txt", "vi.pickle", "./imgs/bbc_2.jpg",
                                        "./imgs/nytimes_2.jpg", './imgs/wapo_2.jpg', './imgs/reuters.png',
                                        './imgs/guardian.png', './imgs/apnews.png', 'tcl86t.dll', 'tk86t.dll',
                                        'nltk_data/'],
                         excludes=['matplotlib', 'gensim', 'keras', 'sklearn', 'scipy'])

os.environ['TCL_LIBRARY'] = "C:/Users/CUONG/AppData/Local/Programs/Python/Python36-32/tcl/tcl8.6"
os.environ['TK_LIBRARY'] = "C:/Users/CUONG/AppData/Local/Programs/Python/Python36-32/tcl/tk8.6"

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="QNews",
    version="0.1.1",
    description="Summarize the News for you",
    options={"build_exe": build_exe_options},
    executables=[Executable("gui_30.py", base=base, icon='xyz.ico')])
