%define realname mod_maxminddb
%define realver  1.1.0
%define srcext   tar.gz

# turn off the generation of debuginfo rpm  (RH9) ??
%global debug_package %{nil}

%if 0%{?suse_version}
%define APXS apxs2
%else
%define APXS apxs
%endif

%define MOD_DIR %(%{APXS} -q LIBEXECDIR)

# Common info
%if 0%{?suse_version}
Name:          apache2-%{realname}
%else
Name:          %{realname}
%endif
Version:       %{realver}
Release:       1.72%{?dist}
License:       Apache-2.0
Group:         Productivity/Networking/Web/Servers
URL:           http://maxmind.github.io/mod_maxminddb/
Summary:       MaxMind DB Apache Module

# Build-time parameters
BuildRequires: libmaxminddb-devel
%if 0%{?suse_version}
BuildRequires: apache2-devel
%else
BuildRequires: httpd-devel
%endif
BuildRoot:     %{_tmppath}/%{name}-root
Source:        https://github.com/maxmind/%{realname}/releases/download/%{version}/%{realname}-%{version}%{?extraver}.%{srcext}

%description
This module allows you to query MaxMind DB files from Apache 2.2+ using
the libmaxminddb library.

# Preparation step (unpackung and patching if necessary)
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

%clean
[ "%{buildroot}" != "/" ] && %{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%doc LICENSE README.md
%{MOD_DIR}/%{realname}.so

%changelog
* Tue Dec 20 2016 aevseev@gmail.com
- New upstream version - 1.1.0
