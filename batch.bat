echo %CD%
timeout /T 3
echo "please confirm the delete process, its only the old programm, with "y/j""
rd /s "Mastermind"

ren "neu_Mastermind" "Mastermind"
cd Mastermind
mastermind.exe
pause

