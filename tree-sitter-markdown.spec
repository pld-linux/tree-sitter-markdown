#
# Conditional build:
%bcond_without	python3	# Python 3.x binding
%bcond_without	tests	# Python binding load test

Summary:	Markdown grammar for tree-sitter
Summary(pl.UTF-8):	Gramatyka formatu Markdown dla tree-sittera
Name:		tree-sitter-markdown
Version:	0.5.2
Release:	1
License:	MIT
Group:		Libraries
#Source0Download: https://github.com/tree-sitter-grammars/tree-sitter-markdown/releases
Source0:	https://github.com/tree-sitter-grammars/tree-sitter-markdown/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	cbc71aea4dab8d70ad59957d54c08446
Patch0:		%{name}-typo.patch
Patch1:		%{name}-python.patch
URL:		https://github.com/tree-sitter-grammars/tree-sitter-markdown
# c11
BuildRequires:	gcc >= 6:4.7
%if %{with python3}
BuildRequires:	python3-devel >= 1:3.10
BuildRequires:	python3-setuptools >= 1:42
BuildRequires:	python3-wheel
%if %{with tests}
BuildRequires:	python3-tree-sitter >= 0.24
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		soname_ver	15.0

%description
A Markdown parser for tree-sitter.

%description -l pl.UTF-8
Gramatyka formatu Markdown dla tree-sittera.

%package devel
Summary:	Header files for tree-sitter-markdown
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki tree-sitter-markdown
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
Header files for tree-sitter-markdown.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki tree-sitter-markdown.

%package static
Summary:	Static tree-sitter-markdown library
Summary(pl.UTF-8):	Statyczna biblioteka tree-sitter-markdown
Group:		Development/Libraries
Requires:	%{name}-devel%{?_isa} = %{version}-%{release}

%description static
Static tree-sitter-markdown library.

%description static -l pl.UTF-8
Statyczna biblioteka tree-sitter-markdown.

%package -n neovim-parser-markdown
Summary:	Markdown parser for Neovim
Summary(pl.UTF-8):	Analizator składni formatu Markdown dla Neovima
Group:		Applications/Editors
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description -n neovim-parser-markdown
Markdown parser for Neovim.

%description -n neovim-parser-markdown -l pl.UTF-8
Analizator składni formatu Markdown Lua dla Neovima.

%package -n python3-tree-sitter-markdown
Summary:	Lua parser for Python
Summary(pl.UTF-8):	Analizator składni formatu Markdown dla Pythona
Group:		Libraries/Python
Requires:	python3-tree-sitter >= 0.24

%description -n python3-tree-sitter-markdown
Lua parser for Python.

%description -n python3-tree-sitter-markdown -l pl.UTF-8
Analizator składni formatu Markdown dla Pythona.

%prep
%setup -q
%patch -P0 -p1
%patch -P1 -p1

%build
%{__make} \
	PREFIX="%{_prefix}" \
	INCLUDEDIR="%{_includedir}" \
	LIBDIR="%{_libdir}" \
	PCLIBDIR="%{_pkgconfigdir}" \
	CC="%{__cc}" \
	CFLAGS="%{rpmcppflags} %{rpmcflags}" \
	LDFLAGS="%{rpmldflags}"

%if %{with python3}
%py3_build

%if %{with tests}
PYTHONPATH=$(readlink -f build-3/lib.*) \
%{__python3} -m unittest discover -s bindings/python/tests
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/nvim/parser

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	PREFIX="%{_prefix}" \
	INCLUDEDIR="%{_includedir}" \
	LIBDIR="%{_libdir}" \
	PCLIBDIR="%{_pkgconfigdir}"

%{__ln_s} -f libtree-sitter-markdown.so.%{soname_ver} $RPM_BUILD_ROOT%{_libdir}/libtree-sitter-markdown.so
%{__ln_s} -f libtree-sitter-markdown-inline.so.%{soname_ver} $RPM_BUILD_ROOT%{_libdir}/libtree-sitter-markdown-inline.so

%{__ln_s} ../../libtree-sitter-markdown.so.%{soname_ver} $RPM_BUILD_ROOT%{_libdir}/nvim/parser/markdown.so
%{__ln_s} ../../libtree-sitter-markdown-inline.so.%{soname_ver} $RPM_BUILD_ROOT%{_libdir}/nvim/parser/markdown_inline.so

# redundant symlinks
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libtree-sitter-markdown*.so.15

%if %{with python3}
%py3_install

%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/tree_sitter_markdown/*.c

%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE README.md
%{_libdir}/libtree-sitter-markdown.so.%{soname_ver}
%{_libdir}/libtree-sitter-markdown-inline.so.%{soname_ver}
# XXX: who should own top dirs?
%dir %{_datadir}/tree-sitter
%dir %{_datadir}/tree-sitter/queries
%{_datadir}/tree-sitter/queries/tree-sitter-markdown
%{_datadir}/tree-sitter/queries/tree-sitter-markdown-inline

%files devel
%defattr(644,root,root,755)
%{_libdir}/libtree-sitter-markdown.so
%{_libdir}/libtree-sitter-markdown-inline.so
%{_includedir}/tree_sitter/tree-sitter-markdown.h
%{_includedir}/tree_sitter/tree-sitter-markdown-inline.h
%{_pkgconfigdir}/tree-sitter-markdown.pc
%{_pkgconfigdir}/tree-sitter-markdown-inline.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libtree-sitter-markdown.a
%{_libdir}/libtree-sitter-markdown-inline.a

%files -n neovim-parser-markdown
%defattr(644,root,root,755)
%{_libdir}/nvim/parser/markdown.so
%{_libdir}/nvim/parser/markdown_inline.so

%if %{with python3}
%files -n python3-tree-sitter-markdown
%defattr(644,root,root,755)
%dir %{py3_sitedir}/tree_sitter_markdown
%{py3_sitedir}/tree_sitter_markdown/_binding.abi3.so
%{py3_sitedir}/tree_sitter_markdown/__init__.py
%{py3_sitedir}/tree_sitter_markdown/__init__.pyi
%{py3_sitedir}/tree_sitter_markdown/py.typed
%{py3_sitedir}/tree_sitter_markdown/__pycache__
%{py3_sitedir}/tree_sitter_markdown-%{version}-py*.egg-info
%endif
