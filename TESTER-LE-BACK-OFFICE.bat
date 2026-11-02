@echo off
chcp 65001 >nul
cd /d "%~dp0"
title SMART BIKER - back-office local
setlocal

echo.
echo   ================================================
echo     SMART BIKER - back-office sur votre ordinateur
echo   ================================================
echo.

where node >nul 2>nul
if errorlevel 1 (
  echo   Node.js n'est pas installe sur cet ordinateur.
  echo.
  echo   Installez-le ^(bouton "Obtenir Node.js", version LTS^),
  echo   puis FERMEZ cette fenetre et relancez ce fichier.
  echo.
  start https://nodejs.org/fr
  pause
  exit /b
)

for /f "tokens=*" %%v in ('node --version') do echo   Node.js %%v detecte.

if exist port.txt del port.txt >nul 2>nul

echo   Demarrage du serveur du site...
start "Serveur du site - NE PAS FERMER" cmd /k node serveur-local.js

echo   Demarrage du back-office...
if exist log-backoffice.txt del log-backoffice.txt >nul 2>nul
( echo CWD=%CD% & node --version & npm --version & where npx ) > log-environnement.txt 2>&1
start "Back-office - NE PAS FERMER" cmd /k "npx -y decap-server > log-backoffice.txt 2>&1"

echo.
echo   [1/2] Recherche du serveur du site...

set PORT=
set /a essais=0
:attendre_site
set /a essais+=1
if exist port.txt set /p PORT=<port.txt
if not "%PORT%"=="" goto site_pret
if %essais% GEQ 30 goto echec_site
timeout /t 1 /nobreak >nul
goto attendre_site

:site_pret
echo         Serveur du site pret, port %PORT%.
echo.
echo   [2/2] Attente du back-office...
echo         Au premier lancement il se telecharge,
echo         comptez une a deux minutes.
echo.

set /a essais2=0
:attendre_cms
set /a essais2+=1
curl -s -o nul -m 3 http://127.0.0.1:8081/api/v1 >nul 2>nul
if not errorlevel 7 goto cms_pret
if %essais2% GEQ 150 goto echec_cms
timeout /t 2 /nobreak >nul
if %essais2%==15 echo         toujours en cours, c'est normal...
if %essais2%==45 echo         toujours en cours, patientez encore...
goto attendre_cms

:cms_pret
echo         Back-office pret.
echo.
timeout /t 2 /nobreak >nul
start http://localhost:%PORT%/admin/

echo   ------------------------------------------------
echo     Le site        http://localhost:%PORT%/
echo     Le back-office http://localhost:%PORT%/admin/
echo.
echo   Pas de mot de passe : vous modifiez directement
echo   les fichiers de ce dossier.
echo.
echo   Laissez les deux fenetres noires ouvertes.
echo   Pour tout arreter, fermez-les.
echo.
echo   Apres avoir publie une modification, lancez
echo   REGENERER-LE-SITE.bat pour voir le resultat.
echo   ------------------------------------------------
echo.
pause
exit /b

:echec_site
echo.
echo   Le serveur du site n'a pas demarre.
echo   Regardez la fenetre "Serveur du site" : elle affiche
echo   le message d'erreur. Envoyez-le moi.
echo.
pause
exit /b

:echec_cms
echo.
echo   Le back-office n'a pas demarre.
echo   Le detail de l'erreur est dans log-backoffice.txt,
echo   je peux le relire a distance.
echo.
echo   Le site, lui, fonctionne : http://localhost:%PORT%/
echo.
echo   Regardez la fenetre "Back-office" : elle affiche
echo   le message d'erreur. Envoyez-le moi.
echo.
start http://localhost:%PORT%/
pause
