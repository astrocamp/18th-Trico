# TriCo

## 小組成員(GitHub 帳號/Email 信箱)

- Hsu-Pei-Chun / philosophysis@gmail.com
- doudouu0504 / selinafs880504@gmail.com
- tingchen1992 / happy810502@gmail.com
- MichellellehciM / ktlaiktlai@gmail.com
- jingjie1997 / artfulrachel6302524@gmail.com
- chienchuanw / chienchuanwww@gmail.com

## 專案執行指令

如果是第一次執行這個專案，請參考以下步驟：

- 建立環境變數文件，確保正確加載配置：`cp .env.example .env`
- poetry install：`poetry install`
- 安裝前端專案所需的依賴套件：`npm install`
- 啟動 Poetry 的虛擬環境：`poetry shell`
- 遷移模型欄位：`python manage.py makemigrations`
- 載入模型欄位：`python manage.py migrate`
- 載入分類選項：`python manage.py seed_categories`
- 啟動 Django 開發伺服器：`python manage.py runserver`

## 環境安裝指令

- 使用 esbuild 打包 JavaScript 文件並生成輸出文件：`npm run build`
- 監聽 JavaScript 文件的樣式變化：`npm run dev`
- 生成並監聽 TailwindCSS 的樣式文件變化：`npm run css`
- 已安裝 htmx
