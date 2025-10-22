def autodecode(string, encoding="gbk"):
    return string.decode(encoding) if isinstance(string, bytes) else string