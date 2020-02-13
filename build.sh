#!/bin/bash

list_dependencies=(rpm-build rpmdevtools)

for i in ${list_dependencies[*]}
do
    if ! rpm -qa | grep -qw $i; then
        echo "__________Dont installed '$i'__________"
        #yum -y install $i
    fi
done

mkdir -p ./{RPMS,SRPMS,BUILD,SOURCES,SPECS}
cp nginx-log-collector.service SOURCES
spectool -g -C SOURCES nginx-log-collector.spec
rpmbuild --quiet --define "_topdir `pwd`" -bb nginx-log-collector.spec
