PKGNAME=argo-probe-eudat-b2handle
SPECFILE=${PKGNAME}.spec
FILES=check_epic_api.py epicclient.py check_handle_resolution.pl check_handle_api.py ${SPECFILE}

PKGVERSION=$(shell grep -s '^Version:' $(SPECFILE) | sed -e 's/Version:\s*//')

rpm: dist
	rpmbuild -ta ${PKGNAME}-${PKGVERSION}.tar.gz

dist:
	rm -rf dist
	mkdir -p dist/${PKGNAME}-${PKGVERSION}
	cp -pr ${FILES} dist/${PKGNAME}-${PKGVERSION}/
	tar zcf dist/${PKGNAME}-${PKGVERSION}.tar.gz -C dist ${PKGNAME}-${PKGVERSION}
	mv dist/${PKGNAME}-${PKGVERSION}.tar.gz .
	rm -rf dist

sources: dist

clean:
	rm -rf ${PKGNAME}-${PKGVERSION}.tar.gz
	rm -rf dist
