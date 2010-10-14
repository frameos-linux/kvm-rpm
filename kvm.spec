%define build_arches x86_64

Name:           kvm
BuildRequires:  libgcrypt-devel gnutls-devel libtermcap-devel readline-devel dbus-devel libaio-devel zlib-devel
BuildRequires:  hal-devel libcap-devel pciutils-devel libpciaccess-devel parted-devel libXau-devel curl-devel 
BuildRequires:  SDL-devel ncurses-devel alsa-lib-devel texi2html dev86 pkgconfig
Provides:       qemu-img kvm 
Requires:       kvm-kmod libvirt
Version:        88
Release:        2.frameos
Url:            http://www.linux-kvm.org/
License:        GPLv2+ and LGPLv2+ and BSD
Group:          Development/Tools
Summary:        Kernel Virtual Machine
Source:         %{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
Summary:        Linux Kernel Virtual Machine

Userland tools

Authors:
--------
    http://www.linux-kvm.org

%prep
%setup -q

%build
./configure --prefix=%{_prefix} \
            --audio-card-list=ac97 --disable-curses --disable-xen
make

%install
make prefix="${RPM_BUILD_ROOT}%{_prefix}" \
     bindir="${RPM_BUILD_ROOT}%{_bindir}" \
     sharedir="${RPM_BUILD_ROOT}%{_datadir}/%{name}" \
     mandir="${RPM_BUILD_ROOT}%{_mandir}" \
     docdir="${RPM_BUILD_ROOT}%{_docdir}/%{name}-%{version}" \
     datadir="${RPM_BUILD_ROOT}%{_datadir}/%{name}" install
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/modules/
#cp -pr /usr/share/kvm ${RPM_BUILD_ROOT}/usr/share/qemu
cp ${RPM_BUILD_ROOT}/usr/bin/qemu-system-x86_64 ${RPM_BUILD_ROOT}/usr/bin/qemu-kvm
echo "#!/bin/sh" > ${RPM_BUILD_ROOT}%{_sysconfdir}/sysconfig/modules/kvm.modules
echo "modprobe kvm_intel" >> ${RPM_BUILD_ROOT}%{_sysconfdir}/sysconfig/modules/kvm.modules
chmod +x ${RPM_BUILD_ROOT}%{_sysconfdir}/sysconfig/modules/kvm.modules
cp -a ${RPM_BUILD_ROOT}/usr/share/kvm ${RPM_BUILD_ROOT}/usr/share/qemu

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_datadir}/*
%{_bindir}/*
%{_sysconfdir}/sysconfig/modules/kvm.modules

%changelog
* Wed Aug 11 2010 Sergio Rubio rubiojr@frameos.org 88-2.frameos
- copy /usr/share/kvm to /usr/share/qemu 

* Thu May 18 2010 Sergio Rubio rubiojr@frameos.org 88-1
- initial release
