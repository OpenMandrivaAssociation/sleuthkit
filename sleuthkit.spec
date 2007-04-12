
# OE: conditional switches
#
#(ie. use with rpm --rebuild):
#
#	--with diet	Compile task against dietlibc
#
# 

%define build_diet 0

# commandline overrides:
# rpm -ba|--rebuild --with 'xxx'
%{?_with_diet: %{expand: %%define build_diet 1}}

Summary: 	The Sleuth Kit
Name:		sleuthkit
Version:	2.05
Release:	%mkrel 1
License:	GPL
Group:		File tools
URL:		http://www.sleuthkit.org/sleuthkit/
Source0:	http://prdownloads.sourceforge.net/sleuthkit/%{name}-%{version}.tar.bz2
Source1:	mac-robber-1.00.tar.bz2
Patch0:		sleuthkit-2.05-nofile.diff
Requires:	file
Obsoletes:	task = %{version}
Provides:	task = %{version}
Conflicts:	dstat
%if %{build_diet}
BuildRequires:	dietlibc-devel >= 0.20-1mdk
%endif
BuildRequires:	libstdc++-devel
BuildRequires:	zlib-devel
BuildRequires:	openssl-devel
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

%prep

%setup -q -n %{name}-%{version} -a1
%patch0 -p0

%build

%if %{build_diet}
    # OE: use the power of dietlibc
    make CC="diet gcc -D_BSD_SOURCE -D_GNU_SOURCE -s -static"
    diet gcc -D_BSD_SOURCE -D_GNU_SOURCE -s -static -o bin/mac-robber mac-robber-1.00/mac-robber.c
%else
    make COPTS="%{optflags}" OPT="%{optflags}"
    gcc %{optflags} -o bin/mac-robber mac-robber-1.00/mac-robber.c
%endif

mv mac-robber-1.00/README README.mac-robber
chmod 644 README.mac-robber

# hack...
perl -pi -e "s|%{_builddir}/%{name}-%{version}|%{_prefix}|g" bin/sorter

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_datadir}/sorter
install -d %{buildroot}%{_mandir}/man1

install -m755 bin/* %{buildroot}%{_bindir}/
install -m644 man/man1/* %{buildroot}%{_mandir}/man1/
install -m644 share/sorter/* %{buildroot}%{_datadir}/sorter/

#rm -r $RPM_BUILD_ROOT%_bindir/file
#rm -r $RPM_BUILD_ROOT%_mandir/man1/file.1

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc CHANGES.txt INSTALL.txt README.mac-robber README.txt TODO.txt licenses/* tct.docs/*
%{_bindir}/dcalc
%{_bindir}/dcat
%{_bindir}/disk_sreset
%{_bindir}/disk_stat
%{_bindir}/dls
%{_bindir}/dstat
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
%{_bindir}/mac-robber
%{_bindir}/mactime
%{_bindir}/md5
%{_bindir}/mmls
%{_bindir}/mmstat
%{_bindir}/sha1
%{_bindir}/sigfind
%{_bindir}/sorter
%{_bindir}/srch_strings
%{_mandir}/man1/dcalc.1*
%{_mandir}/man1/dcat.1*
%{_mandir}/man1/disk_sreset.1*
%{_mandir}/man1/disk_stat.1*
%{_mandir}/man1/dls.1*
%{_mandir}/man1/dstat.1*
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
%{_mandir}/man1/mmls.1*
%{_mandir}/man1/mmstat.1*
%{_mandir}/man1/sigfind.1*
%{_mandir}/man1/sorter.1*
%dir %{_datadir}/sorter/
%{_datadir}/sorter/*

