from scrapy import cmdline

if __name__ == '__main__':
    command = "scrapy crawl spider".split()
    cmdline.execute(command)