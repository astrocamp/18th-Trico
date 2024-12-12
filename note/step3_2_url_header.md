### **`ws` 是什麼意思？**

`ws` 是 **WebSocket 協議**的 URI 前綴，用於指示瀏覽器或客戶端應該使用 WebSocket 協議來建立連接。

- **`ws://`**：表示非加密的 WebSocket 連接（類似於 HTTP）。
- **`wss://`**：表示加密的 WebSocket 連接（類似於 HTTPS）。

---

### **WebSocket 與 HTTP 的區別**

1. **協議層**

   - WebSocket 是一種基於 TCP 的協議，但與 HTTP 不同。
   - 它在首次連接時使用 HTTP 作為握手（`HTTP Upgrade`），然後切換到 WebSocket 協議。

2. **持久連接**
   - 與 HTTP 的請求-響應模式不同，WebSocket 是持久連接，允許雙向通信。

---

### **`ws` 能改嗎？**

不，**`ws` 不能隨便改**，因為它是 WebSocket 協議的指定前綴。如果你修改為其他值（如 `http` 或 `ftp`），則瀏覽器或客戶端無法識別並使用 WebSocket 協議，會導致連接失敗。

- **正確的 URI 前綴**：

  - `ws://`：非加密的 WebSocket。
  - `wss://`：加密的 WebSocket。

- **錯誤示例**（會導致錯誤）：
  - `http://`：這是 HTTP 協議，不能用於 WebSocket。
  - `ftp://`：這是 FTP 協議，與 WebSocket 無關。

---

### **如何選擇使用 `ws` 還是 `wss`？**

1. **`ws://`（非加密）**

   - 適用於本地開發環境（如 `localhost` 或內網）。
   - 不適合在互聯網上使用，因為沒有加密，數據可能被竊聽或篡改。

2. **`wss://`（加密）**
   - 適用於生產環境，尤其是公開互聯網。
   - 需要伺服器支持 HTTPS（SSL/TLS）。

---

### **前端自動選擇協議**

通常，前端代碼會根據當前的 HTTP/HTTPS 協議來選擇使用 `ws://` 或 `wss://`。

#### **JavaScript 範例**

```javascript
const wsProtocol = window.location.protocol === 'https:' ? 'wss://' : 'ws://'
const wsUrl = `${wsProtocol}${window.location.host}/ws/chat/123/`

const chatSocket = new WebSocket(wsUrl)

chatSocket.onopen = function () {
  console.log('WebSocket connection established')
}

chatSocket.onmessage = function (event) {
  console.log('Received message:', event.data)
}
```

- 如果當前頁面是 `https://example.com`，則 WebSocket URL 為：
  ```
  wss://example.com/ws/chat/123/
  ```
- 如果當前頁面是 `http://localhost:8000`，則 WebSocket URL 為：
  ```
  ws://localhost:8000/ws/chat/123/
  ```

---

### **錯誤的修改示例**

如果你隨便修改 `ws`，會導致以下問題：

1. **使用 `http://` 或 `https://`**

   - 錯誤：這是 HTTP 協議，瀏覽器會認為你嘗試發送普通的 HTTP 請求，而非 WebSocket 請求，會拋出錯誤。

2. **使用自定義協議（如 `abc://`）**
   - 錯誤：瀏覽器或客戶端無法識別自定義協議，會直接拒絕連接。

---

### **總結**

1. **`ws://` 和 `wss://` 是 WebSocket 的專用協議前綴**：

   - `ws://` 用於非加密連接（本地開發）。
   - `wss://` 用於加密連接（生產環境）。

2. **不能隨意更改 `ws`**，因為它是 WebSocket 協議的標準部分。隨意更改會導致瀏覽器或客戶端無法識別協議，導致連接失敗。

3. **最佳實踐**：
   - 開發環境：使用 `ws://`。
   - 生產環境：使用 `wss://`，確保數據傳輸安全。
