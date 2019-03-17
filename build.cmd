@echo off

pyinstaller .\main.py ^
--onefile ^
--log-level=DEBUG ^
--specpath=.\build\ ^
--name="SpaceshipGame" ^

