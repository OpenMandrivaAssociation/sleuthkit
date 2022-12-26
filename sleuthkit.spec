%define	major 19
%define libname		%mklibname %{name}
%define develname	%mklibname %{name} -d

%bcond_with		java
%bcond_with		tests
%bcond_without	afflib
%bcond_without	libewf
%bcond_without	libvhdi
%bcond_without	libvmdk
%bcond_without	zlib

Summary: 	The Sleuth Kit
Name:		sleuthkit
Version:	4.12.0
Release:	1
License:	CPL and IBM and GPLv2+
Group:		File tools
URL:		http://www.sleuthkit.org/sleuthkit/
Source0:	https://github.com/sleuthkit/sleuthkit/archive/%{name}-%{version}.tar.gz
#BuildRequires:  intltool
%{?with_afflib:BuildRequires:	pkgconfig(afflib)}
%{?with_tests:BuildRequires:	pkgconfig(cppunit)}
%{?with_libewf:BuildRequires:	pkgconfig(libewf)}
%{?with_libvhdi:BuildRequires:	pkgconfig(libvhdi)}
%{?with_libvmdk:BuildRequires:	pkgconfig(libvmdk)}
BuildRequires:		pkgconfig(ncurses)
BuildRequires:		pkgconfig(openssl)
BuildRequires:		pkgconfig(sqlite3)
%{?with_zlib:BuildRequires:	pkgconfig(zlib)}
%{?with_java:
BuildRequires:		ant
BuildRequires:		ant-junit
BuildRequires:		jdk-current
#BuildRequires:		javapackages-local
BuildRequires:  	jpackage-utils
}

Requires:	file
Requires:	afflib
#Requires:	libewf
Requires:	mac-robber
#Requires:	vhdi
#Requires:	vmdk
%{?with_java:
Requires:       java >= 1:1.6.0
Requires:       jpackage-utils
}

Conflicts:	dstat

%description
The Sleuth Kit (previously known as TASK) is a collection of UNIX-based command
line file system forensic tools that allow an investigator to examine NTFS,
FAT, FFS, EXT2FS, and EXT3FS file systems of a suspect computer in a
non-intrusive fashion. The  tools have a layer-based design and can extract
data from internal file system structures. Because the tools do not rely on the
operating system to process the file systems, deleted and hidden content is
shown.

When performing a complete analysis of a system, command line tools can become
tedious. The Autopsy Forensic Browser is a graphical interface to the tools in
The Sleuth Kit, which allows one to more easily conduct an investigation.
Autopsy provides case management, image integrity, keyword searching, and other
automated operations.

%files
%license licenses/*
%doc ChangeLog.txt NEWS.txt README.md
# License is CPL 1.0 exept for some files.
%{_bindir}/blkcalc
%{_bindir}/blkcat
%{_bindir}/blkls
%{_bindir}/blkstat
%{_bindir}/fcat
%{_bindir}/ffind
%{_bindir}/fls
%{_bindir}/fsstat
%{_bindir}/hfind
%{_bindir}/icat
%{_bindir}/ifind
%{_bindir}/ils
%{_bindir}/img_cat
%{_bindir}/img_stat
%{_bindir}/istat
%{_bindir}/jcat
%{_bindir}/pstat
%{_bindir}/tsk_comparedir
%{_bindir}/tsk_gettimes
%{_bindir}/tsk_imageinfo
%{_bindir}/tsk_loaddb
%{_bindir}/tsk_recover
%{_bindir}/jls
%{_bindir}/usnjls
# This file is described as GPL in the doc
# But the license remains CPL in the source.
%{_bindir}/mactime
##
%{_bindir}/mmcat
%{_bindir}/mmls
%{_bindir}/mmstat
%{_bindir}/sigfind
%{_bindir}/sorter
## This file is GPLv2+
%{_bindir}/fiwalk
%{_bindir}/jpeg_extract
%{_bindir}/srch_strings
#
%{_mandir}/man1/blkcalc.1*
%{_mandir}/man1/blkcat.1*
%{_mandir}/man1/blkls.1*
%{_mandir}/man1/blkstat.1*
%{_mandir}/man1/fcat.1*
%{_mandir}/man1/ffind.1*
%{_mandir}/man1/fls.1*
%{_mandir}/man1/fsstat.1*
%{_mandir}/man1/hfind.1*
%{_mandir}/man1/icat.1*
%{_mandir}/man1/ifind.1*
%{_mandir}/man1/ils.1*
%{_mandir}/man1/img_cat.1*
%{_mandir}/man1/img_stat.1*
%{_mandir}/man1/istat.1*
%{_mandir}/man1/jcat.1*
%{_mandir}/man1/jls.1*
%{_mandir}/man1/mactime.1*
%{_mandir}/man1/mmcat.1*
%{_mandir}/man1/mmls.1*
%{_mandir}/man1/mmstat.1*
%{_mandir}/man1/sigfind.1*
%{_mandir}/man1/sorter.1*
%{_mandir}/man1/tsk_comparedir.1.*
%{_mandir}/man1/tsk_gettimes.1.*
%{_mandir}/man1/tsk_loaddb.1.*
%{_mandir}/man1/tsk_recover.1.*
%{_mandir}/man1/usnjls.1.*
%dir %{_datadir}/tsk
%{_datadir}/tsk/sorter/

#---------------------------------------------------------------------------

%package -n %{libname}
Summary:	Library for %{name}
Group:		System/Libraries

%description -n %{libname}
The %libname package contains library for %{name}.

%files -n %{libname}
%{_libdir}/libtsk.so.%{major}*

#---------------------------------------------------------------------------

%package -n %{develname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libname} = %{version}

%description -n %{develname}
The %{develname} package contains libraries and header files for
developing applications that use %{name}.

%files -n %{develname}
# CPL and IBM
%{_includedir}/tsk/
%{_libdir}/libtsk.so
%{_libdir}/pkgconfig/tsk.pc

#---------------------------------------------------------------------------

%prep
%autosetup -p1 -n %{name}-%{name}-%{version}

%build
export LDFLAGS+=-lsqlite3
#autoreconf -fiv
%configure \
	%{?with_afflib:		--with-afflib}	%{!?with_afflib:	--without-afflib} \
	%{?with_libewf:		--with-libewf}	%{!?with_libewf:	--without-libewf} \
	%{?with_libvhdi:	--with-libvhdi}	%{!?with_libvhdi:	--without-libvhdi} \
	%{?with_libvmdk:	--with-libvmdk}	%{!?with_libvmdk:	--without-libvmdk} \
	%{?with_zlib:		--with-zlib}	%{!?with_zlib:	--without-zlib} \
	%{?with_java:		--enable-java}	%{!?with_java:	--disable-java}

# remove rpath from libtool
sed -i.rpath 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i.rpath 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make_build

# hack...
perl -pi -e "s|%{_builddir}/%{name}-%{version}|%{_prefix}|g" bin/sorter

%install
%make_install

