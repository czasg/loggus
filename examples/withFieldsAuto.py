# coding: utf-8
import loggus.pci

packageName = "loggus"
indexPage = loggus.pci.__index_page__
packageVersion = loggus.pci.__version__
author = loggus.pci.__author__
authorEmail = loggus.pci.__email__

if __name__ == '__main__':
    # single-line
    loggus.withFieldsAuto(packageName, indexPage, packageVersion, authorEmail, ).info("0.0")
    # multi line
    loggus.withFieldsAuto(
        packageName,
        indexPage,
        packageVersion,
        authorEmail,
    ).info("0.0")
