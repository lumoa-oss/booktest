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
        "User-Agent": "python-requests/2.32.3",
        "X-Amzn-Trace-Id": "Root=1-66d6f383-3d65fc8142aa30720965b6ad",
        "X-Api-Key": "mock",
        "X-Timestamp": "1725363074.3761563",
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
        "User-Agent": "python-requests/2.32.3",
        "X-Amzn-Trace-Id": "Root=1-66d6f383-3d65fc8142aa30720965b6ad",
        "X-Api-Key": "mock",
        "X-Timestamp": "1725363074.3761563",
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
    "message": "hello"
}

# request snaphots:

 * https://httpbin.org/anything - 0d833a0b8b125360f00a5ee7cda46c3600948092
 * https://httpbin.org/anything - 2ee62c41048ed9e981d586a43d61217cb119632a

# env snaphots:

 * HOST_NAME=https://httpbin.org/anything
