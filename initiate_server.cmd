echo trying to initiate the server, please wait...
cd "C:\Program Files (x86)\Firebird\Firebird_2_0\bin"
dir
timeout /t 5
instsvc START
:: "C:\Program Files (x86)\Firebird\Firebird_2_0\bin\instsvc" START
timeout /t 5
exit