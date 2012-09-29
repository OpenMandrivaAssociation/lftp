%define	major	0
%define	libname	%mklibname %{name} %{major}
%define develname %mklibname %{name} -d

# build options
%define	enable_dante	0
%{?_with_dante: %define enable_dante 1}

Summary:	Commandline ftp client
Name:		lftp
Version:	4.4.0
Release:	1
URL:		http://lftp.yar.ru/			
Group:		Networking/File transfer
License:	GPLv2+
Source0:	http://ftp.yars.free.net/pub/source/%{name}/%{name}-%{version}.tar.bz2
Source1:	http://ftp.yars.free.net/pub/source/%{name}/%{name}-%{version}.tar.bz2.asc
Patch0:		lftp-2.2.0-lftpgetmanpage.patch
Patch1:		lftp-3.7.7-mdkconf.patch
Patch2:		lftp-4.2.0-link.patch
Patch3:		lftp-3.7.14-fix-str-fmt.patch
Patch4:		lftp-4.4.0-gets.patch
Requires:	less
BuildRequires:	ncurses-devel
BuildRequires:	gnutls-devel >= 3.0
BuildRequires:	readline-devel
BuildRequires:	expat-devel
%if %enable_dante
BuildRequires:	dante-devel
%endif

%description
LFTP is a shell-like command line ftp client. The main two advantages
over other ftp clients are reliability and ability to perform tasks
in background. It will reconnect and reget the file being transferred
if the connection broke. You can start a transfer in background and
continue browsing on the ftp site.  It does this all in one process.
When you have started background jobs and feel you are done, you can
just exit lftp and it automatically moves to nohup mode and completes
the transfers. It has also such nice features as reput and mirror.

%if %enable_dante
Build option:
--with dante	Enable dante support
%endif

%package -n %{libname}
Summary:	Dynamic libraries from %{name}
Group:		System/Libraries

%description -n	%{libname}
Dynamic libraries from %{name}.

%package -n %{develname}
Summary:	Header files and static libraries from %{name}
Group:		Development/C
Requires:	%{libname} >= %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release} 
Obsoletes:	%mklibname -d lftp 0

%description -n	%{develname}
Libraries and includes files for developing programs based on %{name}.

%prep
%setup -q
%patch0 -p1 -b .manpage
%patch1 -p1 -b .agent
%patch2 -p1 -b .link
%patch4 -p1 -b .gets

%build
%configure2_5x \
	--with-modules=yes \
	--with-pager="exec less" \
%if %enable_dante
	--with-socksdante=yes \
%endif

%make 

%install
%makeinstall_std

%find_lang %{name}

%files -f %{name}.lang
%doc COPYING FAQ MIRRORS NEWS 
%doc README.* THANKS TODO lftp.lsm BUGS
%config(noreplace) %{_sysconfdir}/lftp.conf
%{_bindir}/*
%{_mandir}/man?/*
%{_datadir}/%{name}/

%files -n %{libname}
%{_libdir}/*.so.%{major}*
%dir %{_libdir}/lftp/%{version}
%{_libdir}/lftp/%{version}/*.so

%files -n %{develname}
%{_libdir}/*.so
