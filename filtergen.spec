Summary:	Simple packet filter generator
Summary(pl):	Prosty generator filtr�w pakiet�w
Name:		filter
Version:	0.9
Release:	3
License:	GPL
Group:		Networking/Utilities
Source0:	http://hairy.beasts.org/filter/%{name}-%{version}.tar.gz
# Source0-md5:	dda501b978046a1ea4bf764677e4d5cf
Source1:	%{name}.conf
Source2:	%{name}.sysconfig
Source3:	%{name}.init
Patch0:		%{name}-types.patch
URL:		http://hairy.beasts.org/filter/
BuildRequires:	flex
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
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
To jest narz�dzie do generowania regu� filtrowania pakiet�w z
wzgl�dnie wysokopoziomowego j�zyka opisu. Nie obs�uguje wszystkich
zaawansowanych mo�liwo�ci najnowszych filtr�w pakiet�w, ale wspiera
przyzwoity podzbi�r, wystarczaj�cy dla typowych stacji roboczych.

Aktualnie obs�uguje tylko linuksowe iptables i ipchains. Obs�uga Cisco
IOS jest zacz�ta, ale nie kompletna. ipfilter Darrena Reeda jest
obs�ugiwany cz�ciowo. Nie generuje optymalnych regu�ek i ma par�
ogranicze�, kt�re powinny by� usuni�te, ale mimo to jest u�ytecznym
narz�dziem.

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
	$RPM_BUILD_ROOT%{_sysconfdir}/{sysconfig,rc.d/init.d} \
	$RPM_BUILD_ROOT%{_mandir}/man{5,7,8}

install filtergen $RPM_BUILD_ROOT%{_sbindir}
install filter_syntax.5 $RPM_BUILD_ROOT%{_mandir}/man5
install filter_backends.7 $RPM_BUILD_ROOT%{_mandir}/man7
install filtergen.8 $RPM_BUILD_ROOT%{_mandir}/man8
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/simple.conf
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}
install %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
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
%attr(600,root,root) /etc/sysconfig/%{name}
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%{_mandir}/man5/*
%{_mandir}/man7/*
%{_mandir}/man8/*
