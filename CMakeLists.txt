project(OctoPrintPlugin)
cmake_minimum_required(VERSION 2.8.12)

install(FILES
    __init__.py
    OctoPrintOutputDevice.py
    OctoPrintOutputDevicePlugin.py
    LICENSE
    README.md
    DESTINATION lib/cura/plugins/OctoPrintPlugin
)
