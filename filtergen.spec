Summary:	Simple packet filter generator
Summary(pl):	Prosty generator filtrów pakietów
Name:		filter
Version:	0.5
Release:	2
License:	GPL
Group:		Networking/Utilities
Group(de):	Netzwerkwesen/Werkzeuge
Group(es):	Red/Utilitarios
Group(pl):	Sieciowe/Narzêdzia
Group(pt_BR):	Rede/Utilitários
Source0:	http://hairy.beasts.org/filter/%{name}-%{version}.tar.gz
Source1:	%{name}.conf
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

%description -l pl
To jest narzêdzie do generowania regu³ filtrowania pakietów z
wzglêdnie wysokopoziomowego jêzyka opisu. Nie obs³uguje wszystkich
zaawansowanych mo¿liwo¶ci najnowszych filtrów pakietów, ale wspiera
przyzwoity podzbiór, wystarczaj±cy dla typowych stacji roboczych.

Aktualnie obs³uguje tylko linuksowe iptables i ipchains. Obs³uga Cisco
IOS jest zaczêta, ale nie kompletna. ipfilter Darrena Reeda jest
obs³ugiwany czê¶ciowo. Nie generuje optymalnych regu³ek i ma parê
ograniczeñ, które powinny byæ usuniête, ale mimo to jest u¿ytecznym
narzêdziem.

Przeczytaj plik HONESTY!

%prep
%setup -q

%build
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_sysconfdir}/%{name}}

install filtergen $RPM_BUILD_ROOT%{_sbindir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/simple.conf

gzip -9nf README HONESTY HISTORY TODO tests/*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz tests
%attr(755,root,root) %{_sbindir}/filtergen
%dir %{_sysconfdir}/%{name}
%{_sysconfdir}/%{name}/simple.conf
