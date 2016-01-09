#PYTHON 2.7

import os

from struct import unpack,pack

def size(fn):

    length=os.path.getsize(fn)

    return length

fn = 'resource.car'

f=open(fn,'rb')

magic = f.read(4)

fsize=size(fn)

if magic == '\x72\x61\x63\x01':

    namelst=[]

    offsetlst=[]

    f.seek(0x8)

    p=open('resource.car.txt','wb')

    index_size = unpack('I',f.read(4))[0]

    num = unpack('I',f.read(4))[0]

    for i in xrange(num):

        (mark,offset,name_size)=unpack('3I',f.read(0xc))

        name=f.read(name_size)

        if name_size%4==0:

            blank_size=0x4

        else:

            blank_size=4-name_size%4

        blank = f.read(blank_size)

        print('%d|%08x|%08x|%d\r\n'%(mark,offset,name_size,blank_size))

        namelst.append(name)

        offsetlst.append(offset)

    offsetlst.append(fsize)

    for i in xrange(num):

        dsize = offsetlst[i+1]-offsetlst[i]

        f.seek(offsetlst[i])

        (unk2,asize,size) = unpack('3I',f.read(0xc))

        p.write('%08x|%08x|%s|\r\n'%(offsetlst[i]+0xc,size,namelst[i]))

        dat = f.read(size)

        dest = open('resource//%s'%namelst[i],'wb')

        dest.write(dat)

        dest.close()

    p.close()

f.close()