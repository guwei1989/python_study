#!/usr/bin/env python
# coding:utf-8

import mmap
import os

mmap_file = None


##从内存中读取信息，
def read_mmap_info():
    global mmap_file
    mmap_file.seek(0)
    ##把二进制转换为字符串
    info_str = mmap_file.read(1).translate(None, b'\x00').decode()
    info_str = info_str.strip()
    print("**********{info}".format(info=info_str))


##如果内存中没有对应信息，则向内存中写信息以供下次调用使用
def get_mmap_info(fileno):
    global mmap_file
    ##第二个参数1024是设定的内存大小，单位：字节。如果内容较多，可以调大一点
    mmap_file = mmap.mmap(fileno, 256, access=mmap.ACCESS_WRITE, tagname='share_mmap')
    ##读取有效比特数，不包括空比特
    cnt = mmap_file.read_byte()
    print cnt
    if len(cnt) == 0:
        print("Load data to memory")
        mmap_file = mmap.mmap(0, 256, access=mmap.ACCESS_WRITE, tagname='share_mmap')
        mmap_file.write(b"This is the test data")
    else:
        print("The data is in memory")
        read_mmap_info()


##修改内存块中的数据
def reset_mmp_info():
    global mmap_file
    mmap_file.seek(0)
    mmap_file.write(b'\x00')
    mmap_file.write(b"Load data to memory agine")


if __name__ == "__main__":
    with open('copy_test.py', 'r+') as f:
        f_no = f.fileno()
        get_mmap_info(f_no)

