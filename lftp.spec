%define _disable_ld_no_undefined 1
# build options
%bcond_with	dante

%define	major	0
%define	libjobs	%mklibname %{name}-jobs %{major}
%define	libtasks %mklibname %{name}-tasks %{major}
%define	devname	%mklibname %{name} -d

Summary:	Commandline ftp client
Name:		lftp
Version:	4.6.2
Release:	1
Group:		Networking/File transfer
License:	GPLv2+
Url:		http://lftp.yar.ru/
Source0:	http://lftp.yar.ru/ftp/%{name}-%{version}.tar.xz
Source1:	http://lftp.yar.ru/ftp/%{name}-%{version}.tar.xz.asc
Patch0:		lftp-2.2.0-lftpgetmanpage.patch
Patch1:		lftp-3.7.7-mdkconf.patch
Patch4:		lftp-4.4.0-gets.patch

BuildRequires:	readline-devel
BuildRequires:	pkgconfig(expat)
BuildRequires:	pkgconfig(gnutls)
BuildRequires:	pkgconfig(ncursesw)
%if %{with dante}
BuildRequires:	dante-devel
%endif
Requires:	less
Conflicts:	%{_lib}lftp0 < 4.6.0-1

Provides:	ftp

%description
LFTP is a shell-like command line ftp client. The main two advantages
over other ftp clients are reliability and ability to perform tasks
in background. It will reconnect and reget the file being transferred
if the connection broke. You can start a transfer in background and
continue browsing on the ftp site.  It does this all in one process.
When you have started background jobs and feel you are done, you can
just exit lftp and it automatically moves to nohup mode and completes
the transfers. It has also such nice features as reput and mirror.

%if !%{with dante}
Build option:
--with dante	Enable dante support
%endif

%package -n	%{libjobs}
Summary:	Dynamic libraries from %{name}
Group:		System/Libraries
Obsoletes:	%{_lib}lftp0 < 4.6.0-1

%description -n	%{libjobs}
Dynamic libraries from %{name}.

%package -n	%{libtasks}
Summary:	Dynamic libraries from %{name}
Group:		System/Libraries
Conflicts:	%{_lib}lftp0 < 4.6.0-1

%description -n	%{libtasks}
Dynamic libraries from %{name}.

%package -n	%{devname}
Summary:	Header files and static libraries from %{name}
Group:		Development/C
Requires:	%{libjobs} >= %{version}-%{release}
Requires:	%{libtasks} >= %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release} 

%description -n	%{devname}
Libraries and includes files for developing programs based on %{name}.

%prep
%setup -q
%apply_patches
%configure2_5x \
	--with-modules=yes \
	--with-pager="exec less" \
%if %{with dante}
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
%dir %{_libdir}/lftp/%{version}
%{_libdir}/lftp/%{version}/*.so

%files -n %{libjobs}
%{_libdir}/liblftp-jobs.so.%{major}*

%files -n %{libtasks}
%{_libdir}/liblftp-tasks.so.%{major}*

%files -n %{devname}
%{_libdir}/*.so

