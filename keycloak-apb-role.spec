%if 0%{?copr}
%define build_timestamp .%(date +"%Y%m%d%H%M%%S")
%else
%define build_timestamp %{nil}
%endif

Name: 		keycloak-apb-role
Version:	1.0.1
Release:	1%{build_timestamp}%{?dist}
Summary:	Ansible Playbook Bundle for keycloak

License:	ASL 2.0
URL:		https://github.com/ansibleplaybookbundle/keycloak-apb
Source0:	https://github.com/ansibleplaybookbundle/keycloak-apb/archive/%{name}-%{version}.tar.gz
BuildArch:  noarch

%description
%{summary}

%prep
%setup -q -n %{name}-%{version}
%if !0%{?copr}
patch -p1 < downstream.patch
%endif

%install
mkdir -p %{buildroot}/opt/apb/ %{buildroot}/opt/ansible/
mv playbooks %{buildroot}/opt/apb/actions
mv roles %{buildroot}/opt/ansible/roles

%files
%doc
/opt/apb/actions
/opt/ansible/roles
