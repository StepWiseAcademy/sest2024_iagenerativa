@echo off
set "PYTHON_PATH=Caminho\para\python.exe"

:: Verifica se o Python existe no caminho especificado
if not exist "%PYTHON_PATH%" (
    echo Python nao encontrado no caminho especificado: %PYTHON_PATH%
    echo Por favor, ajuste o caminho do Python antes de executar o script.
    pause
    exit /b
)

:: Cria o ambiente virtual na pasta atual
"%PYTHON_PATH%" -m venv venv

echo Ambiente virtual criado com sucesso na pasta atual.

echo Ativando ambiente.

call .\venv\Scripts\activate

cmd /k
