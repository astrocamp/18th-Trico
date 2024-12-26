# TriCo

TriCo 是一個專注於服務媒合的網站，讓使用者可以輕鬆購買或販售他人提供的專業服務，實現高效的資源交換與即時互動。

---

## 小組成員

| 成員名稱          | GitHub 帳號         | Email 信箱                     |
|------------------|--------------------|--------------------------------|
| Hsu-Pei-Chun     | hsu-pei-chun      | philosophysis@gmail.com       |
| doudouu0504      | doudouu0504       | selinafs880504@gmail.com      |
| tingchen1992     | tingchen1992      | happy810502@gmail.com         |
| MichellellehciM  | MichellellehciM   | ktlaiktlai@gmail.com          |
| jingjie1997      | jingjie1997       | artfulrachel6302524@gmail.com |
| chienchuanw      | chienchuanw       | chienchuanwww@gmail.com       |

---

## 專案執行指令

如果是第一次執行這個專案，請參考以下步驟：

1. **建立環境變數文件**  
   確保正確加載配置：  
   ```
   cp .env.example .env
   ```

2. **安裝 Poetry 的依賴**  
   ```
   poetry install
   ```

3. **安裝前端專案所需的依賴套件**  
   ```
   npm install
   ```

4. **啟動 Poetry 的虛擬環境**  
   ```
   poetry shell
   ```

5. **遷移資料庫模型欄位**  
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **載入分類選項**  
   ```
   python manage.py seed_categories
   ```

7. **啟動 Django 開發伺服器**  
   ```
   python manage.py runserver
   ```

---

## 環境安裝指令

- **打包 JavaScript 文件並生成輸出文件**  
  ```
  npm run build
  ```

- **監聽 JavaScript 文件變化**  
  ```
  npm run dev
  ```

- **生成並監聽 TailwindCSS 樣式文件變化**  
  ```
  npm run css
  ```

- **已安裝 HTMX**
