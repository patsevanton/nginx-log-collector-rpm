Name:          nginx-log-collector
Version:       0.1
Release:       1
Summary:       nginx-log-collector
License:       ASL 2.0 
Source0:       nginx-log-collector.service
Source1:       config.yml
BuildRequires: golang
BuildRequires: make
BuildRequires: tree
Requires(pre): /usr/sbin/useradd, /usr/bin/getent
Requires(postun): /usr/sbin/userdel

# Use systemd for fedora >= 18, rhel >=7, SUSE >= 12 SP1 and openSUSE >= 42.1
%define use_systemd (0%{?fedora} && 0%{?fedora} >= 18) || (0%{?rhel} && 0%{?rhel} >= 7) || (!0%{?is_opensuse} && 0%{?suse_version} >=1210) || (0%{?is_opensuse} && 0%{?sle_version} >= 120100)

%if %use_systemd
BuildRequires: systemd
%endif

%description
nginx-log-collector

%build
export GOPATH=%{_builddir}/_build
echo $GOPATH
mkdir -p $GOPATH/src/github.com/avito-tech/
git clone https://github.com/avito-tech/nginx-log-collector.git $GOPATH/src/github.com/avito-tech/nginx-log-collector
pwd
ls
cd $GOPATH/src/github.com/avito-tech/nginx-log-collector
ls $GOPATH/src/github.com/avito-tech/nginx-log-collector
make build
ls
pwd
tree

#%install
#install -d %{buildroot}%{_bindir}
#install -p -m 0755 nginx-clickhouse %{buildroot}%{_bindir}/nginx-clickhouse
#install -d %{buildroot}/etc/nginx-clickhouse
#install -d %{buildroot}/etc/nginx-clickhouse/config
#ls
#pwd
#cp %{SOURCE1} %{buildroot}/etc/nginx-clickhouse/config/config.yml
#%if %{use_systemd}
#%{__mkdir} -p %{buildroot}%{_unitdir}
#%{__install} -m644 %{SOURCE0} \
#    %{buildroot}%{_unitdir}/nginx-clickhouse.service
#%endif

#%pre
#/usr/bin/getent group nginx-clickhouse > /dev/null || /usr/sbin/groupadd -r nginx-clickhouse
#/usr/bin/getent passwd nginx-clickhouse > /dev/null || /usr/sbin/useradd -r -d /usr/lib/nginx-clickhouse -s /bin/bash -g nginx-clickhouse nginx-clickhouse
#
#%post
#%if %use_systemd
#/usr/bin/systemctl daemon-reload
#%endif
#
#%preun
#%if %use_systemd
#/usr/bin/systemctl stop nginx-clickhouse
#%endif
#
#%postun
#%if %use_systemd
#/usr/bin/systemctl daemon-reload
#%endif
#
#%files
#%defattr(-,nginx-clickhouse,nginx-clickhouse,-)
#%{_bindir}/nginx-clickhouse
#/etc/nginx-clickhouse/config/config.yml
#%if %{use_systemd}
#%{_unitdir}/nginx-clickhouse.service
#%endif
