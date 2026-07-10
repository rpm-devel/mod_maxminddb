%global realname mod_maxminddb
%global realver  1.3.0
%global srcext   tar.gz

%global debug_package %{nil}

%global MOD_DIR %(apxs -q LIBEXECDIR)

%if 0%{?suse_version}
%global httpd_devel_pkg apache2-devel
%else
%global httpd_devel_pkg httpd-devel
%endif

Name:          %{realname}
Version:       %{realver}
Release:       1%{?dist}
License:       Apache-2.0
URL:           https://maxmind.github.io/mod_maxminddb/
ExclusiveArch: x86_64 aarch64
Summary:       MaxMind DB Apache Module
Source:        https://github.com/maxmind/%{realname}/releases/download/%{version}/%{realname}-%{version}.%{srcext}

BuildRequires: libmaxminddb-devel
BuildRequires: %{httpd_devel_pkg}

%description
This module allows you to query MaxMind DB files from Apache 2.2+ using
the libmaxminddb library.

%prep
%autosetup -p1 -n %{realname}-%{version}

%build
export PATH=${PATH}:/sbin:/usr/sbin
%configure \
 CFLAGS="%{optflags}" \
 LDFLAGS="-Wl,--as-needed -Wl,--strip-all"
%make_build

%install
install -D -m755 src/.libs/%{realname}.so %{buildroot}%{MOD_DIR}/%{realname}.so

%files
%license LICENSE
%doc README.md
%{MOD_DIR}/%{realname}.so

%changelog
* Sat Jul 05 2026 CasjaysDev <rpm-devel@casjaysdev.pro> - 1.3.0-1
- Guard httpd-devel BuildRequires: openSUSE/SLES use apache2-devel, not
  httpd-devel; added %%if 0%%{?suse_version} conditional via %%httpd_devel_pkg.
  Verified libmaxminddb-devel is named identically on openSUSE (no guard
  needed); ExclusiveArch already correct, no stray BuildArch/noarch found,
  no EL7 macro gaps found

* Sat Jul 05 2026 CasjaysDev <rpm-devel@casjaysdev.pro> - 1.3.0-1
- URL: http→https; remove OpenSUSE conditionals; fix Release tag; install macro
- Source0 verified 302→200; 1.3.0 is current

* Thu Jul 03 2026 CasjaysDev <rpm-devel@casjaysdev.pro> - 1.3.0-1
- Add ExclusiveArch: x86_64 aarch64; %%autosetup -p1; %%make_build; %%license LICENSE

* Fri May 22 2026 CasjaysDev <rpm-devel@casjaysdev.pro> - 1.3.0-1
- Fix spec violations: %global for constants, use %{buildroot}

* Fri Apr 24 2026 CasjaysDev <rpm-devel@casjaysdev.pro> - 1.3.0-1
- Update to 1.3.0
- Modernize spec for AlmaLinux 10; remove BuildRoot, Group, %clean, %defattr

* Tue Dec 20 2016 aevseev@gmail.com
- New upstream version - 1.1.0
