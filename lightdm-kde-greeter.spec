%global optflags %{optflags} -Wno-error -Wno-keyword-macro

Summary:	LightDM KDE Greeter
Name:		lightdm-kde-greeter
Version:	6.1.0
Release:	1
Group:		System/X11
License:	GPLv3+
URL:	 	https://projects.kde.org/projects/playground/base/lightdm
Source0: 	https://invent.kde.org/plasma/lightdm-kde-greeter/-/archive/v%{version}/lightdm-kde-greeter-v%{version}.tar.bz2
Source1:	lightdm-kde-greeter.conf

BuildRequires:	gettext
BuildRequires:	intltool
BuildRequires:	pkgconfig(liblightdm-qt5-3)
BuildRequires:	cmake(Qt6Core)
BuildRequires:  cmake(Qt6Core5Compat)
BuildRequires:	cmake(Qt6DBus)
BuildRequires:	cmake(Qt6Gui)
BuildRequires:  cmake(Qt6ShaderTools)
BuildRequires:	cmake(Qt6Quick)
BuildRequires:	cmake(Qt6QuickWidgets)
BuildRequires:  cmake(Qt6Qml)
BuildRequires:	cmake(Qt6QmlCore)
BuildRequires:	cmake(Qt6QmlNetwork)
BuildRequires:	cmake(Qt6QuickControls2)
BuildRequires:	cmake(Qt6UiPlugin)
BuildRequires:	cmake(Qt6UiTools)
BuildRequires:	cmake(Qt6Widgets)
BuildRequires:	cmake(KF6Config)
BuildRequires:  cmake(KF6IconThemes)
BuildRequires:  cmake(KF6KCMUtils)
BuildRequires:  cmake(KF6Package)
BuildRequires:  cmake(KF6ConfigWidgets)
BuildRequires:  cmake(KF6I18n)
BuildRequires:  cmake(KF6Auth)
BuildRequires:  cmake(KF6NetworkManagerQt)
BuildRequires:  cmake(plasmaquick)
BuildRequires:	qt6-qtbase-theme-gtk3
BuildRequires:  pkgconfig(gtk+-2.0)
BuildRequires:  pkgconfig(liblightdm-gobject-1)

Provides:	lightdm-greeter
Requires:	lightdm
Requires(post,postun):	update-alternatives

%description
A LightDM greeter that uses the KDE toolkit.

%prep
%autosetup -n lightdm-kde-greeter-v%{version} -p1
sed 's/sbin/bin/' -i greeter/CMakeLists.txt

%build
export CC=gcc
export CXX=g++
%cmake \
	-DGREETER_WAYLAND_SESSIONS_FIRST=ON \
	-DGREETER_IMAGES_DIR=%_datadir/%name/images \
 	-DKDE_INSTALL_USE_QT_SYS_PATHS:BOOL=ON \
	-DBUILD_TESTING=OFF
%make_build


%install
%make_install -C build

mkdir -p %{buildroot}%{_sysconfdir}/lightdm
install -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/lightdm/lightdm-kde-greeter.conf

%find_lang kcm_lightdm           --with-kde
%find_lang lightdm_kde_greeter   --with-kde
%find_lang lightdm_theme_userbar --with-kde

# FIXME: why does it installs to the wrong dir
mv %buildroot/%name %buildroot%_datadir/
mkdir -p %buildroot%_sharedstatedir/%name

%post
%systemd_user_post %name-wifikeeper.service

%preun
%systemd_user_preun %name-wifikeeper.service

%postun
%systemd_user_postun_with_restart %name-wifikeeper.service


%files -f kcm_lightdm.lang -f lightdm_kde_greeter.lang -f lightdm_theme_userbar.lang
%doc README.md
%license COPYING.GPL3
%config(noreplace) %_sysconfdir/lightdm/%name.conf
%dir %_sharedstatedir/%name
%_bindir/%name
%_bindir/lightdm-kde-greeter-rootimage
%_bindir/lightdm-kde-greeter-wifikeeper
%_datadir/applications/kcm_lightdm.desktop
%_datadir/dbus-1/system-services/org.kde.kcontrol.kcmlightdm.service
%_datadir/dbus-1/system.d/org.kde.kcontrol.kcmlightdm.conf
%_datadir/polkit-1/actions/org.kde.kcontrol.kcmlightdm.policy
%_datadir/xgreeters/lightdm-kde-greeter.desktop
%_datadir/%name/
%{_libdir}/libexec/kf6/kauth/kcmlightdmhelper
%{_libdir}/qt6/plugins/plasma/kcms/systemsettings/kcm_lightdm.so
%_userunitdir/lightdm-kde-greeter-wifikeeper.service
