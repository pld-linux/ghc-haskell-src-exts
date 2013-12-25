#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	haskell-src-exts
Summary:	Manipulating Haskell source: abstract syntax, lexer, parser, and pretty-printer
Summary(pl.UTF-8):	Operacje na źródłach w Haskellu: abstraksyjna składnia, analiza leksykalna i składniowa, wypisywanie
Name:		ghc-%{pkgname}
Version:	1.14.0
Release:	1
License:	BSD
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/haskell-src-exts
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	84161d1a446c2ddfd1013e9a7b60b03c
URL:		http://hackage.haskell.org/package/haskell-src-exts
BuildRequires:	cpphs >= 1.3
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-array >= 0.1
BuildRequires:	ghc-base >= 3
BuildRequires:	ghc-pretty >= 1.0
%if %{with prof}
BuildRequires:	cpphs-prof >= 1.3
BuildRequires:	ghc-prof >= 6.12.3
BuildRequires:	ghc-array-prof >= 0.1
BuildRequires:	ghc-base-prof >= 3
BuildRequires:	ghc-pretty-prof >= 1.0
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
%requires_eq	ghc
Requires(post,postun):	/usr/bin/ghc-pkg
Requires:	cpphs >= 1.3
Requires:	ghc-array >= 0.1
Requires:	ghc-base >= 3
Requires:	ghc-pretty >= 1.0
Obsoletes:	ghc-haskell-src-exts-doc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
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

%description -l pl.UTF-8
Haskell-Source with Extensions (HSE, haskell-src-exts) to rozszerzenie
standardowego pakietu haskell-src, obsługujące większość
zarejestrowanych rozszerzeń składniowych do Haskella, w tym:

- wieloparametrowe klasy typów z zależnościami funkcyjnymi
- rodziny typów indeksowanych (w tym asocjacyjnych)
- deklaracje pustych danych
- GADT
- parametry implikowane
- Template Haskell

i kilka innych. Obsługiwane są wszystkie rozszerzenia zaimplementowane
w GHC. Poza tymi rozszerzeniami, pakiet obsługuje wzorce regularne
zgodne z rozszerzeniem HaRP, a także składnię osadzonego XML-a w stylu
HSX.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC.
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	cpphs-prof >= 1.3
Requires:	ghc-array-prof >= 0.1
Requires:	ghc-base-prof >= 3
Requires:	ghc-pretty-prof >= 1.0

%description prof
Profiling %{pkgname} library for GHC. Should be installed when GHC's
profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.hs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
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
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc CHANGELOG %{name}-%{version}-doc/*
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/HShaskell-src-exts-%{version}.o
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHShaskell-src-exts-%{version}.a
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Haskell
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Haskell/*.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Haskell/Exts
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Haskell/Exts/*.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Haskell/Exts/Annotated
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Haskell/Exts/Annotated/*.hi

%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHShaskell-src-exts-%{version}_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Haskell/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Haskell/Exts/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Haskell/Exts/Annotated/*.p_hi
