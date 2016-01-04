%{?scl:%scl_package rubygem-%{gem_name}}
%{!?scl:%global pkg_name %{name}}

%global gem_name safe_yaml
# Although there are tests
# the dependancies aren't in Fedora yet
%global enable_tests 0

Summary:       Parse YAML safely
Name:          %{?scl_prefix}rubygem-%{gem_name}
Version:       1.0.4
Release:       2%{?dist}
Group:         Development/Languages
License:       MIT
URL:           http://dtao.github.com/safe_yaml/
Source0:       https://rubygems.org/gems/%{gem_name}-%{version}.gem
Requires:      %{?scl_prefix_ruby}ruby(release)
Requires:      %{?scl_prefix_ruby}ruby(rubygems) 
BuildRequires: %{?scl_prefix_ruby}ruby(release)
BuildRequires: %{?scl_prefix_ruby}rubygems-devel
%if 0%{?enable_tests}
BuildRequires: %{?scl_prefix}rubygem(hashie)
BuildRequires: %{?scl_prefix}rubygem(heredoc_unindent)
BuildRequires: %{?scl_prefix}rubygem(ostruct)
BuildRequires: %{?scl_prefix_ror}rubygem(rspec)
BuildRequires: %{?scl_prefix}rubygem(yaml)
%endif
BuildArch:     noarch
Provides:      %{?scl_prefix}rubygem(%{gem_name}) = %{version}

%description
The SafeYAML gem provides an alternative implementation of 
YAML.load suitable for accepting user input in Ruby applications. 
Unlike Ruby's built-in implementation of YAML.load, SafeYAML's 
version will not expose apps to arbitrary code execution exploits.

%package doc
Summary:   Documentation for %{pkg_name}
Group:     Documentation
Requires:  %{?scl_prefix}%{pkg_name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{pkg_name}

%prep
%{?scl:scl enable %{scl} - << \EOF}
gem unpack %{SOURCE0}
%{?scl:EOF}
%setup -q -D -T -n  %{gem_name}-%{version}
%{?scl:scl enable %{scl} - << \EOF}
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec
%{?scl:EOF}

%build
%{?scl:scl enable %{scl} - << \EOF}
gem build %{gem_name}.gemspec
%{?scl:EOF}
%{?scl:scl enable %{scl} - << \EOF}
%gem_install
%{?scl:EOF}

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a ./%{gem_dir}/* %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{_bindir}
cp -a ./%{_bindir}/* %{buildroot}%{_bindir}

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x

# Remove build leftovers.
rm -rf %{buildroot}%{gem_instdir}/{.rvmrc,.document,.require_paths,.gitignore,.travis.yml,.rspec,.gemtest,.yard*}
rm -rf %{buildroot}%{gem_instdir}/%{gem_name}.gemspec
rm -rf %{buildroot}%{gem_instdir}/bundle_install_all_ruby_versions.sh

%if 0%{?enable_tests}

%check
pushd .%{gem_instdir}
%{?scl:scl enable %{scl} - << \EOF}
rspec -Ilib spec
%{?scl:EOF}
popd
%endif

%files
%{_bindir}/safe_yaml
%doc %{gem_instdir}/LICENSE.txt
%dir %{gem_instdir}
%{gem_instdir}/bin
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_instdir}/CHANGES.md
%doc %{gem_instdir}/README.md
%doc %{gem_docdir}
%{gem_instdir}/Rakefile
%{gem_instdir}/Gemfile
%{gem_instdir}/run_specs_all_ruby_versions.sh
%{gem_instdir}/spec

%changelog
* Thu Feb 19 2015 Josef Stribny <jstribny@redhat.com> - 1.0.4-2
- Add SCL macros

* Mon Oct 27 2014 Troy Dawson <tdawson@redhat.com> - 1.0.4-1
- Updated to latest release

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 29 2014 Troy Dawson <tdawson@redhat.com> - 1.0.3-1
- Updated to version 1.0.3

* Tue Feb 04 2014 Troy Dawson <tdawson@redhat.com> - 1.0.1-1
- Updated to version 1.0.1

* Mon Jul 22 2013  Troy Dawson <tdawson@redhat.com> - 0.9.4-2
- Updated tests

* Wed Jul 17 2013  Troy Dawson <tdawson@redhat.com> - 0.9.4-1
- Update to 0.9.4

* Fri Jun 14 2013  Troy Dawson <tdawson@redhat.com> - 0.9.3-1
- Initial package
