%global realname mod_maxminddb
%global realver  1.3.0
%global srcext   tar.gz

%global debug_package %{nil}

%if 0%{?suse_version}
%global httpd_devel_pkg apache2-devel
%global httpd_pkg apache2
%global httpd_moddir %{_libdir}/apache2
%else
%global httpd_devel_pkg httpd-devel
%global httpd_pkg httpd
%{!?_httpd_moddir: %global _httpd_moddir %{_libdir}/httpd/modules}
%global httpd_moddir %{_httpd_moddir}
%{!?_httpd_mmn: %global _httpd_mmn %(cat %{_includedir}/httpd/.mmn 2>/dev/null || echo 0-0)}
%endif

Name:          %{realname}
Version:       %{realver}
Release:       4%{?dist}
License:       Apache-2.0
URL:           https://maxmind.github.io/mod_maxminddb/
ExclusiveArch: x86_64 aarch64
Summary:       MaxMind DB Apache Module
Source:        https://github.com/maxmind/%{realname}/releases/download/%{version}/%{realname}-%{version}.%{srcext}

BuildRequires: gcc, make
BuildRequires: libmaxminddb-devel
BuildRequires: %{httpd_devel_pkg}
%if 0%{?suse_version}
Requires:      %{httpd_pkg}
%else
Requires:      httpd-mmn = %{_httpd_mmn}
%endif

%description
This module allows you to query MaxMind DB files from Apache 2.2+ using
the libmaxminddb library.

%prep
%autosetup -p1 -n %{realname}-%{version}

%build
export PATH=${PATH}:/sbin:/usr/sbin
apxs_ldflags=$(printf '%s\n' '%{?build_ldflags}' | tr ' ' '\n' | grep '^-Wl,' | tr '\n' ' ')
%configure \
 CFLAGS="%{optflags}" \
 LDFLAGS="$apxs_ldflags -Wl,--as-needed"
%make_build

%install
install -D -m755 src/.libs/%{realname}.so %{buildroot}%{httpd_moddir}/%{realname}.so

%files
%license LICENSE
%doc README.md
%{httpd_moddir}/%{realname}.so

%changelog
* Tue Sep 29 2026 CasjaysDev <rpm-devel@casjaysdev.pro> - 1.3.0-4
- Preserve RPM linker flags accepted by apxs and filter compiler-only options

* Mon Sep 28 2026 CasjaysDev <rpm-devel@casjaysdev.pro> - 1.3.0-2
- Use distro-specific Apache module directories without executing apxs during
  spec parsing
- Require the matching Apache runtime package or httpd module magic number
- Preserve RPM linker hardening flags instead of stripping the module at link
  time

* Sun Jul 05 2026 CasjaysDev <rpm-devel@casjaysdev.pro> - 1.3.0-1
- Guard httpd-devel BuildRequires: openSUSE/SLES use apache2-devel, not
  httpd-devel; added %%if 0%%{?suse_version} conditional via %%httpd_devel_pkg.
  Verified libmaxminddb-devel is named identically on openSUSE (no guard
  needed); ExclusiveArch already correct, no stray BuildArch/noarch found,
  no EL7 macro gaps found

* Sun Jul 05 2026 CasjaysDev <rpm-devel@casjaysdev.pro> - 1.3.0-1
- URL: http→https; remove OpenSUSE conditionals; fix Release tag; install macro
- Source0 verified 302→200; 1.3.0 is current

* Fri Jul 03 2026 CasjaysDev <rpm-devel@casjaysdev.pro> - 1.3.0-1
- Add ExclusiveArch: x86_64 aarch64; %%autosetup -p1; %%make_build; %%license LICENSE

* Fri May 22 2026 CasjaysDev <rpm-devel@casjaysdev.pro> - 1.3.0-1
- Fix spec violations: %global for constants, use %{buildroot}

* Fri Apr 24 2026 CasjaysDev <rpm-devel@casjaysdev.pro> - 1.3.0-1
- Update to 1.3.0
- Modernize spec for AlmaLinux 10; remove BuildRoot, Group, %clean, %defattr

* Tue Dec 20 2016 aevseev@gmail.com
- New upstream version - 1.1.0
