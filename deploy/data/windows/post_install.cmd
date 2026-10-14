sc stop AmneziaWGTunnel$AmneziaVPN
sc delete AmneziaWGTunnel$AmneziaVPN
taskkill /IM "ewokVPN-service.exe" /F
taskkill /IM "ewokVPN.exe" /F
exit /b 0
