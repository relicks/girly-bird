@echo off


IF /I "%1"=="all" GOTO all
IF /I "%1"=="init" GOTO init
IF /I "%1"=="install" GOTO install
IF /I "%1"=="run" GOTO run
IF /I "%1"=="" GOTO all
GOTO error

:all
	CALL make.bat init
	CALL make.bat install
	CALL make.bat run
	GOTO :EOF

:init
	python -m venv .venv
	.\.venv\Scripts\python.exe -m pip install --upgrade pip
	GOTO :EOF

:install
	.\.venv\Scripts\pip install .
	GOTO :EOF

:run
	.\.venv\Scripts\python .\main.py
	GOTO :EOF

:error
    IF "%1"=="" (
        ECHO make: *** No targets specified and no makefile found.  Stop.
    ) ELSE (
        ECHO make: *** No rule to make target '%1%'. Stop.
    )
    GOTO :EOF
