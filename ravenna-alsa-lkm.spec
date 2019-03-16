

%define git_commit_sha 01bce4390835bcb9875a13a1f76a3be2e25b3eea
%define git_short 01bce4390835
%define kmod_name MergingRavennaALSA

%if 0%{?fedora}
%undefine _debugsource_packages
%endif

Name:           ravenna-alsa-lkm
Version:        %{git_short}
Release:        0.1%{?dist}
Summary:        ALSA RAVENNA/AES67 Driver

License:        GPL
URL:            https://www.merging.com/
Source0:        https://bitbucket.org/MergingTechnologies/ravenna-alsa-lkm/get/%{git_commit_sha}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires: elfutils-libelf-devel
BuildRequires: chrpath
BuildRequires: kernel-devel

%description
ALSA Linux driver designed to provide high performance RAVENNA/AES67 support for the Linux ecosystems.

%package -n merging-butler
Summary:	User land binary for ravenna-alsa-lkm
License:	EULA

%description -n merging-butler
User land binary for ravenna-alsa-lkm

%prep
%setup -q -n MergingTechnologies-%{name}-%{version}
cd driver
echo "/usr/lib/rpm/redhat/find-requires | %{__sed} -e '/^ksym.*/d'" > filter-requires.sh
echo "override %{kmod_name} * weak-updates/%{kmod_name}" > kmod-%{kmod_name}.conf


%build
cd driver
%{__make} %{?_smp_mflags} -C /usr/src/kernels/`rpm -qa --queryformat "%%{VERSION}-%%{RELEASE}.%%{ARCH}" kernel-devel` M=`pwd` modules


%install
export INSTALL_MOD_PATH=%{buildroot}
export INSTALL_MOD_DIR=extra/%{kmod_name}
pushd driver
%{__make} -C /usr/src/kernels/`rpm -qa --queryformat "%%{VERSION}-%%{RELEASE}.%%{ARCH}" kernel-devel` M=`pwd` modules_install
%{__install} -d %{buildroot}%{_sysconfdir}/depmod.d/
%{__install} kmod-%{kmod_name}.conf %{buildroot}%{_sysconfdir}/depmod.d/
# Set the module(s) to be executable, so that they will be stripped when packaged.
find %{buildroot} -type f -name \*.ko -exec %{__chmod} u+x \{\} \;
popd
pushd Butler
%{__install} -d %{buildroot}%{_bindir}
%{__install} -m 755 Merging_RAVENNA_Daemon %{buildroot}%{_bindir}/
chrpath --delete %{buildroot}%{_bindir}/Merging_RAVENNA_Daemon


%files
%defattr(-,root,root,-)
%doc README.md
/lib/modules/*/extra/%{kmod_name}/
%{_sysconfdir}/depmod.d/kmod-%{kmod_name}.conf

%files -n merging-butler
%{_bindir}/Merging_RAVENNA_Daemon

%changelog
* Sat Mar 16 2019 Lucas Bickel <hairmare@rabe.ch> - 01bce4390835-0.1
- Initial RPM release
