---
---

# 🔹 What is HTTP?

**HTTP (HyperText Transfer Protocol)** is the foundation of data communication on the web. It defines how messages are **formatted and transmitted**, and how **web servers** and **browsers should respond** to various commands.

When you type a URL into your browser, like https://en.wikipedia.org/wiki/HTTP, you're using HTTP to request a web page from a server.

### 🔹 Why was HTTP created?

HTTP was developed as a **simple, stateless protocol** to allow documents (initially just plain text) to be retrieved over the internet. It has evolved into a system that can handle multimedia content, APIs, secure communications, and more.

---

### 🔹 How does it work?

HTTP follows a **client-server model**:

- **Client (e.g., your browser)** sends an **HTTP request** to a **server**.
- **Server** processes the request and sends back an **HTTP response**.

This exchange happens every time you:

- Load a web page
- Submit a form
- Click a link
- Fetch data in an app

---

### 🔹 Example of an HTTP Request

When your browser requests a page:

```
GET /index.html HTTP/1.1
Host: www.example.com
```

- `GET` is the HTTP method.
- `/index.html` is the path to the resource.
- `HTTP/1.1` is the protocol version.

---

### 🔹 Example of an HTTP Response

```
HTTP/1.1 200 OK
Content-Type: text/html
Content-Length: 1234

<html> ... </html>
```

- `200 OK` is the status code, meaning success.
- The body contains the HTML page to be displayed.

---

### 🔹 HTTP Methods (Common Ones)

- **GET** – Retrieve data (e.g., a web page).
- **POST** – Send data (e.g., a form).
- **PUT** – Update a resource.
- **DELETE** – Remove a resource.
- **PATCH** – Partially update a resource.

---

### 🔹 Stateless Protocol

HTTP is **stateless**, meaning each request is independent. The server doesn't remember previous requests. To manage sessions (like staying logged in), websites use **cookies, tokens, or session IDs**.

---

### 🔹 Versions of HTTP

- **HTTP/1.0** – Basic, one request per connection.
- **HTTP/1.1** – Adds persistent connections, chunked transfers, more headers.
- **HTTP/2** – Faster, multiplexing (multiple requests in one connection).
- **HTTP/3** – Even faster, based on QUIC (UDP instead of TCP).

---

### 🔹 HTTP vs HTTPS

- **HTTP**: Data is sent in **plain text** – insecure.
- **HTTPS**: Secure version using **SSL/TLS encryption** – protects your data from eavesdroppers.

---

### 🔹 Summary

| Feature        | HTTP                        |
| -------------- | --------------------------- |
| Stands for     | HyperText Transfer Protocol |
| Type           | Request-response protocol   |
| Used by        | Browsers, mobile apps, APIs |
| Secure version | HTTPS                       |
| Stateless?     | Yes                         |
| Versions       | 1.0, 1.1, 2, 3              |

---
