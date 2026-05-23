%global realname mod_maxminddb
%global realver  1.3.0
%global srcext   tar.gz

# turn off the generation of debuginfo rpm
%global debug_package %{nil}

%if 0%{?suse_version}
%define APXS apxs2
%else
%define APXS apxs
%endif

%global MOD_DIR %(%{APXS} -q LIBEXECDIR)

# Common info
%if 0%{?suse_version}
Name:          apache2-%{realname}
%else
Name:          %{realname}
%endif
Version:       %{realver}
Release:       1.72%{?dist}
License:       Apache-2.0
URL:           http://maxmind.github.io/mod_maxminddb/
Summary:       MaxMind DB Apache Module

# Build-time parameters
BuildRequires: libmaxminddb-devel
%if 0%{?suse_version}
BuildRequires: apache2-devel
%else
BuildRequires: httpd-devel
%endif
Source:        https://github.com/maxmind/%{realname}/releases/download/%{version}/%{realname}-%{version}%{?extraver}.%{srcext}

%description
This module allows you to query MaxMind DB files from Apache 2.2+ using
the libmaxminddb library.

# Preparation step (unpacking and patching if necessary)
%prep
%setup -q -n %{realname}-%{version}%{?extraver}

%build
export PATH=${PATH}:/sbin:/usr/sbin
%configure \
 CFLAGS="%{optflags}" \
 LDFLAGS="-Wl,--as-needed -Wl,--strip-all"
%{__make} %{?_smp_mflags}

%install
%{__install} -D -m755 src/.libs/%{realname}.so %{buildroot}%{MOD_DIR}/%{realname}.so

%files
%doc LICENSE README.md
%{MOD_DIR}/%{realname}.so

%changelog
* Fri May 22 2026 CasjaysDev <rpm-devel@casjaysdev.pro> - 1.3.0-1
- Fix spec violations: %global for constants, use %{buildroot}

* Fri Apr 24 2026 CasjaysDev <rpm-devel@casjaysdev.pro> - 1.3.0-1
- Update to 1.3.0
- Modernize spec for AlmaLinux 10; remove BuildRoot, Group, %clean, %defattr

* Tue Dec 20 2016 aevseev@gmail.com
- New upstream version - 1.1.0
