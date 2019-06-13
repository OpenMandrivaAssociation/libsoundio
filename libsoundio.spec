%define major 1
%define libname %mklibname soundio %{major}
%define devname %mklibname soundio -d

Summary:	C library for cross-platform real-time audio input and output
Name:		libsoundio
Version:	1.1.0
Release:	1
License:	MIT
Group:		Sound
Url:		http://libsound.io/
Source0:	https://github.com/andrewrk/libsoundio/archive/%{version}/%{name}-%{version}.tar.gz
BuildRequires:	cmake
BuildRequires:	doxygen
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(jack)
BuildRequires:	pkgconfig(libpulse)
Requires:	%{libname} = %{EVRD}

%description
C library providing cross-platform audio input and output. The API is suitable
for real-time software such as digital audio workstations as well as consumer
software such as music players. This library is an abstraction; however in the
delicate balance between performance and power, and API convenience, the scale
is tipped closer to the former. Features that only exist in some sound
backends are exposed.

%files
%doc CHANGELOG.md LICENSE README.md
%{_bindir}/sio_*

#-----------------------------------------------------------------------------

%package -n %{libname}
Summary:	Library files for %{name}
Group:		System/Libraries

%description -n %{libname}
This package contains the library files for %{name}.

%files -n %{libname}
%doc LICENSE
%{_libdir}/%{name}.so.%{major}*

#-----------------------------------------------------------------------------

%package -n %{devname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Provides:	soundio-devel = %{EVRD}

%description -n %{devname}
This package contains libraries and header files for developing applications
that use %{name}.

%files -n %{devname}
%doc CHANGELOG.md LICENSE
%doc build/html/*
%{_includedir}/soundio/*.h
%{_libdir}/%{name}.so
%{_datadir}/cmake/Modules/FindSoundIo.cmake

#-----------------------------------------------------------------------------

%prep
%setup -q

%build
%cmake \
	-DBUILD_STATIC_LIBS="OFF" \
	-DBUILD_TESTS="OFF" \
	-DENABLE_COREAUDIO="OFF" \
	-DENABLE_WASAPI="OFF" \
	-DCMAKE_BUILD_TYPE=Release
%make

# Since this is a library, build dev docs
%make doc

%install
%makeinstall_std -C build

# Install the cmake module for the library
mkdir -p %{buildroot}/%{_datadir}/cmake/Modules/
install -m 0644 doc/FindSoundIo.cmake %{buildroot}/%{_datadir}/cmake/Modules/
