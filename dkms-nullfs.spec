%global debug_package %{nil}
%global dkms_name nullfs

Name:       dkms-%{dkms_name}
Version:    0.18
Release:    2%{?dist}
Summary:    A virtual file system that behaves like /dev/null
License:    GPLv3+
URL:        https://github.com/abbbi/nullfsvfs
BuildArch:  noarch

Source0:    %{url}/archive/v%{version}.tar.gz#/nullfsvfs-%{version}.tar.gz
Source1:    %{name}.conf
%if 0%{?rhel} == 9
# https://github.com/abbbi/nullfsvfs/commit/63661607ded4e3ee0ba35cf50e1166a2b203daeb
Patch0:     nullfs-el9.patch
%endif

BuildRequires:  sed

Provides:   %{dkms_name}-kmod = %{?epoch:%{epoch}:}%{version}
Requires:   %{dkms_name}-kmod-common = %{?epoch:%{epoch}:}%{version}
Requires:   dkms

%description
A virtual file system that behaves like /dev/null. It can handle regular file
operations but writing to files does not store any data. The file size is
however saved, so reading from the files behaves like reading from /dev/zero
with a fixed size.

Writing and reading is basically an NOOP, so it can be used for performance
testing with applications that require directory structures.

%prep
%autosetup -p1 -n nullfsvfs-%{version}

cp -f %{SOURCE1} dkms.conf

sed -i -e 's/__VERSION_STRING/%{version}/g' dkms.conf

%build

%install
# Create empty tree:
mkdir -p %{buildroot}%{_usrsrc}/%{dkms_name}-%{version}/
cp -fr nullfs.c Makefile dkms.conf %{buildroot}%{_usrsrc}/%{dkms_name}-%{version}/

%post
dkms add -m %{dkms_name} -v %{version} -q --rpm_safe_upgrade || :
# Rebuild and make available for the currently running kernel:
dkms build -m %{dkms_name} -v %{version} -q || :
dkms install -m %{dkms_name} -v %{version} -q --force || :

%preun
# Remove all versions from DKMS registry:
dkms remove -m %{dkms_name} -v %{version} -q --all --rpm_safe_upgrade || :

%files
%{_usrsrc}/%{dkms_name}-%{version}

%changelog
* Sat May 10 2025 Simone Caronni <negativo17@gmail.com> - 0.18-2
- Update dkms.conf file.

* Wed Apr 16 2025 Simone Caronni <negativo17@gmail.com> - 0.18-1
- Update to 0.18.0.
- Weak modules are already disabled in Fedora.

* Wed Oct 16 2024 Simone Caronni <negativo17@gmail.com> - 0.17-2
- Do not uninstall in preun scriptlet in case of an upgrade.

* Wed Nov 29 2023 Simone Caronni <negativo17@gmail.com> - 0.17-1
- First build.

