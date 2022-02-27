#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_with	tests	# unit tests (circular dependencies)
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define module	zope.copy
Summary:	Pluggable object copying mechanism
Summary(pl.UTF-8):	Mechanizm kopiowania obiektów z obsługą wtyczek
Name:		python-%{module}
Version:	4.2
Release:	1
License:	ZPL v2.1
Group:		Libraries/Python
Source0:	https://files.pythonhosted.org/packages/source/z/zope.copy/zope.copy-%{version}.tar.gz
# Source0-md5:	4111cf208f0cb7cd6dfad742abf97cbe
URL:		https://www.zope.dev/
%if %{with python2}
BuildRequires:	python >= 1:2.7
BuildRequires:	python-devel >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-zope.component
BuildRequires:	python-zope.interface
BuildRequires:	python-zope.location
BuildRequires:	python-zope.testing
BuildRequires:	python-zope.testrunner
%endif
%endif
%if %{with python3}
BuildRequires:	python3 >= 1:3.4
BuildRequires:	python3-devel >= 1:3.4
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-zope.component
BuildRequires:	python3-zope.interface
BuildRequires:	python3-zope.location
BuildRequires:	python3-zope.testing
BuildRequires:	python3-zope.testrunner
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-repoze.sphinx.autointerface
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package provides a pluggable mechanism for copying persistent
objects.

%description -l pl.UTF-8
Ten pakiet zapewnia mechanizm kopiowania trwałych obiektów z
obsługą wtyczek.

%package -n python3-%{module}
Summary:	Pluggable object copying mechanism
Summary(pl.UTF-8):	Mechanizm kopiowania obiektów z obsługą wtyczek
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.4

%description -n python3-%{module}
This package provides a pluggable mechanism for copying persistent
objects.

%description -n python3-%{module} -l pl.UTF-8
Ten pakiet zapewnia mechanizm kopiowania trwałych obiektów z
obsługą wtyczek.

%package apidocs
Summary:	API documentation for Python zope.copy module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona zope.copy
Group:		Documentation

%description apidocs
API documentation for Python zope.copy module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona zope.copy.

%prep
%setup -q -n %{module}-%{version}

%build
%if %{with python2}
%py_build

%if %{with tests}
PYTHONPATH=$(pwd)/src \
zope-testrunner-2 --test-path=src -v
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTHONPATH=$(pwd)/src \
zope-testrunner-3 --test-path=src -v
%endif
%endif

%if %{with doc}
PYTHONPATH=$(pwd)/src \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%{__rm} -r $RPM_BUILD_ROOT%{py_sitescriptdir}/zope/copy/tests
%endif

%if %{with python3}
%py3_install

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/zope/copy/tests
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGES.rst COPYRIGHT.txt LICENSE.txt README.rst
%{py_sitescriptdir}/zope/copy
%{py_sitescriptdir}/zope.copy-*.egg-info
%{py_sitescriptdir}/zope.copy-*-nspkg.pth
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc CHANGES.rst COPYRIGHT.txt LICENSE.txt README.rst
%{py3_sitescriptdir}/zope/copy
%{py3_sitescriptdir}/zope.copy-*.egg-info
%{py3_sitescriptdir}/zope.copy-*-nspkg.pth
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_modules,_static,*.html,*.js}
%endif
