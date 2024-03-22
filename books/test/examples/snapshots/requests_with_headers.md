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
        "X-Amzn-Trace-Id": "Root=1-65fd3624-3529480e217d49f05feb05fe",
        "X-Api-Key": "secret",
        "X-Timestamp": "1711093284.323702",
        "X-User-Id": "1"
    },
    "json": {
        "message": "hello"
    },
    "method": "POST",
    "origin": "89.27.46.42",
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
        "X-Amzn-Trace-Id": "Root=1-65fd3624-3529480e217d49f05feb05fe",
        "X-Api-Key": "secret",
        "X-Timestamp": "1711093284.323702",
        "X-User-Id": "1"
    },
    "json": {
        "message": "hello"
    },
    "method": "POST",
    "origin": "89.27.46.42",
    "url": "https://httpbin.org/anything"
}

# response for user 2:

{
    "message": "hello"
}

# request snaphots:

 * https://httpbin.org/anything - 27998400b033ee02f437700839238fb5f6f1d9d3
 * https://httpbin.org/anything - 7f963daf2af5a559a14be24f80a30ff5b30245d9

# env snaphots:

 * HOST_NAME=https://httpbin.org/anything
