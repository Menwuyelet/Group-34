# HTTP Versions and Request Methods – Study Notes

## 📌 What is HTTP?

HTTP stands for **Hypertext Transfer Protocol**. It’s the protocol that allows web browsers, mobile apps, and other clients to communicate with web servers.

At its core, HTTP works on a **request-response** model:

- The **client** sends a request (like asking for a web page),
- The **server** processes it and sends back a response (like the HTML content or JSON data).

It’s a **stateless** protocol, meaning each request is independent and doesn't remember anything from previous ones (unless you use cookies, sessions, etc.).

---

## 🔢 Difference HTTP Versions

Over time, HTTP has gone through several versions to make the communication between clients and servers faster, more efficient, and more secure. Here's a breakdown of how each version improves on the previous one.

---

### ✅ HTTP/0.9

This was the very first version. Extremely basic.

- Only supported the `GET` method.
- No headers, no status codes—just raw HTML content.
- No support for images, styles, or scripts.
- Very limited and not used today.

> **Use case:** Just fetching simple web pages.

### Headers

Contain metadata—information about the request or response

such as:

For requests:

- Host: the domain name

- User-Agent: browser info

- Accept: types of data the client can handle

For responses:

- Content-Type: like text/html, application/json

- Content-Length: size of the body

- Set-Cookie: for setting cookies

---

### ✅ HTTP/1.0

This was the first version to introduce important features such as:

- **Headers**: So clients and servers could share extra info like content type, length, etc.
- **Status codes**: Now you could know if the request was successful (e.g., `200 OK`, `404 Not Found`).
- Added methods like `POST` and `HEAD` in addition to `GET` method.

**Its Limitation** was every request opened a new TCP connection. This meant loading a single page with multiple resources (like CSS, JS, and images) was slow.

- A TCP connection is a reliable communication link between two devices (like a client and a server) over the internet, established using the Transmission Control Protocol (TCP).

---

### ✅ HTTP/1.1

It introduced a major improvement and still widely used today.

- Introduced **persistent connections** (keep-alive), so multiple requests could be handled over the same connection.
- Allowed **pipelining** (sending multiple requests without waiting for responses).
- Added support for **chunked transfers** and **caching**.
- Introduced the `Host` header—important for hosting multiple websites on the same server.

> Still, it had problems like **head-of-line blocking**, where one slow request could delay others.

- Head-of-line (HOL) blocking happens in network communication when a line of data gets stuck because the first packet is delayed or lost, and everything behind it has to wait—even if those later packets arrived successfully.

---

### ✅ HTTP/2

This version introduced features to make things much faster, smarter and secure.

- Instead of text, it's a **binary protocol** (faster parsing and less error-prone). A binary protocol is a way of formatting data for communication where the data is encoded in binary (0s and 1s) rather than plain text (human-readable characters).
- Supports **multiplexing**: multiple requests and responses can happen in parallel on a single connection.
- Compresses headers to reduce redundancy (via **HPACK**). HTTP requests and responses include headers — little pieces of information like content type, cookies, user-agent, and more. These headers can get quite large, especially when many requests are made, and a lot of the header data is repetitive across requests. To improve performance, HTTP/2 uses a compression algorithm called HPACK to reduce the size of these headers.

> Greatly reduces latency and improves performance, especially for complex web apps.

---

### ✅ HTTP/3

It is the latest version, focused on speed and reliability, especially on modern networks.

- Uses a new transport protocol called **QUIC** (built on **UDP**, not TCP).
- Handles packet loss more gracefully and avoids head-of-line blocking entirely.
- Built-in encryption (no need for separate TLS handshake).
- Establishes connections faster (great for mobile devices and unstable networks).

---

## 🚀 HTTP Request Methods

HTTP methods (also called verbs) define the kind of operation the client wants the server to perform on a resource. These are essential when designing or working with web services and APIs.

---

### 🟩 GET

- Used to **retrieve** data from the server.
- It **does not** change anything on the server.
- The most common method (e.g., visiting a web page).
- Can be cached and bookmarked.

---

### 🟦 POST

- Used to **send data** to the server (e.g., form submission).
- Typically used to **create new resources**.
- Not idempotent (sending it twice may create two items).

---

### 🟧 PUT

- Used to **update** or **replace** a resource entirely.
- Idempotent (doing it multiple times has the same effect).
- Often used in APIs when editing full objects.

---

### 🟨 PATCH

- Used to **partially update** a resource (just change one field, for example).
- More efficient than PUT when you don’t want to send the entire object.

---

### 🟥 DELETE

- Tells the server to **remove** a resource.
- Idempotent—deleting the same resource multiple times has the same result.

---

### ⚪ HEAD

- Like GET, but only retrieves the **headers** (no response body).
- Good for checking if something exists or getting metadata (like file size).

---

### ⚫ OPTIONS

- Used to **check which HTTP methods** are supported for a resource.
- Often used in **CORS preflight** checks in browsers.

---
