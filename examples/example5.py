import loggus

if __name__ == '__main__':
    loggus.info()
    loggus.info("hello", "world")
    loggus.info({"hello": "world"})
    loggus.info({"hello": "world"}, "o")
    loggus.info("hello world", {"hello": "world"}, ["hello", "world"], {"hello", "world"}, ("hello", "world"))
