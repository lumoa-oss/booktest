# description:

in this description, it's assumed that user id is significant. 
this test should create 2 snapshots, one for each user

# response for user 1:

{
    "args": {},
    "data": "{\"message\": \"hello\"}",
    "files": {},
    "form": {},
    "headers": {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Content-Length": "20",
        "Content-Type": "application/json",
        "Host": "httpbin.org",
        "User-Agent": "python-requests/2.31.0",
        "X-Amzn-Trace-Id": "Root=1-66d8157f-7f46b8c1585c2c7c098b6fa6",
        "X-Api-Key": "mock",
        "X-Timestamp": "1725437310.9940488",
        "X-User-Id": "1"
    },
    "json": {
        "message": "hello"
    },
    "method": "POST",
    "origin": "82.181.38.215",
    "url": "https://httpbin.org/anything"
}

# 2nd response for user 1:

{
    "args": {},
    "data": "{\"message\": \"hello\"}",
    "files": {},
    "form": {},
    "headers": {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Content-Length": "20",
        "Content-Type": "application/json",
        "Host": "httpbin.org",
        "User-Agent": "python-requests/2.31.0",
        "X-Amzn-Trace-Id": "Root=1-66d8157f-7f46b8c1585c2c7c098b6fa6",
        "X-Api-Key": "mock",
        "X-Timestamp": "1725437310.9940488",
        "X-User-Id": "1"
    },
    "json": {
        "message": "hello"
    },
    "method": "POST",
    "origin": "82.181.38.215",
    "url": "https://httpbin.org/anything"
}

# response for user 2:

{
    "args": {},
    "data": "{\"message\": \"hello\"}",
    "files": {},
    "form": {},
    "headers": {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Content-Length": "20",
        "Content-Type": "application/json",
        "Host": "httpbin.org",
        "User-Agent": "python-requests/2.31.0",
        "X-Amzn-Trace-Id": "Root=1-66d81580-1af920d36cf3928159051721",
        "X-Api-Key": "mock",
        "X-Timestamp": "1725437311.7450721",
        "X-User-Id": "2"
    },
    "json": {
        "message": "hello"
    },
    "method": "POST",
    "origin": "82.181.38.215",
    "url": "https://httpbin.org/anything"
}

# request snaphots:

 * https://httpbin.org/anything - d360944caa4275ee6fb2da7159894b4ed90cd17f
 * https://httpbin.org/anything - 655d501f55408bce98f364383a5f1d6b5378e30b

# env snaphots:

 * HOST_NAME=https://httpbin.org/anything
