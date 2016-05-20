# FIXME Follow https://fedoraproject.org/wiki/Packaging:Python
%define is_el7 %(test 0%{?centos} -eq 07 || test 0%{?rhel} -eq 07 && echo 1 || echo 0)

Name:           imgbased
Version:        0.6
Release:        %{?_release}%{?!_release:0.1}%{?dist}
Summary:        Tools to work with an image based rootfs

License:        GPLv2+
URL:            https://www.github.com/fabiand/imgbased
Source0:        %{name}-%{version}.tar.xz

BuildArch:      noarch

# Skips check since rhel default repos lack pep8, pyflakes and python-nose
%if ! 0%{?rhel}
%{!?with_check:%global with_check 1}
%else
%{!?with_check:%global with_check 0}
%endif

BuildRequires:       make
BuildRequires:       automake autoconf
BuildRequires:       rpm-build
BuildRequires:       git
BuildRequires:       asciidoc

BuildRequires:       python-devel python-six

%if 0%{?with_check}
BuildRequires:       python-pep8 pyflakes python-nose
%endif

BuildRequires:       rpm-python

%if 0%{?is_el7}
BuildRequires:       python-six
%else
BuildRequires:       python3-six
BuildRequires:       python3-devel
%endif

Requires:       lvm2
Requires:       util-linux
Requires:       augeas
Requires:       rsync


%description
This tool enforces a special usage pattern for LVM.
Basically this is about having read-only bases and writable
layers atop.


%prep
%setup -q


%build
%configure
make %{?_smp_mflags}


%install
%if 0%{?fedora}
install -Dm 0644 src/plugin-dnf/imgbased-warning.py \
                 %{buildroot}/%{python3_sitelib}/dnf-plugins/imgbased-warning.py
%else
install -Dm 0644 src/plugin-yum/imgbased-warning.py \
                 %{buildroot}/%{_prefix}/lib/yum-plugins/imgbased-warning.py
install -Dm 0644 src/plugin-yum/imgbased-warning.conf \
                 %{buildroot}/%{_sysconfdir}/yum/pluginconf.d/imgbased-warning.conf
%endif
%make_install


%files
%doc README.md LICENSE
%{_sbindir}/imgbase
%{_datadir}/%{name}/hooks.d/
%{python_sitelib}/%{name}/
%{_mandir}/man8/imgbase.8*
/%{_docdir}/%{name}/*.asc
%if 0%{?fedora}
%{python3_sitelib}/dnf-plugins/imgbased-warning.py*
%{python3_sitelib}/dnf-plugins/__pycache__/imgbased*
%else
%{_sysconfdir}/yum/pluginconf.d/imgbased-warning.conf
%{_prefix}/lib/yum-plugins/imgbased-warning.py*
%endif

%changelog
* Wed Apr 02 2014 Fabian Deutsch <fabiand@fedoraproject.org> - 0.1-0.1
- Initial package
