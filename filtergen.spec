Summary:	Simple packet filter generator
Summary(pl):	Prosty generator filtrów pakietów
Name:		filtergen
Version:	0.11
Release:	1
License:	GPL
Group:		Networking/Utilities
Source0:	http://hairy.beasts.org/filter/%{name}-%{version}.tar.gz
# Source0-md5:	de33c1dce928fe240b036498e56e545f
Source1:	filter.conf
Source2:	filter.sysconfig
Source3:	filter.init
URL:		http://hairy.beasts.org/filter/
BuildRequires:	flex
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
Provides:	firewall
Obsoletes:	filter
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
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -Wall -Werror -Wno-unused"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_sysconfdir}/filter} \
	$RPM_BUILD_ROOT/etc/{sysconfig,rc.d/init.d} \
	$RPM_BUILD_ROOT%{_mandir}/man{5,7,8}

install filtergen $RPM_BUILD_ROOT%{_sbindir}
install filter_syntax.5 $RPM_BUILD_ROOT%{_mandir}/man5
install filter_backends.7 $RPM_BUILD_ROOT%{_mandir}/man7
install filtergen.8 $RPM_BUILD_ROOT%{_mandir}/man8
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/filter/simple.conf
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}
install %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
touch $RPM_BUILD_ROOT%{_sysconfdir}/filter/generated_rules

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add filtergen
if [ -f /var/lock/subsys/filtergen ]; then
	/etc/rc.d/init.d/filtergen restart >&2
else
	echo "Run \"/etc/rc.d/init.d/filtergen start\" to start filtergen"
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/filtergen ]; then
		/etc/rc.d/init.d/filtergen stop >&2
	fi
	/sbin/chkconfig --del filtergen
fi

%files
%defattr(644,root,root,755)
%doc README HONESTY HISTORY TODO tests
%attr(755,root,root) %{_sbindir}/filtergen
%dir %{_sysconfdir}/filter
%attr(600,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/filter/simple.conf
%attr(600,root,root) %{_sysconfdir}/filter/generated_rules
%attr(600,root,root) /etc/sysconfig/%{name}
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%{_mandir}/man5/*
%{_mandir}/man7/*
%{_mandir}/man8/*
