Name:          nginx-log-collector
Version:       0.2
Release:       1
Summary:       nginx-log-collector
License:       ASL 2.0
Source0:       nginx-log-collector.service
Source1:       config.yaml
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
cd $GOPATH/src/github.com/avito-tech/nginx-log-collector
ls $GOPATH/src/github.com/avito-tech/nginx-log-collector
make build
cd build
cp nginx-log-collector ../../../../../../nginx-log-collector

%install
install -d %{buildroot}%{_bindir}
install -p -m 0755 nginx-log-collector %{buildroot}%{_bindir}/nginx-log-collector
install -d %{buildroot}/etc/nginx-log-collector
cp %{SOURCE1} %{buildroot}/etc/nginx-log-collector/config.yaml
%if %{use_systemd}
%{__mkdir} -p %{buildroot}%{_unitdir}
%{__install} -m644 %{SOURCE0} \
    %{buildroot}%{_unitdir}/nginx-log-collector.service
%endif

%pre
/usr/bin/getent group nginx-log-collector > /dev/null || /usr/sbin/groupadd -r nginx-log-collector
/usr/bin/getent passwd nginx-log-collector > /dev/null || /usr/sbin/useradd -r -d /usr/lib/nginx-log-collector -s /bin/bash -g nginx-log-collector nginx-log-collector

%post
%if %use_systemd
/usr/bin/systemctl daemon-reload
%endif

%preun
%if %use_systemd
/usr/bin/systemctl stop nginx-log-collector
%endif

%postun
%if %use_systemd
/usr/bin/systemctl daemon-reload
%endif

%files
%defattr(-,nginx-log-collector,nginx-log-collector,-)
%{_bindir}/nginx-log-collector
/etc/nginx-log-collector/config.yaml
%if %{use_systemd}
%{_unitdir}/nginx-log-collector.service
%endif
