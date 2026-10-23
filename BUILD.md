# Windows EXE 打包版

來源為使用者指定的 Downloads/Actual_Pygame-main/Actual_Pygame-main 版本。保留原製作者名單與玩法。

## 修改

新增 asset_loader.py，所有圖片、字型與背景音樂改以程式所在位置定位。PyInstaller 封裝後會從內附素材讀取，不需要桌面或 Downloads 的原始資料夾。
新增 launch.py 為打包入口，packaged_checks.py 為內附資源檢查；main.py 仍可作為 Python 版本入口。

## 重建

在 Windows 專案資料夾開啟 PowerShell，使用 Python 3.12：

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install pygame==2.6.1 pyinstaller==6.22.3
.\.venv\Scripts\python.exe -m PyInstaller --clean --noconfirm ActualPygame.spec
```

產物為 dist/ActualPygame.exe。Spec 使用相對於自身位置的素材路徑，可搬移後重建。

## 驗證範圍

已直接執行封裝後的 EXE，在另一個含中文及空格的資料夾中，且 PATH 不含 Python，完成：
- 130 個素材的 SHA-256 核對。
- 128 張 PNG、1 個 TTF 字型及 1 個 MP3 音樂解碼。
- 四個選單建立及繪製。
- 五個關卡各召喚四種單位、隕石與敵人，執行 29 次事件迴圈並繪圖。
- 正常 main 入口及背景音樂初始化。

測試使用 SDL dummy 驅動並檢查產生的畫面，未涵蓋完整通關與所有 Windows 硬體配置。

PyInstaller 資源定位參考：https://www.pyinstaller.org/en/stable/runtime-information.html
