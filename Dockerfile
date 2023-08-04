from quay.io/centos/centos:stream8

ARG PIP_INDEX_URL=http://mirrors.aliyun.com/pypi/simple/
ARG PIP_TRUSTED_HOST=mirrors.aliyun.com
ARG MIRROR_BASE=http://mirrors.aliyun.com

LABEL name="co"

# basic packages
RUN rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-centosofficial \
    && sed -i -e '/^mirrorlist/d' \
        -e "s|^#\?baseurl=http://mirror.centos.org|baseurl=${MIRROR_BASE}|" /etc/yum.repos.d/*.repo \
    && sed -i -e '/^mirrorlist/d' \
        -e "s|^#\?baseurl=http://mirror.centos.org|baseurl=${MIRROR_BASE}|" /etc/yum.repos.d/*.repo \
    && dnf --enablerepo=powertools -y update \
    && dnf --enablerepo=powertools install -y \
        expect \
        git \
        mysql-libs \
        procps-ng \
        python39 \
        sudo \
        unzip \
    && dnf clean all


ADD . /app
WORKDIR /app

# install co requirements
RUN BUILD_DEP_PKGS=" \
        cpp \
        gcc \
        glibc-devel \
        glibc-headers \
        kernel-headers \
        keyutils-libs-devel \
        krb5-devel \
        libcom_err-devel \
        libffi-devel \
        libjpeg-turbo-devel \
        libsepol-devel \
        libverto-devel \
        libxcrypt-devel \
        mysql-devel \
        openssl-devel \
        pcre2-devel \
        platform-python-devel \
        python39-devel \
        zlib-devel \
        " \
    && dnf -y install $BUILD_DEP_PKGS \
    && pip3 install --no-cache-dir --upgrade pip \
    && pip3 install --no-cache-dir -r requirements.txt \
    && dnf -y remove $BUILD_DEP_PKGS \

