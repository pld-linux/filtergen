Summary:	Simple packet filter generator
Summary(pl):	Prosty generator filtrów pakietów
Name:		filter
Version:	0.9
Release:	2
License:	GPL
Group:		Networking/Utilities
Source0:	http://hairy.beasts.org/filter/%{name}-%{version}.tar.gz
Source1:	%{name}.conf
Source2:	%{name}.sysconfig
Source3:	%{name}.init
Patch0:		%{name}-types.patch
URL:		http://hairy.beasts.org/filter/
BuildRequires:	flex
Prereq:		rc-scripts
Prereq:		/sbin/chkconfig
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
%patch -p1

%build
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -Wall -Werror"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_sysconfdir}/%{name}} \
	$RPM_BUILD_ROOT%{_sysconfdir}/{sysconfig,rc.d/init.d}

install filtergen $RPM_BUILD_ROOT%{_sbindir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/simple.conf
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/%{name}
install %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/%{name}
touch $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/generated_rules

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add filter
if [ -f /var/lock/subsys/filter ]; then
        /etc/rc.d/init.d/filter restart >&2
else
        echo "Run \"/etc/rc.d/init.d/filter start\" to start filter"
fi

%preun
if [ "$1" = "0" ]; then
        if [ -f /var/lock/subsys/filter ]; then
                /etc/rc.d/init.d/filter stop >&2
        fi
        /sbin/chkconfig --del filter
fi

%files
%defattr(644,root,root,755)
%doc README HONESTY HISTORY TODO tests
%attr(755,root,root) %{_sbindir}/filtergen
%dir %{_sysconfdir}/%{name}
%attr(600,root,root) %{_sysconfdir}/%{name}/simple.conf
%attr(600,root,root) %{_sysconfdir}/%{name}/generated_rules
%attr(600,root,root) %{_sysconfdir}/sysconfig/%{name}
%attr(754,root,root) %{_sysconfdir}/rc.d/init.d/%{name}
