%define		pkgname	haskell-src-exts
Summary:	Manipulating Haskell source: abstract syntax, lexer, parser, and pretty-printer
Name:		ghc-%{pkgname}
Version:	1.11.1
Release:	3
License:	BSD
Group:		Development/Languages
Source0:	http://hackage.haskell.org/packages/archive/%{pkgname}/%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	c0c8f214de2e712455a5a250b7f898a9
URL:		http://hackage.haskell.org/package/haskell-src-exts/
BuildRequires:	cpphs
BuildRequires:	ghc >= 6.12.3
BuildRequires:	rpmbuild(macros) >= 1.608
Requires:	cpphs
%requires_eq	ghc
Obsoletes:	ghc-haskell-src-exts-doc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0
%define		_noautocompressdoc	*.haddock

%description
Haskell-Source with Extensions (HSE, haskell-src-exts) is an extension
of the standard haskell-src package, and handles most registered
syntactic extensions to Haskell, including:

* Multi-parameter type classes with functional dependencies
* Indexed type families (including associated types)
* Empty data declarations
* GADTs
* Implicit parameters
* Template Haskell 

and a few more. All extensions implemented in GHC are supported.
Apart from these standard extensions, it also handles regular patterns
as per the HaRP extension as well as HSX-style embedded XML syntax.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.hs configure -v2 \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build
runhaskell Setup.hs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
rm -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT/%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc CHANGELOG
%doc %{name}-%{version}-doc/*
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}
