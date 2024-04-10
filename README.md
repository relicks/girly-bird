# chilly-bird

## 1. Prerequisites

- Python >= 3.10
- Pygame compatible system

## 2. Running from precompiled binaries

Only available for Windows and Linux. If there are problems with running the
game from precompiled binaries proceed to the `Running from source` section.

### 2.1. On Linux

Run the `bin/linux64/chilly-bird` file.

### 2.2. On Windows

Run the `bin\win64\chilly-bird.exe` file.

## 3. Running from source

### 3.1. On Unix-like systems

```sh
make # creates venv, installs the game and runs it
make run # runs the game, if installed in venv
```

### 3.2. On Windows

`make.bat` is converted from `Makefile` and has all the same commands,
though altered to run on Windows.

```bat
.\make.bat
.\make.bat run
```
