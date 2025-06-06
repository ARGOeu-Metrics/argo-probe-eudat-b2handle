Name:		argo-probe-eudat-b2handle
Version:	1.1
Release:	0%{?dist}
Summary:	Monitoring Metrics for B2HANDLE 
License:	GPLv3+
Packager:	Kyriakos Gkinis <kyrginis@admin.grnet.gr>

Source:		%{name}-%{version}.tar.gz
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}

Requires:	python3
Requires:	python3dist(pyhandle)
Requires:	perl-interpreter
Requires:	perl-JSON

# Create an option to build with epic api probe, default is without
%bcond_with epicapi

%if %{with epicapi}
BuildRequires:	python3-devel
Requires:	python3-lxml
Requires:	python3-defusedxml
Requires:	python3-httplib2
Requires:	python3-simplejson
%endif

%description
Monitoring metrics to check functionality of Handle service and EPIC API

%prep
%setup -q

%define _unpackaged_files_terminate_build 0 

%install

install -d %{buildroot}/%{_libexecdir}/argo/probes/eudat-b2handle
install -m 755 check_handle_resolution.pl %{buildroot}/%{_libexecdir}/argo/probes/eudat-b2handle/check_handle_resolution.pl
install -m 644 check_handle_api.py %{buildroot}%{_libexecdir}/argo/probes/eudat-b2handle/check_handle_api.py
%if %{with epicapi}
install -m 755 check_epic_api.py %{buildroot}/%{_libexecdir}/argo/probes/eudat-b2handle/check_epic_api.py
install -m 644 epicclient.py %{buildroot}%{_libexecdir}/argo/probes/eudat-b2handle/epicclient.py
%py_byte_compile %{__python3} %{buildroot}%{_libexecdir}/argo/probes/eudat-b2handle/epicclient.py
%endif

%files
%dir /%{_libexecdir}/argo
%dir /%{_libexecdir}/argo/probes/
%dir /%{_libexecdir}/argo/probes/eudat-b2handle

%attr(0755,root,root) /%{_libexecdir}/argo/probes/eudat-b2handle/check_handle_resolution.pl
%attr(0755,root,root) /%{_libexecdir}/argo/probes/eudat-b2handle/check_handle_api.py
%if %{with epicapi}
%attr(0755,root,root) /%{_libexecdir}/argo/probes/eudat-b2handle/check_epic_api.py
%attr(0755,root,root) /%{_libexecdir}/argo/probes/eudat-b2handle/epicclient.py
%attr(0644,root,root) /%{_libexecdir}/argo/probes/eudat-b2handle/__pycache__
%endif

%pre

%changelog
* Fri May 2 2025 Kyriakos Gkinis <kyrginis@admin.grnet.gr> - 1.1-0
- Handle API probe adds UUID string to test handle name

* Thu Apr 18 2024 Kyriakos Gkinis <kyrginis@admin.grnet.gr> - 1.0-0
- Added support for python3
- Handle API probe uses pyhandle library instead of b2handle
- Handle API probe prints more debugging output when called with --debug
- EPIC API probe is optional

* Mon Mar 14 2022 Themis Zamani <themiszamani@gmail.com> - 0.9-4
- Update package prerequisites based on argo monitoring. 
  
* Wed Mar 24 2021 Kyriakos Gkinis <kyrginis@admin.grnet.gr> - 0.9-3
- Add dependency on b2handle rpm, remove pip preinstall command

* Mon Sep 07 2020 Kyriakos Gkinis <kyrginis@admin.grnet.gr> - 0.9-2
- Include python2-pip dependency and b2handle library preinstall command only in el7 RPMs
* Thu Sep 03 2020 Kyriakos Gkinis <kyrginis@admin.grnet.gr> - 0.9-1
- Catch SSLError exception and exit with code CRITICAL
* Wed Apr 17 2019 Kyriakos Gkinis <kyrginis@admin.grnet.gr> - 0.8-1
- Add python2-pip dependency
- Add preinstall command to pip install b2handle library
* Thu Jan 17 2019 Kyriakos Gkinis <kyrginis@admin.grnet.gr> - 0.7-1
- check_handle_resolution.pl : Updated version that works with HS_SERV values
* Thu Oct 4 2018 Kyriakos Gkinis <kyrginis@admin.grnet.gr> - 0.6-1
- Add configuration directory /etc/nagios/plugins/
* Thu Jan 12 2017 Kyriakos Gkinis <kyrginis@admin.grnet.gr> - 0.5-1
- Add check_handle_api.py probe for Handle v8 REST API
- Change installation directory name to eudat-b2handle
* Wed Feb 3 2016 Christos Kanellopoulos <skanct@gmail.com> - 0.4-1
- New package version
* Fri Jan 15 2016 Kyriakos Gkinis <kyrginis@admin.grnet.gr> - 0.1-1
- Initial version of the package
