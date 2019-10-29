#!/usr/bin/env bash

set -eu
set -o pipefail

# Global stuff
CFLAGS='-O2 -Wall'

pcre_version="8.43"
export PCREDIR="$(pwd)/pcre-${pcre_version}/pcre-bin"
if [ ! -d pcre-${pcre_version}  ] ; then
    echo "Downloading PCRE tarball..."
    wget https://ftp.pcre.org/pub/pcre/pcre-${pcre_version}.tar.gz -O pcre.tar.gz
    tar xzvf pcre.tar.gz -C .
    rm pcre.tar.gz
fi
if [ ! -d "$PCREDIR" ] ; then
    echo "Building PCRE ${pcre_version}"
    cd pcre-${pcre_version}
    ./configure --prefix=$PCREDIR --disable-shared
    make && make install
    cd ..
fi


haproxy_version="2.0.8"
HAPROXYDIR="$(pwd)/haproxy-${haproxy_version}/haproxy-bin"
if [ ! -d "haproxy-$haproxy_version" ] ; then
    echo "Download HAproxy tarball..."
    wget http://www.haproxy.org/download/2.0/src/haproxy-${haproxy_version}.tar.gz -O haproxy.tar.gz
    tar xzvf haproxy.tar.gz -C .
    rm haproxy.tar.gz
fi
cd haproxy-${haproxy_version}
echo "Building HAproxy ${haproxy_version}"
make \
    PCREDIR=$PCREDIR \
    USE_STATIC_PCRE=1 \
    USE_REGPARM=1 \
    USE_OPENSSL=1 \
    USE_ZLIB=1 \
    DESTDIR=$HAPROXYDIR \
    TARGET=linux-glibc
make \
    TARGET=linux-glibc \
    DESTDIR=$HAPROXYDIR \
    install
