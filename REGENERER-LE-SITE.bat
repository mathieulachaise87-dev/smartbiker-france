@echo off
chcp 65001 >nul
cd /d "%~dp0"
title SMART BIKER - regenerer les pages

echo.
echo   Regeneration des pages a partir du dossier content\
echo.

set PY=
where py >nul 2>nul && set PY=py -3
if "%PY%"=="" (
  where python >nul 2>nul && set PY=python
)

if "%PY%"=="" (
  echo   Python n'est pas installe sur cet ordinateur.
  echo.
  echo   Installez-le ^(cochez "Add python.exe to PATH" pendant
  echo   l'installation^), puis relancez ce fichier.
  echo.
  start https://www.python.org/downloads/
  pause
  exit /b
)

echo   Verification des outils...
%PY% -m pip install --quiet --disable-pip-version-check pyyaml markdown pillow

echo.
%PY% build.py
echo.

if errorlevel 1 (
  echo   Une erreur s'est produite. Le message est juste au-dessus.
) else (
  echo   Termine. Ouvrez index.html pour voir le resultat.
)
echo.
pause
