Summary:	Markdown grammar for tree-sitter
Name:		tree-sitter-markdown
Version:	0.2.3
Release:	1
License:	MIT
Group:		Libraries
Source0:	https://github.com/tree-sitter-grammars/tree-sitter-markdown/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	b6ea171a2c434992d9ddb965361513c2
URL:		https://github.com/tree-sitter-grammars/tree-sitter-markdown
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		ts_markdown_soname		libtree-sitter-markdown.so.0
%define		ts_markdown_inline_soname	libtree-sitter-markdown-inline.so.0

%description
A Markdown parser for tree-sitter.

%package devel
Summary:	Header files for tree-sitter-markdown
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
Header files for tree-sitter-markdown.

%package static
Summary:	Static tree-sitter-markdown library
Group:		Development/Libraries
Requires:	%{name}-devel%{?_isa} = %{version}-%{release}

%description static
Static tree-sitter-markdown library.

%package -n neovim-parser-markdown
Summary:	Markdown parser for Neovim
Group:		Applications/Editors
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description -n neovim-parser-markdown
Markdown parser for Neovim.

%prep
%setup -q

%build
%{__make} \
	PREFIX="%{_prefix}" \
	INCLUDEDIR="%{_includedir}" \
	LIBDIR="%{_libdir}" \
	PCLIBDIR="%{_pkgconfigdir}" \
	CC="%{__cc}" \
	CFLAGS="%{rpmcppflags} %{rpmcflags}" \
	LDFLAGS="%{rpmldflags}"

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_libdir}/nvim/parser

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	PREFIX="%{_prefix}" \
	INCLUDEDIR="%{_includedir}" \
	LIBDIR="%{_libdir}" \
	PCLIBDIR="%{_pkgconfigdir}"

%{__ln_s} %{_libdir}/%{ts_markdown_soname} $RPM_BUILD_ROOT%{_libdir}/nvim/parser/markdown.so
%{__ln_s} %{_libdir}/%{ts_markdown_inline_soname} $RPM_BUILD_ROOT%{_libdir}/nvim/parser/markdown_inline.so

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CONTRIBUTING.md LICENSE README.md
%attr(755,root,root) %{_libdir}/libtree-sitter-markdown.so.*.*
%attr(755,root,root) %ghost %{_libdir}/%{ts_markdown_soname}
%attr(755,root,root) %{_libdir}/libtree-sitter-markdown-inline.so.*.*
%attr(755,root,root) %ghost %{_libdir}/%{ts_markdown_inline_soname}

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libtree-sitter-markdown.so
%attr(755,root,root) %{_libdir}/libtree-sitter-markdown-inline.so
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
