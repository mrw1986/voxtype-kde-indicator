Name:           voxtype-kde-indicator
Version:        1.0.0
Release:        1%{?dist}
Summary:        Recording indicator and OSD overlay for Voxtype on KDE Plasma 6

License:        MIT
URL:            https://github.com/mrw1986/voxtype-kde-indicator
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  systemd-rpm-macros

Requires:       gtk4-layer-shell
Requires:       python3-gobject
Recommends:     python3-PyQt6

%description
A non-focus-stealing OSD overlay for Voxtype voice-to-text on KDE Plasma 6
Wayland. Shows a centered recording/transcribing indicator using GTK4 and
the zwlr_layer_shell_v1 protocol. Includes a notify-send shim to suppress
Voxtype's built-in notifications and an optional PyQt6 system tray icon.

%prep
%autosetup -n %{name}-%{version}

%install
# Scripts
install -Dpm 755 scripts/voxtype-overlay %{buildroot}%{_libexecdir}/%{name}/voxtype-overlay
install -Dpm 755 scripts/voxtype-overlay-wrapper %{buildroot}%{_libexecdir}/%{name}/voxtype-overlay-wrapper
install -Dpm 755 scripts/voxtype-indicator %{buildroot}%{_libexecdir}/%{name}/voxtype-indicator
# Shim installed as "notify-send" so it shadows the real binary via PATH
install -Dpm 755 scripts/notify-send-shim %{buildroot}%{_libexecdir}/%{name}/notify-send

# Systemd user units — template paths from rpm/ versions
install -d %{buildroot}%{_userunitdir}
install -d %{buildroot}%{_userunitdir}/voxtype.service.d

sed -e 's|@@LIBEXECDIR@@|%{_libexecdir}|g' \
    rpm/voxtype-overlay.service > %{buildroot}%{_userunitdir}/voxtype-overlay.service
chmod 644 %{buildroot}%{_userunitdir}/voxtype-overlay.service

sed -e 's|@@LIBEXECDIR@@|%{_libexecdir}|g' \
    rpm/voxtype-indicator.service > %{buildroot}%{_userunitdir}/voxtype-indicator.service
chmod 644 %{buildroot}%{_userunitdir}/voxtype-indicator.service

sed -e 's|@@LIBEXECDIR@@|%{_libexecdir}|g' \
    rpm/voxtype-no-notify.conf > %{buildroot}%{_userunitdir}/voxtype.service.d/no-notify.conf
chmod 644 %{buildroot}%{_userunitdir}/voxtype.service.d/no-notify.conf

%post
%systemd_user_post voxtype-overlay.service voxtype-indicator.service

%preun
%systemd_user_preun voxtype-overlay.service voxtype-indicator.service

%postun
%systemd_user_postun_with_restart voxtype-overlay.service voxtype-indicator.service

%files
%license LICENSE
%doc README.md screenshots/
%dir %{_libexecdir}/%{name}
%{_libexecdir}/%{name}/voxtype-overlay
%{_libexecdir}/%{name}/voxtype-overlay-wrapper
%{_libexecdir}/%{name}/voxtype-indicator
%{_libexecdir}/%{name}/notify-send
%{_userunitdir}/voxtype-overlay.service
%{_userunitdir}/voxtype-indicator.service
%dir %{_userunitdir}/voxtype.service.d
%{_userunitdir}/voxtype.service.d/no-notify.conf

%changelog
* Tue Feb 24 2026 Matt Wilson <mrw1986@gmail.com> - 1.0.0-1
- Initial RPM release
- OSD overlay with GTK4 + layer-shell (non-focus-stealing)
- Microphone icon with pulsing glow, bouncing dots for transcribing
- Fade in/out transitions with idle debounce
- notify-send shim for notification suppression
- Optional PyQt6 system tray icon
