# SpaceshipGame
A 2d Shoot 'em up game written in pygame.

## Running

Install dependencies with pip:

```bash
pip install pygame
```

Run the main program:

```bash
python main.py
```
## Building

SpaceshipGame can be built using PyInstaller. First, install PyInstaller if you don't have it:

    pip install pyinstaller

Next, install the Python dependencies:

    pip install -r requirements.txt

On Linux, you may also need to install tkinter.

To build exectuables for Windows, run the `build.cmd` file.

For Mac or Linux, run the `build.sh` file.

The executables can be found in the `dist` folder.

Optionally, if you want to use UPX, download it from https://upx.github.io/ and extract it to the `upx` folder, such that the UPX executable is in the folder root.

