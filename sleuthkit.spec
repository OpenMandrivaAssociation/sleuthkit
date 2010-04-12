%define libver 3
%define major 3
%define libname		%mklibname tsk %{libver} %{major}
%define develname	%mklibname tsk %{libver} -d

Summary: 	The Sleuth Kit
Name:		sleuthkit
Version:	3.0.1
Release:	%mkrel 2
License:	GPL
Group:		File tools
URL:		http://www.sleuthkit.org/sleuthkit/
Source0:	http://prdownloads.sourceforge.net/sleuthkit/%{name}-%{version}.tar.gz
Source1:	mac-robber-1.00.tar.bz2
Patch0:		sleuthkit-3.0.1-link.patch
Requires:	file
Requires:	afflib
Requires:	libewf
Provides:	task = %{version}
Obsoletes:	task = %{version}
Conflicts:	dstat
BuildRequires:	afflib-devel
BuildRequires:	libewf-devel
BuildRequires:	libstdc++-devel
BuildRequires:	openssl-devel
BuildRequires:	zlib-devel
BuildRequires:	libncurses-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

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
%setup -q -n %{name}-%{version} -a1
%patch0 -p0

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
rm -rf %{buildroot}
%makeinstall_std
find %{buildroot} -name '*.la' -exec rm -f {} ';'
install -m755 mac-robber %{buildroot}%{_bindir}/

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc CHANGES.txt README.txt licenses/* README.mac-robber
%doc docs/other.txt docs/skins*.txt docs/ref*.txt
# License is CPL 1.0 exept for some files.
%{_bindir}/blkcalc
%{_bindir}/blkcat
%{_bindir}/blkls
%{_bindir}/blkstat
%{_bindir}/disk_sreset
%{_bindir}/disk_stat
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
%{_mandir}/man1/disk_sreset.1*
%{_mandir}/man1/disk_stat.1*
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
%dir %{_datadir}/tsk3
%{_datadir}/tsk3/sorter/

%files -n %{libname}
%defattr(-,root,root,-)
%{_libdir}/libtsk3.so.%{major}*

%files -n %{develname}
%defattr(-,root,root,-)
%doc docs/library-api.txt
# CPL and IBM
%{_includedir}/tsk3/
%{_libdir}/libtsk3.so

