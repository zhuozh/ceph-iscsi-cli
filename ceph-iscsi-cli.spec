Name:		ceph-iscsi-cli
Version:	2.5
Release:	6%{?dist}
Summary:	CLI configuration tool to manage multiple iSCSI gateways
Group:		Applications/System
License:	GPLv3

URL:		https://github.com/pcuzner/ceph-iscsi-cli
Source0:	https://github.com/pcuzner/%{name}/archive/%{version}/%{name}-%{version}.tar.gz
BuildArch:  noarch

BuildRequires: python2-devel
BuildRequires: python-setuptools
BuildRequires: systemd

Requires: python-rtslib >= 2.1
Requires: ceph-iscsi-config >= 2.3
Requires: python-requests >= 2.6
Requires: python-configshell >= 1.1
Requires: python-flask >= 0.10.1
Requires: pyOpenSSL >= 0.13

%description
This package provides a CLI interface similar to the targetcli tool used to
interact with the kernel LIO subsystem. The rpm installs two components; a CLI
shell (based on configshell) and an API service called rbd-target-api.

The CLI orchestrates iscsi configuration changes through the API service
running on EACH gateway node. The API service uses the same configuration
settings file '/var/lib/ceph/etc/ceph/iscsi-gateway.cfg' as the rbd-target-gw service.

You should ensure that the 'cfg' file is consistent across gateways for
predictable behaviour.

%prep
%setup -q 

%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build


%install
%{__python} setup.py install --skip-build --root %{buildroot} --install-scripts %{_bindir}
mkdir -p %{buildroot}%{_unitdir}
install -m 0644 .%{_unitdir}/rbd-target-api.service %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_mandir}/man8
install -m 0644 gwcli.8 %{buildroot}%{_mandir}/man8/
gzip %{buildroot}%{_mandir}/man8/gwcli.8
mkdir -p %{buildroot}%{_sysconfdir}/systemd/system/rbd-target-gw.service.d
install -m 0644 .%{_sysconfdir}/systemd/system/rbd-target-gw.service.d/dependencies.conf %{buildroot}%{_sysconfdir}/systemd/system/rbd-target-gw.service.d/

%post
/bin/systemctl --system daemon-reload &> /dev/null || :
/bin/systemctl --system enable rbd-target-api &> /dev/null || :

%postun
/bin/systemctl --system daemon-reload &> /dev/null || :

%files
%doc README
%doc LICENSE
%{_bindir}/gwcli
%{_bindir}/rbd-target-api
%{_unitdir}/rbd-target-api.service
%{_sysconfdir}/systemd/system/rbd-target-gw.service.d
%{python2_sitelib}/*
%{_mandir}/man8/gwcli.8.gz

%changelog
* Tue Jun 12 2018 Zhuoyu Zhang <zhangzhuoyu@cmss.chinamobile.com> 2.5-6
- utils: fix bug in clients_logged_in
- raise exception when executor not in gateway list
- fix bug in logged_in

* Fri May 25 2018 Zhuoyu Zhang <zhangzhuoyu@cmss.chinamobile.com> 2.5-5
- let get_available_ips return a dictionary of ip and hostname

* Wed May 23 2018 Zhuoyu Zhang <zhangzhuoyu@cmss.chinamobile.com> 2.5-4
- return hostname with available ip
- fix spelling error messsge to message

* Mon May 21 2018 Zhuoyu Zhang <zhangzhuoyu@cmss.chinamobile.com> 2.5-3
- bump version to 2.5-3
- fix snap shot bugs
- for tianji
- support multiple target
- bypass version check
- do not check gateway list in requires_restricted_auth
- remove restricted on ONE iSCSI target

* Mon Sep 04 2017 Paul Cuzner <pcuzner@redhat.com> 2.5-2
- automatically check state of gateways every 5 seconds
- hostgroup logic updated
- added an isalive api endpoint to check state of gateways
- abort any change request, when there are offline iscsi gateways

* Tue Aug 15 2017 Jason Dillaman <dillaman@redhat.com> 2.5-1
- version bump to 2.5

* Sat Jan 21 2017 Paul Cuzner <pcuzner@redhat.com> 2.1-1
- updated for TCMU support (krbd/device mapper support removed)
- rbd-target-api restructured to remove python-flask-restful dependency
- api endpoints available through a get /api call
- spec updated for pyOpenSSL dependency (used by API)
- added feature text to disk info command instead of just a feature code (int)
- automatically select TLS version based on version of werkzeug
- disk resize and info now available from the upper level 'disks' section
- requested commands echo'd to the log file improving audit record
- add gateways refresh command
- fix: disk resize now changes all related entries in the tree
- ceph clusters are populated automatically through presence in /var/lib/ceph/etc/ceph
- added ceph cluster name to disk info output
- 'ansible' mode exports decrypt chap passwords automatically
- cli installation binds rbd-target-api to the unit state of rbd-target-gw
- workflow: switch dir to newly created client to speed up client definition
- workflow: non-existent disk gets autodefined within the client dialog
- gateway health determined using iscsi port AND api port state

* Thu Jan 5 2017 Paul Cuzner <pcuzner@redhat.com> 2.0-1
- initial rpm packaging


