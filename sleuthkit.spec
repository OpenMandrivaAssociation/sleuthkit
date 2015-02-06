%define libver 3
%define major 9
%define libname		%mklibname tsk %{libver} %{major}
%define develname	%mklibname tsk %{libver} -d

Summary: 	The Sleuth Kit
Name:		sleuthkit
Version:	4.0.1
Release:	2
License:	GPL
Group:		File tools
URL:		http://www.sleuthkit.org/sleuthkit/
Source0:	http://prdownloads.sourceforge.net/sleuthkit/%{name}-%{version}.tar.gz
Source1:	mac-robber-1.00.tar.bz2
Patch0:		sleuthkit-4.0.0-gentoo-system-sqlite.patch
Patch1:		sleuthkit-4.0.1-rosa-linkage.patch
Requires:	file
Requires:	afflib
Requires:	libewf
Conflicts:	dstat
BuildRequires:	afflib-devel
BuildRequires:	pkgconfig(libewf)
BuildRequires:	openssl-devel
BuildRequires:	zlib-devel
BuildRequires:	ncurses-devel

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

%package -n %{libname}
Summary:	Library for %{name}
Group:		System/Libraries

%description -n %{libname}
The %libname package contains library for %{name}.

%package -n %{develname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libname} = %{version}

%description -n %{develname}
The %{develname} package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -a1
%patch0 -p1
%patch1 -p1

%build
autoreconf -fi
%configure2_5x --disable-static

# remove rpath from libtool
sed -i.rpath 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i.rpath 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make
gcc %{optflags} -o mac-robber mac-robber-1.00/mac-robber.c

mv mac-robber-1.00/README README.mac-robber
chmod 644 README.mac-robber

# hack...
perl -pi -e "s|%{_builddir}/%{name}-%{version}|%{_prefix}|g" bin/sorter

%install
%makeinstall_std
install -m755 mac-robber %{buildroot}%{_bindir}/

%files
%doc ChangeLog.txt NEWS.txt README.txt licenses/* README.mac-robber
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
%{_bindir}/tsk_comparedir
%{_bindir}/tsk_gettimes
%{_bindir}/tsk_loaddb
%{_bindir}/tsk_recover
%{_bindir}/jls
# This file is described as GPL in the doc
# But the license remains CPL in the source.
%{_bindir}/mactime
%{_bindir}/mac-robber
##
%{_bindir}/mmcat
%{_bindir}/mmls
%{_bindir}/mmstat
%{_bindir}/sigfind
%{_bindir}/sorter
## This file is GPLv2+
%{_bindir}/srch_strings
#
%{_mandir}/man1/blkcalc.1*
%{_mandir}/man1/blkcat.1*
%{_mandir}/man1/blkls.1*
%{_mandir}/man1/blkstat.1*
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
%{_mandir}/man1/tsk_comparedir.1.xz
%{_mandir}/man1/tsk_gettimes.1.xz
%{_mandir}/man1/tsk_loaddb.1.xz
%{_mandir}/man1/tsk_recover.1.xz
%dir %{_datadir}/tsk3
%{_datadir}/tsk3/sorter/


%files -n %{libname}
%{_libdir}/libtsk3.so.%{major}*

%files -n %{develname}
# CPL and IBM
%{_includedir}/tsk3/
%{_libdir}/libtsk3.so



%changelog
* Tue Dec 07 2010 Oden Eriksson <oeriksson@mandriva.com> 3.0.1-3mdv2011.0
+ Revision: 614899
- the mass rebuild of 2010.1 packages

* Mon Apr 12 2010 Funda Wang <fwang@mandriva.org> 3.0.1-2mdv2010.1
+ Revision: 533653
- fix linkage

* Mon Jul 20 2009 Frederik Himpe <fhimpe@mandriva.org> 3.0.1-1mdv2010.0
+ Revision: 398108
- Update to new version 3.0.1
- Run autoreconf to fix --disable-static configure option
- Remove rpath
- Remove unused .la files
- Remove unbundle patch which is not needed anymore
- Create libtsk3 subpackages
- Fix file list (synced with Fedora)
- BuildRequires: libncurses-devel

* Sat Aug 02 2008 Thierry Vignaud <tv@mandriva.org> 2.09-4mdv2009.0
+ Revision: 260795
- rebuild

* Tue Jul 29 2008 Thierry Vignaud <tv@mandriva.org> 2.09-3mdv2009.0
+ Revision: 252599
- rebuild

* Fri Dec 21 2007 Olivier Blin <oblin@mandriva.com> 2.09-1mdv2008.1
+ Revision: 136503
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Fri Sep 07 2007 Oden Eriksson <oeriksson@mandriva.com> 2.09-1mdv2008.0
+ Revision: 81984
- 2.09
- unbundle file, afflib and libewf

* Fri Aug 31 2007 Oden Eriksson <oeriksson@mandriva.com> 2.05-2mdv2008.0
+ Revision: 76894
- rebuild


* Sat Jul 29 2006 Oden Eriksson <oeriksson@mandriva.com> 2.05-1mdv2007.0
- 2.05
- fix deps

* Wed Oct 19 2005 Nicolas Lécureuil <neoclust@mandriva.org> 2.03-1mdk
- New release 2.03
- %%mkrel

* Sun Dec 26 2004 Stefan van der Eijk <stefan@mandrake.org> 1.73-1mdk
- 1.73
- rediffed p0

* Thu Nov 25 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 1.72-2mdk
- fix #12488

* Sun Oct 31 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 1.72-1mdk
- 1.72
- fix P0

* Wed Sep 01 2004 Stefan van der Eijk <stefan@mandrake.org> 1.71-1mdk
- 1.71

* Thu May 06 2004 Michael Scherer <misc@mandrake.org> 1.69-1mdk
- New release 1.69
- rpmbuildupdate aware
- update patch
- [DIRM]

