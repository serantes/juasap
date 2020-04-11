# Juasap

**Juasap** is a Python3 script to browse Whatsapp web version simulating a desktop application thanks to Qt5 and it's QTWebEngine components.

**Juasap** has a window to display the web version of Whatsapp, "https://web.whatsapp.com," and an icon in the system tray to close the application. The window close button only hides the window and don't close the application.

### Requirements

- Python3
- Qt 5.14 (maybe works with other versions)
- PySide2
- Pyinstaller (to build an executable)


### Remarks

You can create an executable using "build.sh" script or executing directly **Juasap** with the command:

```sh
  python3 juasap.py
```

### Changelog

**2020-04-12 - _First version_**
- Added a window to browse "https://web.whatsapp.com".
- Added an icon to system tray to show the window and close the application.
