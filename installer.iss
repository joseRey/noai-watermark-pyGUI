[Setup]
; App Information
AppName=AI Watermark & Metadata Remover
AppVersion=1.0
AppPublisher=joseRey
AppPublisherURL=https://github.com/joseRey/Watermark-GUI

; Installation Paths
DefaultDirName={autopf}\WatermarkRemover
DefaultGroupName=AI Watermark Remover

; Output configuration
OutputDir=.
OutputBaseFilename=WatermarkRemover_Setup
Compression=lzma
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64

; Cosmetic
SetupIconFile=compiler:SetupClassicIcon.ico
UninstallDisplayIcon={app}\launcher.bat

[Files]
; Package our source files
Source: "gui_app.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "requirements.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "launcher.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
; Create Start Menu Shortcut
Name: "{group}\AI Watermark Remover"; Filename: "{app}\launcher.bat"; IconFilename: "cmd.exe"

; Create Desktop Shortcut
Name: "{autodesktop}\AI Watermark Remover"; Filename: "{app}\launcher.bat"; IconFilename: "cmd.exe"

[Run]
; Option to launch immediately after installation
Filename: "{app}\launcher.bat"; Description: "Launch AI Watermark Remover (First run will download AI models)"; Flags: postinstall nowait
