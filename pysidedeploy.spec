[app]
title = auctionretrostore
project_dir = .
input_file = main.py
exec_directory = .
project_file = auction_retro_store.pyproject

[python]
python_path = python3
packages = Nuitka==2.6.8,ordered_set,zstandard
android_packages = buildozer==1.5.0,cython==0.29.37

[qt]
qml_files =
excluded_qml_plugins =
modules = Core,Gui,Widgets,Multimedia,Network

[android]
wheel_pyside =
wheel_shiboken =
plugins =

[nuitka]
extra_args = --quiet --noinclude-qt-translations

[buildozer]
mode = debug
recipe_dir =
jars_dir =
ndk_path =
sdk_path =
modules = Core,Gui,Widgets,Multimedia,Network
local_libs = plugins_platforms_qtforandroid
arch = aarch64
