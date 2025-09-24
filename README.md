# sql_master
An utility tool to analyze, compare and revise files for sql scripts.


to generate the exe

pyinstaller --onefile --add-data "analysis.py:." --add-data "app.py:." --add-data "git_commands.py:." --add-data "col_rename.py:." run_app.py

check in the dist/ for exe file
