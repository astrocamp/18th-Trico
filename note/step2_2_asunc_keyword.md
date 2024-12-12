函數前面加上 `async` 關鍵字是因為 Django Channels 使用 **非同步編程模型**，而 `async` 關鍵字是 Python 中聲明 **非同步函數（協程）** 的方式。

---

### **1. 為什麼需要非同步編程？**

非同步編程的主要目的是提高程序的性能，特別是在處理大量 I/O 操作（如網絡請求、文件讀寫等）時。WebSocket 本質上是一種持續的網絡連接，非同步編程在這種情況下非常重要：

- **多任務並發**：非同步函數允許伺服器同時處理多個 WebSocket 連接，而不需要為每個連接阻塞伺服器資源。
- **避免阻塞**：如果一個函數正在等待某個操作完成（例如從 Redis 獲取數據），非同步模型允許程式繼續處理其他任務，而不是讓整個伺服器卡住等待。

---

### **2. `async` 關鍵字的作用**

`async` 關鍵字用於定義協程（coroutine），協程是一種可以被暫停並恢復的函數。它的作用包括：

- 告訴 Python 這是一個 **非同步函數**。
- 允許在函數內部使用 `await` 關鍵字，等待其他非同步操作完成。

範例：

```python
async def my_function():
    print("Before await")
    await some_async_task()  # 等待非同步操作完成
    print("After await")
```

在這個例子中，`await` 會暫停執行該協程，直到 `some_async_task()` 完成，然後繼續執行後續代碼。

---

### **3. Django Channels 和 `async`**

在 Django Channels 中，WebSocket 和 Channels Layer（通常是基於 Redis 的）都是 I/O 密集型操作，非同步函數可以讓這些操作高效運行。

以下是 Django Channels 的主要非同步操作場景：

#### **(1) WebSocket 操作**
- 接受 WebSocket 連接：`await self.accept()`。
- 向 WebSocket 發送消息：`await self.send(...)`。
- 等待來自客戶端的數據。

#### **(2) Channels Layer 操作**
- 加入群組：`await self.channel_layer.group_add(...)`。
- 從群組中刪除：`await self.channel_layer.group_discard(...)`。
- 向群組發送消息：`await self.channel_layer.group_send(...)`。

這些操作本質上是非同步的，需要 `async` 函數來使用 `await`。

---

### **4. 非同步函數的要求**

- 只有在 `async def` 定義的函數內部才能使用 `await`。
- 非同步函數不能直接調用同步函數，否則可能導致阻塞。
- 如果需要在非同步函數中調用同步函數，可以使用執行緒池（`concurrent.futures.ThreadPoolExecutor`）將同步代碼轉換為非同步執行。

---

### **5. 為什麼所有核心方法都需要加 `async`？**

Django Channels 的核心方法（如 `connect`、`disconnect`、`receive`）需要執行非同步操作，因此它們被要求定義為非同步函數：

#### **核心方法**
1. **`async def connect(self)`**
   - 當 WebSocket 連接建立時被調用。
   - 可能需要進行非同步操作（如驗證用戶、加入群組）。

2. **`async def disconnect(self, close_code)`**
   - 當 WebSocket 連接關閉時被調用。
   - 可能需要進行非同步操作（如從群組中移除用戶）。

3. **`async def receive(self, text_data)`**
   - 當 WebSocket 收到消息時被調用。
   - 可能需要進行非同步操作（如處理數據、將消息分發給其他用戶）。

#### **範例**
以下是一個具體的例子展示如何利用非同步操作處理 WebSocket：

```python
from channels.generic.websocket import AsyncWebsocketConsumer
import asyncio

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # 非同步地接受連接
        await self.accept()

    async def disconnect(self, close_code):
        # 非同步地從群組移除
        await self.channel_layer.group_discard("chat_group", self.channel_name)

    async def receive(self, text_data):
        # 模擬一個非同步的處理操作（例如訪問數據庫）
        await asyncio.sleep(1)  # 暫停 1 秒
        # 將消息發送回用戶端
        await self.send(text_data="Message received!")
```

---

### **6. 如果不加 `async` 會發生什麼？**

如果不使用 `async`，以下問題可能會發生：

- **無法使用 `await`**：如果沒有 `async`，Python 無法識別 `await`，並會拋出語法錯誤。
- **性能問題**：所有的操作都會變成同步的，伺服器可能會因為處理單個請求而阻塞，導致其他請求無法及時處理。

範例（錯誤的用法）：

```python
def connect(self):  # 缺少 async 關鍵字
    self.accept()  # 錯誤：accept 是非同步操作，必須使用 await
```

這會導致程序無法正常運行，並拋出以下錯誤：

```
RuntimeError: Task got bad yield: <coroutine object ...>
```

---

### **結論**
1. `async` 是用來聲明非同步函數的，允許在函數內使用 `await` 處理非同步操作。
2. Django Channels 的 `connect`、`disconnect` 和 `receive` 方法必須是非同步函數，因為它們需要執行非同步操作（如接受連接、向 WebSocket 發送消息等）。
3. 非同步函數提高了伺服器的性能，特別是在處理高並發的 WebSocket 連接時。