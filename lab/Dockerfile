FROM php:8.3-cli-bookworm

ENV DEBIAN_FRONTEND=noninteractive \
    PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

RUN mkdir -p /lab/pin-src /oracle

COPY bin/w /usr/local/bin/w
COPY bin/w /bin/w
COPY bin/ifconfig /sbin/ifconfig
COPY gadget.php stubs.php health.php /lab/
COPY pin-src/ /lab/pin-src/

RUN chmod 0755 /usr/local/bin/w /bin/w /sbin/ifconfig \
    && chmod 0755 /oracle \
    && php -l /lab/gadget.php \
    && php -l /lab/stubs.php \
    && php -l /lab/pin-src/globals.inc.excerpt.php \
    && php -l /lab/pin-src/util.inc.excerpt.php \
    && php -l /lab/pin-src/interfaces.inc.excerpt.php \
    && php -l /lab/pin-src/interfaces_vlan_edit.php.excerpt.php \
    && php -l /lab/pin-src/interfaces_qinq_edit.php.excerpt.php

WORKDIR /lab
EXPOSE 18810

CMD ["php", "-S", "0.0.0.0:18810", "-t", "/lab"]
