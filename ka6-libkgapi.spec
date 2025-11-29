#
# Conditional build:
%bcond_with	tests		# build with tests
%bcond_without	webengine	# build without webengine
%define		kdeappsver	25.08.3
%define		kframever	5.94.0
%define		qtver		5.15.2
%define		kaname		libkgapi
%ifarch x32 i686
%undefine	with_webengine
%endif
Summary:	libkgapi
Name:		ka6-%{kaname}
Version:	25.08.3
Release:	2
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	b5d929ddcffa6ec2234c07fbead7464d
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6Gui-devel >= 5.11.1
BuildRequires:	Qt6Network-devel
BuildRequires:	Qt6Positioning-devel >= 5.11.1
BuildRequires:	Qt6PrintSupport-devel >= 5.11.1
BuildRequires:	Qt6Qml-devel >= 5.11.1
BuildRequires:	Qt6Quick-devel >= 5.11.1
BuildRequires:	Qt6Test-devel
%{?with_webengine:BuildRequires:	Qt6WebChannel-devel >= 5.11.1}
%{?with_webengine:BuildRequires:	Qt6WebEngine-devel >= 5.11.1}
BuildRequires:	Qt6Widgets-devel
BuildRequires:	Qt6Xml-devel
BuildRequires:	cmake >= 3.20
BuildRequires:	cyrus-sasl-devel
BuildRequires:	gettext-devel
BuildRequires:	kf6-extra-cmake-modules >= %{kframever}
BuildRequires:	kf6-kcalendarcore-devel >= %{kframever}
BuildRequires:	kf6-kcontacts-devel >= %{kframever}
BuildRequires:	kf6-kio-devel >= %{kframever}
BuildRequires:	kf6-kwallet-devel >= %{kframever}
BuildRequires:	kf6-kwindowsystem-devel >= %{kframever}
BuildRequires:	ninja
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	qt6-linguist >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	shared-mime-info
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
%requires_eq_to Qt6Core Qt6Core-devel
Obsoletes:	ka5-%{kaname} < %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LibKGAPI is a KDE-based library for accessing various Google services
via their public API.

%description -l pl.UTF-8
LibKGAPI is biblioteką KDE do dostępu do różnych usług Google'a
korzystając z ich publicznego API.

%package devel
Summary:	Header files for %{kaname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kaname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Obsoletes:	ka5-%{kaname}-devel < %{version}

%description devel
Header files for %{kaname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kaname}.

%prep
%setup -q -n %{kaname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON
%ninja_build -C build

%if %{with tests}
ctest --test-dir build
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kaname}_qt --with-qm --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{kaname}_qt.lang
%defattr(644,root,root,755)
%{_libdir}/libKPim6GAPIBlogger.so.*.*
%ghost %{_libdir}/libKPim6GAPIBlogger.so.6
%{_libdir}/libKPim6GAPICalendar.so.*.*
%ghost %{_libdir}/libKPim6GAPICalendar.so.6
%{_libdir}/libKPim6GAPICore.so.*.*
%ghost %{_libdir}/libKPim6GAPICore.so.6
%{_libdir}/libKPim6GAPIDrive.so.*.*
%ghost %{_libdir}/libKPim6GAPIDrive.so.6
%{_libdir}/libKPim6GAPILatitude.so.*.*
%ghost %{_libdir}/libKPim6GAPILatitude.so.6
%{_libdir}/libKPim6GAPIMaps.so.*.*
%ghost %{_libdir}/libKPim6GAPIMaps.so.6
%{_libdir}/libKPim6GAPIPeople.so.*.*
%ghost %{_libdir}/libKPim6GAPIPeople.so.6
%{_libdir}/libKPim6GAPITasks.so.*.*
%ghost %{_libdir}/libKPim6GAPITasks.so.6
%ghost %{_libdir}/sasl2/libkdexoauth2.so.3
%{_libdir}/sasl2/libkdexoauth2.so.*.*
%{_datadir}/qlogging-categories6/libkgapi.categories

%files devel
%defattr(644,root,root,755)
%{_includedir}/KPim6/KGAPI
%{_libdir}/cmake/KPim6GAPI
%{_libdir}/libKPim6GAPIBlogger.so
%{_libdir}/libKPim6GAPICalendar.so
%{_libdir}/libKPim6GAPICore.so
%{_libdir}/libKPim6GAPIDrive.so
%{_libdir}/libKPim6GAPILatitude.so
%{_libdir}/libKPim6GAPIMaps.so
%{_libdir}/libKPim6GAPIPeople.so
%{_libdir}/libKPim6GAPITasks.so
%{_libdir}/sasl2/libkdexoauth2.so
