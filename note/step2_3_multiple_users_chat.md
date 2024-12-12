`self.scope` 是 Django Channels 提供的一個 **字典**，它存儲了與當前連接相關的上下文信息，並不是一個「三維字典」，而是一個**多層嵌套的字典結構**。

---

### **`self.scope` 的內容**

`scope` 包含的信息與 Django 的 `request` 類似，但它專門用於非同步協議（如 WebSocket）。以下是 `scope` 的一些重要鍵：

1. **`type`**  
   - 連接類型，例如 `"websocket"`。
2. **`path`**  
   - 當前連接的路徑，例如 `"/ws/chat/myroom/"`。
3. **`headers`**  
   - 請求的 HTTP 標頭，以字節對形式表示，例如：`[(b'host', b'localhost')]`。
4. **`query_string`**  
   - 請求的查詢字符串（URL 中的 `?key=value` 部分），以字節表示。
5. **`client`**  
   - 客戶端的 IP 地址和端口，例如：`("127.0.0.1", 50834)`。
6. **`server`**  
   - 伺服器的 IP 地址和端口，例如：`("127.0.0.1", 8000)`。
7. **`subprotocols`**  
   - WebSocket 協議的子協議。
8. **`user`**  
   - 當前認證的用戶對象，類似於 Django 的 `request.user`。
9. **`session`**  
   - Django 的會話對象，類似於 `request.session`。
10. **`url_route`**  
    - 與路由匹配相關的信息，特別是 URL 提取的參數。

---

### **範例：`scope` 的完整內容**

以下是一個典型的 `self.scope` 結構，假設連接的 URL 是：
```
ws://127.0.0.1:8000/ws/chat/myroom/?token=123
```

`self.scope` 的可能內容如下：

```python
{
    'type': 'websocket',  # 連接類型
    'path': '/ws/chat/myroom/',  # 請求的路徑
    'headers': [
        (b'host', b'127.0.0.1:8000'),
        (b'upgrade', b'websocket'),
        (b'connection', b'Upgrade'),
        (b'sec-websocket-key', b'some-key'),
        (b'sec-websocket-version', b'13'),
        (b'origin', b'http://127.0.0.1:8000'),
    ],
    'query_string': b'token=123',  # 查詢字符串
    'client': ('127.0.0.1', 50834),  # 客戶端的 IP 和端口
    'server': ('127.0.0.1', 8000),  # 伺服器的 IP 和端口
    'subprotocols': [],  # WebSocket 子協議（如果有）
    'user': <User: anonymous>,  # 當前用戶對象（默認為匿名用戶）
    'session': <django.contrib.sessions.backends.db.SessionStore object>,  # Django 會話
    'url_route': {
        'kwargs': {
            'room_name': 'myroom'  # 路由中提取的參數
        }
    }
}
```

---

### **如何使用 `scope` 的數據**

#### 1. **提取路由參數**
這是最常見的用途，通過 `scope['url_route']['kwargs']` 提取參數。

範例：
```python
self.room_name = self.scope['url_route']['kwargs']['room_name']
```

#### 2. **獲取用戶對象**
`scope['user']` 提供與當前連接關聯的 Django 用戶對象。

範例：
```python
if self.scope['user'].is_authenticated:
    print(f"User {self.scope['user'].username} connected")
else:
    print("Anonymous user connected")
```

#### 3. **讀取查詢字符串**
`scope['query_string']` 提供 URL 中的查詢參數。

範例：
```python
query_string = self.scope['query_string']
params = dict(param.split(b'=') for param in query_string.split(b'&'))
token = params.get(b'token')
```

#### 4. **訪問 HTTP 標頭**
`scope['headers']` 提供原始 HTTP 標頭數據。

範例：
```python
headers = dict(self.scope['headers'])
host = headers.get(b'host').decode('utf-8')
print(f"Host: {host}")
```

---

### **總結**

- `self.scope` 是 Django Channels 提供的上下文數據，是一個多層嵌套字典。
- 它的結構類似於 Django 的 `request`，但為非同步操作量身定制，包含 WebSocket 連接的各種信息。
- 開發者可以利用它來訪問路由參數、用戶、查詢字符串、HTTP 標頭等信息。