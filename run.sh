#!/bin/sh
scrapy crawl wangyiyun -s JOBDIR=cache -s LOG_LEVEL=INFO > run.log 2>&1
