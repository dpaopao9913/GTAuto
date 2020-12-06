@echo off
pushd %~dp0
setlocal enabledelayedexpansion

setlocal
set THIS_PATH=%~dp0
set INPUT_FILENAME=AllSdlxliffFilename.csv

rem Anacondaの仮想環境（base）の実行
call "C:\Program Files (x86)\Microsoft Visual Studio\Shared\Anaconda3_64\Scripts\activate.bat"

rem ==============================
rem === main rutine
rem ==============================
for /f "delims=" %%A in (%INPUT_FILENAME%) do (

    rem サブルーチン「edit_filename」に引数として、パス名を引き渡す
    rem echo %%A

    call :extract_filename "%%A"
    rem 参考: https://stackoverflow.com/questions/3942265/errorlevel-in-a-for-loop-batch-windows/11692001
    rem echo !EXTRACTED_FILENAME!

    set SUFFIX=.bilingual.csv
    set output_filename=!EXTRACTED_FILENAME!!SUFFIX!
    rem echo !output_filename!

    rem usage: 
    rem       python <*.py> <input_filename> <output_filename>
    GTAuto_ToCSV.py "%%A" "!output_filename!"
)
pause

rem ==============================
rem === subrutine01
rem ==============================
:extract_filename
rem echo %~n1
set EXTRACTED_FILENAME=%~n1
exit /b

endlocal