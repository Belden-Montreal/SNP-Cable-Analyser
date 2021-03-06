; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

#define MyAppName "SNP Analyzer"
#define MyAppVersion "0.1.1"
#define MyAppPublisher "Belden Inc."
#define MyAppURL "https://github.com/liamaltarac/SNP-Cable-Analyser"
#define MyAppExeName "SNPAnalyzer.exe"

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{14AE230B-9257-4457-AB8C-A27E009DC353}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={pf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
OutputBaseFilename=SNPAnalyzerSetup
Compression=lzma
SolidCompression=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "C:\Users\cedryk\Documents\SNP-Cable-Analyser\dist\main\SNPAnalyzer.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cedryk\Documents\SNP-Cable-Analyser\dist\main\_asyncio.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cedryk\Documents\SNP-Cable-Analyser\dist\main\_bz2.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cedryk\Documents\SNP-Cable-Analyser\dist\main\_contextvars.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cedryk\Documents\SNP-Cable-Analyser\dist\main\_ctypes.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cedryk\Documents\SNP-Cable-Analyser\dist\main\_decimal.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cedryk\Documents\SNP-Cable-Analyser\dist\main\_distutils_findvs.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cedryk\Documents\SNP-Cable-Analyser\dist\main\_hashlib.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cedryk\Documents\SNP-Cable-Analyser\dist\main\_lzma.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cedryk\Documents\SNP-Cable-Analyser\dist\main\_multiprocessing.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cedryk\Documents\SNP-Cable-Analyser\dist\main\_overlapped.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cedryk\Documents\SNP-Cable-Analyser\dist\main\_queue.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cedryk\Documents\SNP-Cable-Analyser\dist\main\_socket.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cedryk\Documents\SNP-Cable-Analyser\dist\main\_sqlite3.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cedryk\Documents\SNP-Cable-Analyser\dist\main\_ssl.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cedryk\Documents\SNP-Cable-Analyser\dist\main\_tkinter.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cedryk\Documents\SNP-Cable-Analyser\dist\main\base_library.zip"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cedryk\Documents\SNP-Cable-Analyser\dist\main\kiwisolver.cp37-win_amd64.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cedryk\Documents\SNP-Cable-Analyser\dist\main\lib_arpack-.3EACCC44R6URYOMHQMYVCKQCOM2QIBWU.gfortran-win_amd64.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cedryk\Documents\SNP-Cable-Analyser\dist\main\lib_blas_su.QEQE75KHNLMPCS22K3WRCEACXGLTB6HX.gfortran-win_amd64.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cedryk\Documents\SNP-Cable-Analyser\dist\main\lib_test_fo.JF5HTWMUPBXWGAYEBVEJU3OZAHTSVKCT.gfortran-win_amd64.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cedryk\Documents\SNP-Cable-Analyser\dist\main\libansari.R6EA3HQP5KZ6TAXU4Y4ZVTRPT7UVA53Z.gfortran-win_amd64.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cedryk\Documents\SNP-Cable-Analyser\dist\main\libbanded5x.YUREFBE7I7SVCEADSLRKXT6OOZGRBSI4.gfortran-win_amd64.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cedryk\Documents\SNP-Cable-Analyser\dist\main\libbispeu.5N2XSD7URZS4WTOSLTOG4DDMA4HGB46U.gfortran-win_amd64.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cedryk\Documents\SNP-Cable-Analyser\dist\main\libblkdta00.5GIEOPPZ5HSTP5DAMUKWIW364O4QBFMY.gfortran-win_amd64.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cedryk\Documents\SNP-Cable-Analyser\dist\main\libchkder.6HLXPVTQJEGRZGLI5DFRMNW3SS76BHP6.gfortran-win_amd64.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cedryk\Documents\SNP-Cable-Analyser\dist\main\libcobyla2.JEGTSUUFJ7DFXWZN5PAYZTTLBDATC4WD.gfortran-win_amd64.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cedryk\Documents\SNP-Cable-Analyser\dist\main\libcrypto-1_1-x64.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cedryk\Documents\SNP-Cable-Analyser\dist\main\libd_odr.KVFHIZPGUGII2ECJE7R2OHXK5HXMWUBQ.gfortran-win_amd64.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cedryk\Documents\SNP-Cable-Analyser\dist\main\libdcosqb.K4J3XBR4PEETMRHZICUWW4LXG5UONZ34.gfortran-win_amd64.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cedryk\Documents\SNP-Cable-Analyser\dist\main\libdcosqb.QRGA36MB6CFHWLQN6ETWARR4M4E6P3C2.gfortran-win_amd64.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cedryk\Documents\SNP-Cable-Analyser\dist\main\libdcsrch.I2AOPDCXAPDRFNPWY55H5UE7XZSU5CVN.gfortran-win_amd64.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cedryk\Documents\SNP-Cable-Analyser\dist\main\libdet.NGI4SZSHQBJM5NEVUSJQND4WM2GMQE54.gfortran-win_amd64.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cedryk\Documents\SNP-Cable-Analyser\dist\main\libdfft_sub.H6SHLMT5W26CD2XUAFVQ3LOOJUC4U4T4.gfortran-win_amd64.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cedryk\Documents\SNP-Cable-Analyser\dist\main\libdfitpack.PJU6IBGOYZCWITNVROHYOQAYNGAXO3HT.gfortran-win_amd64.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cedryk\Documents\SNP-Cable-Analyser\dist\main\libdgamln.KTXSQTWP7LWG4EZMWBS4LH477BS6ZGYC.gfortran-win_amd64.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cedryk\Documents\SNP-Cable-Analyser\dist\main\libdop853.6TJTQZW3I3Q3QIDQHEOBEZKJ3NYRXI4B.gfortran-win_amd64.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cedryk\Documents\SNP-Cable-Analyser\dist\main\libdqag.VX5QPGEJYMIC5JGWBYFC5BHJCBBVPPDV.gfortran-win_amd64.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cedryk\Documents\SNP-Cable-Analyser\dist\main\libgetbreak.A6HULTPFZ6I2MFB4CVJ5HQKTG6FYIBPY.gfortran-win_amd64.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cedryk\Documents\SNP-Cable-Analyser\dist\main\libGLESv2.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cedryk\Documents\SNP-Cable-Analyser\dist\main\liblbfgsb.B2GDIH5ZLORB7V6SRZRPDJE26PPONKZC.gfortran-win_amd64.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cedryk\Documents\SNP-Cable-Analyser\dist\main\libmvndst.RBJKFH65GH3A3NKEATRJ523P6WF4AZAG.gfortran-win_amd64.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cedryk\Documents\SNP-Cable-Analyser\dist\main\libnnls.IXEEHJUCGHJL42YZEM6UIEMROJWXHMLJ.gfortran-win_amd64.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cedryk\Documents\SNP-Cable-Analyser\dist\main\libopenblas.BNVRK7633HSX7YVO2TADGR4A5KEKXJAW.gfortran-win_amd64.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cedryk\Documents\SNP-Cable-Analyser\dist\main\libopenblas.CSRRD7HKRKC3T3YXA7VY7TAZGLSWDKW6.gfortran-win_amd64.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cedryk\Documents\SNP-Cable-Analyser\dist\main\libslsqp_op.NNY57ZXZ43A4RH3YWFA7BKHP5PC2K3I5.gfortran-win_amd64.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cedryk\Documents\SNP-Cable-Analyser\dist\main\libspecfun.BHLTWMBI4EYWDACZN4DQUESSDJRJNGEL.gfortran-win_amd64.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cedryk\Documents\SNP-Cable-Analyser\dist\main\libssl-1_1-x64.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cedryk\Documents\SNP-Cable-Analyser\dist\main\libvode.4H2RO3B5HKRH6QPBU4GYYKK3YPWS7OUR.gfortran-win_amd64.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cedryk\Documents\SNP-Cable-Analyser\dist\main\libwrap_dum.43IN5WJ7HGVGKYPFVJK5YQ34OMH3IKLA.gfortran-win_amd64.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cedryk\Documents\SNP-Cable-Analyser\dist\main\libwrap_dum.V5FHT5OP45YBBACXAHY3NF5CISQJNFFQ.gfortran-win_amd64.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cedryk\Documents\SNP-Cable-Analyser\dist\main\MSVCP140.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cedryk\Documents\SNP-Cable-Analyser\dist\main\pyexpat.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cedryk\Documents\SNP-Cable-Analyser\dist\main\python3.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cedryk\Documents\SNP-Cable-Analyser\dist\main\python37.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cedryk\Documents\SNP-Cable-Analyser\dist\main\Qt5Core.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cedryk\Documents\SNP-Cable-Analyser\dist\main\Qt5DBus.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cedryk\Documents\SNP-Cable-Analyser\dist\main\Qt5Gui.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cedryk\Documents\SNP-Cable-Analyser\dist\main\Qt5Network.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cedryk\Documents\SNP-Cable-Analyser\dist\main\Qt5Qml.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cedryk\Documents\SNP-Cable-Analyser\dist\main\Qt5Quick.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cedryk\Documents\SNP-Cable-Analyser\dist\main\Qt5Svg.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cedryk\Documents\SNP-Cable-Analyser\dist\main\Qt5WebSockets.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cedryk\Documents\SNP-Cable-Analyser\dist\main\Qt5Widgets.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cedryk\Documents\SNP-Cable-Analyser\dist\main\select.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cedryk\Documents\SNP-Cable-Analyser\dist\main\SNPAnalyzer.exe.manifest"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cedryk\Documents\SNP-Cable-Analyser\dist\main\sqlite3.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cedryk\Documents\SNP-Cable-Analyser\dist\main\tcl86t.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cedryk\Documents\SNP-Cable-Analyser\dist\main\tk86t.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cedryk\Documents\SNP-Cable-Analyser\dist\main\unicodedata.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cedryk\Documents\SNP-Cable-Analyser\dist\main\VCRUNTIME140.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cedryk\Documents\SNP-Cable-Analyser\dist\main\Include\*"; DestDir: "{app}\Include"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\cedryk\Documents\SNP-Cable-Analyser\dist\main\IPython\*"; DestDir: "{app}\IPython"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\cedryk\Documents\SNP-Cable-Analyser\dist\main\jedi\*"; DestDir: "{app}\jedi"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\cedryk\Documents\SNP-Cable-Analyser\dist\main\lib2to3\*"; DestDir: "{app}\lib2to3"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\cedryk\Documents\SNP-Cable-Analyser\dist\main\limits\*"; DestDir: "{app}\limits"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\cedryk\Documents\SNP-Cable-Analyser\dist\main\markupsafe\*"; DestDir: "{app}\markupsafe"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\cedryk\Documents\SNP-Cable-Analyser\dist\main\matplotlib\*"; DestDir: "{app}\matplotlib"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\cedryk\Documents\SNP-Cable-Analyser\dist\main\mpl-data\*"; DestDir: "{app}\mpl-data"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\cedryk\Documents\SNP-Cable-Analyser\dist\main\numpy\*"; DestDir: "{app}\numpy"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\cedryk\Documents\SNP-Cable-Analyser\dist\main\pandas\*"; DestDir: "{app}\pandas"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\cedryk\Documents\SNP-Cable-Analyser\dist\main\PyQt5\*"; DestDir: "{app}\PyQt5"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\cedryk\Documents\SNP-Cable-Analyser\dist\main\pytz\*"; DestDir: "{app}\pytz"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\cedryk\Documents\SNP-Cable-Analyser\dist\main\scipy\*"; DestDir: "{app}\scipy"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\cedryk\Documents\SNP-Cable-Analyser\dist\main\skrf\*"; DestDir: "{app}\skrf"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\cedryk\Documents\SNP-Cable-Analyser\dist\main\tcl\*"; DestDir: "{app}\tcl"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\cedryk\Documents\SNP-Cable-Analyser\dist\main\tk\*"; DestDir: "{app}\tk"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

