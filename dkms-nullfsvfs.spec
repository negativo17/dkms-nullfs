%global debug_package %{nil}
%global dkms_name nullfsvfs

Name:       dkms-%{dkms_name}
Version:    0.27
Release:    1%{?dist}
Summary:    A virtual file system that behaves like /dev/null
License:    GPLv3+
URL:        https://github.com/abbbi/%{dkms_name}
BuildArch:  noarch

Source0:    %{url}/archive/v%{version}.tar.gz#/%{dkms_name}-%{version}.tar.gz
Source1:    %{name}.conf
%if 0%{?rhel} == 9
# https://github.com/abbbi/nullfsvfs/commit/63661607ded4e3ee0ba35cf50e1166a2b203daeb
Patch0:     %{dkms_name}-el9.patch
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
%autosetup -p1 -n %{dkms_name}-%{version}

cp -f %{SOURCE1} dkms.conf

sed -i -e 's/__VERSION_STRING/%{version}/g' dkms.conf

%build

%install
# Create empty tree:
mkdir -p %{buildroot}%{_usrsrc}/%{dkms_name}-%{version}/
cp -fr %{dkms_name}.c Makefile dkms.conf %{buildroot}%{_usrsrc}/%{dkms_name}-%{version}/

%post
dkms add -m %{dkms_name} -v %{version} -q --rpm_safe_upgrade || :
# Rebuild and make available for the currently running kernel:
dkms build -m %{dkms_name} -v %{version} -q --force
dkms install -m %{dkms_name} -v %{version} -q --force

%preun
# Remove all versions from DKMS registry:
dkms remove -m %{dkms_name} -v %{version} -q --all --rpm_safe_upgrade || :

%files
%{_usrsrc}/%{dkms_name}-%{version}

%changelog
* Wed Jul 01 2026 Simone Caronni <negativo17@gmail.com> - 0.27-1
- Update to 0.27.

* Sun Mar 08 2026 Simone Caronni <negativo17@gmail.com> - 0.26-1
- Rename to nullfsvfs and update to 0.26.

* Mon Feb 09 2026 Simone Caronni <negativo17@gmail.com> - 0.22-1
- Update to 0.22.

* Mon Dec 01 2025 Simone Caronni <negativo17@gmail.com> - 0.21-1
- Update to 0.21.

* Wed Oct 08 2025 Simone Caronni <negativo17@gmail.com> - 0.19-2
- Fix modules not getting rebuilt when reinstalling package.
- Do not filter out as success module build steps.

* Wed Jun 18 2025 Simone Caronni <negativo17@gmail.com> - 0.19-1
- Update to 0.19.

* Sat May 10 2025 Simone Caronni <negativo17@gmail.com> - 0.18-2
- Update dkms.conf file.

* Wed Apr 16 2025 Simone Caronni <negativo17@gmail.com> - 0.18-1
- Update to 0.18.0.
- Weak modules are already disabled in Fedora.

* Wed Oct 16 2024 Simone Caronni <negativo17@gmail.com> - 0.17-2
- Do not uninstall in preun scriptlet in case of an upgrade.

* Wed Nov 29 2023 Simone Caronni <negativo17@gmail.com> - 0.17-1
- First build.

