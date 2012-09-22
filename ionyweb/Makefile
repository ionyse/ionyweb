#######################
# Cmd projet Django   #
#######################

DEBUG=False
LESS_FILES= static/admin/css/ionyweb_admin_dark.less static/admin/css/ionyweb_login.less
LESS_REQUIREMENTS= static/admin/css/*.less
CSS_FILES=$(LESS_FILES:.less=.min.css)

JS_ENGINE=`which node nodejs 2>/dev/null`
JS_FILES=static/admin/js/ionyweb_admin.js static/admin/js/apps.js static/admin/js/design.js static/admin/js/edit.js static/admin/js/layouts.js static/admin/js/menu.js static/admin/js/messages.js static/admin/js/pages.js static/admin/js/panels.js static/admin/js/plugins.js static/admin/js/settings.js static/admin/js/urls.js static/admin/js/themes.js static/admin/js/file_manager.js

LOGIN_JS_FILES = static/admin/js/ionyweb_admin.js

BUILD_DIR = build

COMPILER = $(JS_ENGINE) $(BUILD_DIR)/uglify.js --unsafe

# PATH TO IONYWEB-BOOTSTRAP REPO
BOOTSTRAP_REPO_DIR = $(PWD)/../../ionyweb-bootstrap
BOOTSTRAP_DEST_DIR = $(PWD)/static/admin
BOOTSTRAP_THEMES_DEST_DIR = $(PWD)/contrib/themes/default

ifeq ($(DEBUG),True)
	LESSC=lessc
else
	LESSC=lessc -x
endif

less: $(CSS_FILES)

%.min.css: %.less $(LESS_REQUIREMENTS)
	(cd `dirname $<`; $(LESSC) `basename $<` > `basename $@`)

js: static/admin/js/ionyweb_admin.min.js static/admin/js/ionyweb_login.min.js
# @@if test ! -z ${JS_ENGINE}; then \
# 	echo "Vérification";\
# 	$(JS_ENGINE) $<;\
# else \
# 	echo "You must have NodeJS installed in order to test ionyweb_admin."; \
# fi

static/admin/js/ionyweb_admin.min.js: $(JS_FILES)
	cat $^ > $@;
	@@if test ! -z ${JS_ENGINE}; then \
		${COMPILER} $@ > $@.tmp; \
		mv $@.tmp $@; \
		rm -f $@.tmp;\
	else \
		echo "You must have NodeJS installed in order to minify ionyweb_admin."; \
	fi

static/admin/js/ionyweb_login.min.js: $(LOGIN_JS_FILES)
	cat $^ > $@;
	@@if test ! -z ${JS_ENGINE}; then \
		${COMPILER} $@ > $@.tmp; \
		mv $@.tmp $@; \
		rm -f $@.tmp;\
	else \
		echo "You must have NodeJS installed in order to minify ionyweb_login."; \
	fi

# Local development management
clean:
	find . -name "*~" -exec rm -fr {} \;
	find . -name "*.pyc" -exec rm -fr {} \;
	find . -name ".DS_Store" -exec rm -fr {} \;
	find . -name "Thumbs.db" -exec rm -fr {} \;
	find . -name "Thumbs.db:encryptable" -exec rm -fr {} \;

messages-fr:
	django-admin.py makemessages -l fr --ignore=page_app/* --ignore=plugin_app/*

js-messages-fr:
	django-admin.py makemessages -d djangojs -l fr --ignore=page_app/* --ignore=plugin_app/* --ignore=static/admin/js/*.min.js

compilemessages:
	django-admin.py compilemessages

bootstrap:
	(cd $(BOOTSTRAP_REPO_DIR); hg pull; hg up ionyweb; make bootstrap)
	rm -fr $(BOOTSTRAP_DEST_DIR)/bootstrap
	mv $(BOOTSTRAP_REPO_DIR)/bootstrap/ $(BOOTSTRAP_DEST_DIR)

theme-default:
	(cd $(BOOTSTRAP_REPO_DIR); hg pull; hg up themes; make bootstrap)
	mv $(BOOTSTRAP_REPO_DIR)/bootstrap/* $(BOOTSTRAP_THEMES_DEST_DIR)
	rmdir $(BOOTSTRAP_REPO_DIR)/bootstrap/
