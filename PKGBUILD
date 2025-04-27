# Maintainer: Finn <github.com/FiOS-repo>

pkgname=timi
pkgver=1.1.0
pkgrel=1
pkgdesc="A simple CLI timer utility"
arch=('any')
url="https://github.com/FiOS-repo/timi"
license=('MIT')
depends=('python' 'python-colorama' 'python-notify2')
makedepends=('git' 'python-build' 'python-installer' 'python-wheel')
source=("git+https://github.com/FiOS-repo/timi.git#branch=master"
        "git+https://aur.archlinux.org/python-plyer.git")
sha256sums=('SKIP'
            'SKIP')

prepare() {
    # Build python-plyer from AUR
    cd "$srcdir/python-plyer"
    makepkg -si --noconfirm
}

package() {
    cd "$srcdir/$pkgname"
    
    # Create required directories
    install -dm755 "$pkgdir/usr/bin"
    install -dm755 "$pkgdir/usr/lib/python3/site-packages/timi"
    install -dm777 "$pkgdir/var/timi/timers"
    
    # Install Python files
    install -Dm644 main.py "$pkgdir/usr/lib/python3/site-packages/timi/"
    install -Dm644 timedeamon.py "$pkgdir/usr/lib/python3/site-packages/timi/"
    
    # Create executable wrapper
    echo '#!/bin/sh' > "$pkgdir/usr/bin/timi"
    echo 'python /usr/lib/python3/site-packages/timi/main.py "$@"' >> "$pkgdir/usr/bin/timi"
    chmod 755 "$pkgdir/usr/bin/timi"
}