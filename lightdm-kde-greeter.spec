Summary:	LightDM KDE Greeter
Name:		lightdm-kde-greeter
Version:	6.0.2
Release:	1
Group:		System/X11
License:	GPLv3+
URL:	 	https://projects.kde.org/projects/playground/base/lightdm
Source0: 	https://invent.kde.org/plasma/lightdm-kde-greeter/-/archive/v%{version}/lightdm-kde-greeter-v%{version}.tar.bz2
Source1:	lightdm-kde-greeter.conf

BuildRequires:	gettext
BuildRequires:	intltool
BuildRequires:	pkgconfig(liblightdm-qt5-3)
BuildRequires:  cmake(Qt6Core5Compat)
BuildRequires:  cmake(Qt6ShaderTools)
BuildRequires:  cmake(Qt6Qml)
BuildRequires:  cmake(KF6IconThemes)
BuildRequires:  cmake(KF6KCMUtils)
BuildRequires:  cmake(KF6Package)
BuildRequires:  cmake(KF6ConfigWidgets)
BuildRequires:  cmake(KF6I18n)
BuildRequires:  cmake(KF6Auth)
BuildRequires:  cmake(KF6NetworkManagerQt)
BuildRequires:  cmake(plasmaquick)
BuildRequires:  pkgconfig(gtk+-2.0)
BuildRequires:  pkgconfig(liblightdm-gobject-1)

Provides:	lightdm-greeter
Requires:	lightdm
Requires(post,postun):	update-alternatives

%description
A LightDM greeter that uses the KDE toolkit.

%prep
%autosetup -n lightdm-kde-greeter-v%{version} -p1

%build
%cmake_kf6 \
	-DGREETER_WAYLAND_SESSIONS_FIRST=ON \
	-DGREETER_IMAGES_DIR=%_datadir/%name/images \
	-DBUILD_TESTING=OFF
%make_build


%install
%make_install -C build

mkdir -p %{buildroot}%{_sysconfdir}/lightdm
install -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/lightdm/lightdm-kde-greeter.conf

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
%config(noreplace) %{_sysconfdir}/lightdm/lightdm-kde-greeter.conf
%{_kde_libdir}/kde4/kcm_lightdm.so
%{_kde_libdir}/kde4/libexec/kcmlightdmhelper
%{_kde_libdir}/kde4/libexec/lightdm-kde-greeter-rootimage
%{_sbindir}/lightdm-kde-greeter
%{_datadir}/apps/lightdm-kde-greeter
%{_datadir}/dbus-1/system-services/org.kde.kcontrol.kcmlightdm.service
%{_datadir}/kde4/services/kcm_lightdm.desktop
%{_datadir}/polkit-1/actions/org.kde.kcontrol.kcmlightdm.policy
%{_datadir}/xgreeters/lightdm-kde-greeter.desktop
