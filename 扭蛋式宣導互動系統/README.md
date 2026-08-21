# 扭蛋式宣導互動系統

## 網頁版

直接用瀏覽器開啟 `index.html` 即可遊玩。網頁版不需要安裝 Python 或其他套件，適合部署到 GitHub Pages。

若要發布到 GitHub Pages：

1. 將本資料夾內容推送到 GitHub repository。
2. 到 repository 的 **Settings → Pages**。
3. 在 **Build and deployment** 選擇 **Deploy from a branch**，分支選 `main`、資料夾選 `/扭蛋式宣導互動系統`（若 Pages 不支援子資料夾，請將本資料夾內容放到 repository 根目錄）。
4. 儲存後，GitHub 會提供一個 `github.io` 網站網址。

網頁版會從 `宣導用` 資料夾的圖片清單中隨機抽出海報。若新增或刪除圖片，請同步更新 `script.js` 裡的 `posterFiles` 清單，GitHub Pages 就會顯示最新圖片。

## 使用方式

1. 安裝 Python 3。
2. 用 VS Code 開啟本資料夾。
3. 開啟 VS Code 終端機，執行：

```bash
python -m pip install pillow
```

4. 把宣導圖片放進 `宣導用` 資料夾。
5. 執行：

```bash
python main.py
```

支援 PNG、JPG、JPEG、GIF。

程式會自動讀取 `宣導用` 資料夾，不需要在程式碼中設定圖片檔名。

## 互動流程

開始抽扭蛋
→ 扭蛋機晃動
→ 扭蛋掉出
→ 點擊扭蛋
→ 扭蛋開啟
→ 隨機宣導海報彈出
→ 再抽一次

程式會記住上一張宣導圖片，因此正常情況下不會連續抽到相同圖片。

## 錯誤處理

- 找不到 `宣導用` 資料夾：顯示提示，不會直接當機。
- 資料夾沒有圖片：顯示提示。
- 只有一張圖片：直接使用該圖片，不進行排除。
