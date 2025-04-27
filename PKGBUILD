# Maintainer: Finn <github.com/FiOS-repo>

pkgname=timi
pkgver=1.1.0
pkgrel=1
pkgdesc="A simple CLI timer utility"
arch=('any')
url="https://github.com/FiOS-repo/timi"
license=('MIT')
depends=('python' 'python-colorama')
makedepends=('git')
source=("git+https://github.com/FiOS-repo/timi.git#branch=master")
sha256sums=('SKIP')

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
