$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut([Environment]::GetFolderPath("Desktop") + "\wechat-api.lnk")
$Shortcut.TargetPath = "D:\8___辅助资料\hermes-workspace\wechat-query\services\wechat-download-api\start_api.bat"
$Shortcut.WorkingDirectory = "D:\8___辅助资料\hermes-workspace\wechat-query\services\wechat-download-api"
$Shortcut.Description = "微信公众号文章API服务"
$Shortcut.Save()
Write-Host "OK"
