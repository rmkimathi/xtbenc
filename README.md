# XTB Encoder
xtbenc is a gui for ffmpeg. It combines the beauty of GUI with the power of commandline for geeks!

![Options](images/xtbenc-01.png)

# Resources
Warning - tkinter + Python 3.7.3 and later, including 3.8 has problems. Python 3.6 is the recommended version for PySimpleGUI. In Ubuntu if you get an error similar to: ImportError: No module named tkinter then you need to install tkinter.
```
python3 -m pip install pysimplegui
sudo apt install python3-tk
```

# Usage
ffmpeg.exe and ffprobe.exe should be in env path or drop your static binaries in the same folder as xtbenc. Additional arguments can be added by editting the csv files in the presets folder.

# Reference
(https://github.com/PySimpleGUI/PySimpleGUI)

(https://docs.python.org/3.6/library/shlex.html)

(https://docs.python.org/3.6/library/subprocess.html)

(https://docs.python.org/3.6/library/csv.html)

(https://github.com/fabianlee/blogcode/tree/master/python)
