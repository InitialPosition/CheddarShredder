pyinstaller cityapp.py ^
	--onefile ^
	--paths ./cityapp3/ ^
	--name CityApp ^
	--icon ./res/icon.ico ^
	--windowed ^
	--add-data="./cityapp3/window/ui/testIcons/logo_scaled.png;./window/ui/testIcons" ^
	--distpath ./dist/Windows
