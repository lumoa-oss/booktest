# description:

in this description, it's assumed that user id is significant. 
this test should create 2 snapshots, one for each user

note: you may need to freeze this twice, because on first run 2 different calls
are made for user 1, but only snapshot is stored. recalling first run is necesssary,
because otherwise the system may get stuck on timeouts. this will cause the result to
be different on second run, as in first run 2 calls are done, while on second run
one snapshot is used twice.

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
        "X-Amzn-Trace-Id": "Root=1-68dfb3b7-7675352f3ac0ad5f737c0346",
        "X-Api-Key": "mock",
        "X-Timestamp": "1759490999.1804047",
        "X-User-Id": "1"
    },
    "json": {
        "message": "hello"
    },
    "method": "POST",
    "origin": "85.131.27.192",
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
        "X-Amzn-Trace-Id": "Root=1-68dfb3b8-00fe79c40f2a7e672274e938",
        "X-Api-Key": "mock",
        "X-Timestamp": "1759491000.1399927",
        "X-User-Id": "1"
    },
    "json": {
        "message": "hello"
    },
    "method": "POST",
    "origin": "85.131.27.192",
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
        "User-Agent": "python-requests/2.32.3",
        "X-Amzn-Trace-Id": "Root=1-68dfb3b9-3733fff24ff432560578df49",
        "X-Api-Key": "mock",
        "X-Timestamp": "1759491001.3160596",
        "X-User-Id": "2"
    },
    "json": {
        "message": "hello"
    },
    "method": "POST",
    "origin": "85.131.27.192",
    "url": "https://httpbin.org/anything"
}
