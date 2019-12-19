# XTB Encoder
xtbenc is a gui for ffmpeg. It combines the beauty of GUI with the power of commandline for geeks!

![Options](images/xtbenc-01.png)

# Resources
Warning - tkinter + Python 3.7.3 and later, including 3.8 has problems. Python 3.6 is the recommended version for PySimpleGUI. In Ubuntu if you get an error similar to: ImportError: No module named tkinter then you need to install tkinter.
```
python3 -m pip install pysimplegui
sudo apt install python3-tk

pyinstaller --add-data="presets:presets" xtbenc.py # Ubuntu
pyinstaller --windowed --icon=xtbenc.ico --add-data="presets;presets" xtbenc.py # Windows
```

# Usage
ffmpeg.exe and ffprobe.exe should be in env path or drop your static binaries in the same folder as xtbenc. ffmpeg arguments can be typed in directly in the "Extra Options" combo or permanently added by editing the csv files in the presets folder.

[Releases](https://github.com/rmkimathi/xtbenc/releases)

# Reference
[PySimpleGUI](https://github.com/PySimpleGUI/PySimpleGUI)

[Shlex](https://docs.python.org/3.6/library/shlex.html)

[Subprocess](https://docs.python.org/3.6/library/subprocess.html)

[CSV](https://docs.python.org/3.6/library/csv.html)

[Live loop](https://github.com/fabianlee/blogcode/tree/master/python)
