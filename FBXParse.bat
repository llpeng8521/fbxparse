@echo off

@echo 解析FBX工具
@echo start
@echo -------------------------------
cd "%~dp0"
python fbxparse.py %~f1
@echo -------------------------------
@echo finish
@echo on
pause