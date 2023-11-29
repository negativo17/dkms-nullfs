%global debug_package %{nil}
%global dkms_name nullfs

Name:       dkms-%{dkms_name}
Version:    0.17
Release:    1%{?dist}
Summary:    A virtual file system that behaves like /dev/null
License:    GPLv3+
URL:        https://github.com/abbbi/nullfsvfs
BuildArch:  noarch

Source0:    %{url}/archive/v%{version}.tar.gz#/nullfsvfs-%{version}.tar.gz
Source1:    %{name}.conf
Source2:    dkms-no-weak-modules.conf

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

%if 0%{?fedora}
# Do not enable weak modules support in Fedora (no kABI):
install -p -m 644 -D %{SOURCE2} %{buildroot}%{_sysconfdir}/dkms/%{dkms_name}.conf
%endif

%post
dkms add -m %{dkms_name} -v %{version} -q || :
# Rebuild and make available for the currently running kernel:
dkms build -m %{dkms_name} -v %{version} -q || :
dkms install -m %{dkms_name} -v %{version} -q --force || :

%preun
# Remove all versions from DKMS registry:
dkms remove -m %{dkms_name} -v %{version} -q --all || :

%files
%{_usrsrc}/%{dkms_name}-%{version}
%if 0%{?fedora}
%{_sysconfdir}/dkms/%{dkms_name}.conf
%endif

%changelog
* Wed Nov 29 2023 Simone Caronni <negativo17@gmail.com> - 0.17-1
- First build.

