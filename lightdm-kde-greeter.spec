Summary:	LightDM KDE Greeter
Name:		lightdm-kde-greeter
Version:	0.3.1
Release:	2
Group:		System/X11
License:	GPLv3+
URL:	 	https://projects.kde.org/projects/playground/base/lightdm
Source0: 	http://carroll.aset.psu.edu/pub/kde/unstable/lightdm-kde/src/lightdm-kde-%{version}.tar.bz2

BuildRequires:	gettext
BuildRequires:	intltool
BuildRequires:	kdelibs4-devel
BuildRequires:	pkgconfig(liblightdm-qt-2) >= 1.3.2

Provides:	lightdm-greeter
Requires:	lightdm
Requires:	kdebase4-runtime
Requires(post,postun):	update-alternatives

%description
A LightDM greeter that uses the KDE toolkit.

%prep
%setup -qn lightdm-%{version}

%build
%cmake_kde4
%make

%install
%makeinstall_std -C build

%find_lang %{name} --all-name --with-kde

%post
%{_sbindir}/update-alternatives \
	--install %{_datadir}/xgreeters/lightdm-greeter.desktop \
	lightdm-greeter \
	%{_datadir}/xgreeters/lightdm-kde-greeter.desktop \
	10

%postun
if [ $1 -eq 0 ]; then
%{_sbindir}/update-alternatives \
	--remove lightdm-greeter \
	%{_datadir}/xgreeters/lightdm-kde-greeter.desktop
fi

%files -f %{name}.lang
%{_sysconfdir}/dbus-1/system.d/org.kde.kcontrol.kcmlightdm.conf
%{_kde_libdir}/kde4/kcm_lightdm.so
%{_kde_libdir}/kde4/libexec/kcmlightdmhelper
%{_kde_libdir}/kde4/libexec/lightdm-kde-greeter-rootimage
%{_sbindir}/lightdm-kde-greeter
%{_datadir}/apps/lightdm-kde-greeter
%{_datadir}/dbus-1/system-services/org.kde.kcontrol.kcmlightdm.service
%{_datadir}/kde4/services/kcm_lightdm.desktop
%{_datadir}/polkit-1/actions/org.kde.kcontrol.kcmlightdm.policy
%{_datadir}/xgreeters/lightdm-kde-greeter.desktop
