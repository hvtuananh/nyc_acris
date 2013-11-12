def addr_filter(str):
    return str not in "st street ave avenue av place pl parkway pkwy".split()
    
print filter(addr_filter, "1701 kick st".split())