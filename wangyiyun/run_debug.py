# coding: utf-8

from scrapy import cmdline

if __name__ == '__main__':
    name = 'artist_spider'
    cmd = 'scrapy crawl ' + name
    cmd = cmd + ' -s LOG_LEVEL=WARNING'
    cmd = cmd + ' -s JOBDIR=cache'
    print("execute cmd: ", cmd)
    cmdline.execute(cmd.split())