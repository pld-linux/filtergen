Summary:	Simple packet filter generator
Name:		filter
Version:	0.5
Release:	1
License:	GPL
Group:		Networking/Utilities
Group(de):	Netzwerkwesen/Werkzeuge
Group(es):	Red/Utilitarios
Group(pl):	Sieciowe/Narzêdzia
Group(pt_BR):	Rede/Utilitários
Source0:	http://hairy.beasts.org/filter/%{name}-%{version}.tar.gz
Source1:	%{name}.conf
Patch0:		%{name}-equalsigns.patch
URL:		http://hairy.beasts.org/filter/
BuildRequires:	flex
Provides:	firewall
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This tool is for generating packet filtering rules from a fairly high-
level description language. It doesn't support all of the whizz-bang
features of the latest and greatest packet filters, but supports a
decent subset which is sufficient for typical workstation.

It currently supports only Linux iptables and ipchains. Cisco IOS has
been begun, but is incomplete. Darren Reed's ipfilter may be supported
at some stage. It doesn't generate optimal rulesets, and has a few
limitations which need to be removed, but is still a useful tool.

Please read HONESTY file!

%prep
%setup  -q
%patch0 -p1

%build
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/{%{_sbindir},%{_sysconfdir}/%{name}}

install filtergen $RPM_BUILD_ROOT/%{_sbindir}
install %{SOURCE1} $RPM_BUILD_ROOT/%{_sysconfdir}/%{name}/simple.conf

gzip -9nf README HONESTY HISTORY TODO tests/*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz tests
%attr(755,root,root) %{_sbindir}/filtergen
%{_sysconfdir}/%{name}/simple.conf
