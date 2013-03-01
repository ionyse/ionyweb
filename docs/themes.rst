===============================
Working with Themes and Layouts
===============================

Some themes and layouts are provided with ionyweb.

In the code they are on `ionyweb/contrib/`.

In your ionyweb project, you can also put some local themes and layout.

Don't forget to define the `LAYOUTS_DIR` and `THEMES_DIR` in you settings. ::
    
    LAYOUTS_DIRS = (
        os.path.join(ABSOLUTE_PATH, 'layouts'),
        os.path.join(get_ionyweb_path(), 'contrib', 'layouts'),
    )
    
    THEMES_DIRS = (
        os.path.join(ABSOLUTE_PATH, 'themes'),
        os.path.join(get_ionyweb_path(), 'contrib', 'themes'),
    )

------
Themes
------

Files tree of a theme
=====================

On a theme, you must create a `MANIFEST.json`::

    {"title": "Jungleland",
     "description": "A stylish warm brown design suitable for environmental community and nature business website.",
     "author": "styleshout",
     "website": "http://www.styleshout.com/",
     "date": "01/09/2009",
     "preview": "jungleland.jpg",
	 "editable": false
    }

You must define a preview image that will give a visual overview of your theme.

A theme can have multiple styles, if you need only one, you must call it ``default``.

Then you must to have a `templates` directory with all your template
inside.  They will be find there by the
`ionyweb.loaders.themes_templates.Loader` when you are looking for
`'themes/notmyidea/index.html'`

All the other file outside the `templates` dir are static files and will be collected.

For example::

    themes/
    └── notmyidea
        ├── default
        │   ├── css
        │   │   ├── main.css
        │   │   ├── reset.css
        │   │   ├── styles.css
        │   │   ├── typogrify.css
        │   │   └── wide.css
        │   ├── images
        │   │   └── icons
        │   │       ├── delicious.png
        │   │       ├── lastfm.png
        │   │       ├── linkedin.png
        │   │       ├── rss.png
        │   │       └── twitter.png
        │   └── templates
        │       ├── index.html
        │       └── navigation.html
        ├── favicon.ico
        ├── MANIFEST.json
        └── preview.png
    
    6 directories, 15 files


Create a custom theme
=====================

Most of the time, you just need to inherit from ``templates/themes/html5.html`` file::

    {% load ionyweb_tags i18n %}
    {# Minimum HTML5 template #}
    <!DOCTYPE html>
    {% get_current_language as LANGUAGE_CODE %}
    <html lang="{% firstof LANGUAGE_CODE "en" %}">
      <head>
        {% admin_toolbar_medias %}
    
        {% block head %}
        	{% block header_title %}
          		<title>{% title %} - {{ request.website.title }}</title>
          	{% endblock %}
          <meta charset="utf-8">
          <meta name="viewport" content="width=device-width, initial-scale=1.0">
          <!-- Le HTML5 shim, for IE6-8 support of HTML5 elements -->
          <!--[if lt IE 9]>
    	<script src="http://html5shim.googlecode.com/svn/trunk/html5.js"></script>
          <![endif]-->
          {% render_favicon %}
          {% block theme-design-css %}{% endblock %}
          {% block theme-design-js %}{% endblock %}
        {% endblock %}
    
        {% render_meta_kw %}
        {% render_meta_description %}
        {% render_medias %}
      </head>
    
      {% block body-tag %}
      <body>
      {% endblock %}
    
        {% admin_toolbar %}
    
        {% block top_body %}{% endblock %}
    
        {% block body %}
    
          <!-- Header -->
          {% block header %}
            <header>{% render_layout "header" %}</header>
          {% endblock %}
          <!-- End of Header -->
    
          <!-- Navigation -->
          {% block navigation %}
            <nav>{% render_navigation %}</nav>
          {% endblock %}
          <!-- End of Navigation -->
    
          <!-- Content -->
          {% block content %}
            <div id="main-content">
              {% block page %}{% render_page %}{% endblock %}
            </div>
          {% endblock %}
          <!-- End of Content -->
    
          <!-- Footer -->
          {% block footer %}
            <footer>{% render_layout "footer" %}</footer>
          {% endblock %}
          <!-- End of Footer -->
          {% render_clipboard %}
          
          {% block render_default %}
            {% render_default %}
          {% endblock %}
    
        {% endblock %}
    
        {% googleanalytics %}
        {% block extra-medias %}{% endblock %}
    
        {% block bottom_body %}{% endblock %}
    
      </body>
    
    </html>


This file is the minimum working Ionyweb theme.

The ``ionyweb_tags`` templatetags provide quite a few tags:

**Load the admin interface**

 - ``{% admin_toolbar_medias %}`` that will load the static file for the admin interface
 - ``{% admin_toolbar %}`` that will load the html needed for the admin interface


**Load the header**

 - ``{% render_favicon %}`` : Load the favicon of the theme.
 - ``{% render_meta_kw %}`` : Render the page meta keywords
 - ``{% render_meta_description %}`` : Render the page meta description


**Load the content**

 - ``{% render_medias %}`` : Render the medias needed by plugins and
   page's apps
 - ``{% render_layout "header" %}`` : Render layout that contains
   plugins that will be displayed on all pages. You can create as many
   layout as you want by changing its name.
 - ``{% render_page %}``: Render the content of the page. Plugins
   specific to this page and the Page App content
 - ``{% render_navigation %}`` : Load the navigation and generate the
   menu.
 - ``{% render_clipboard %}`` : Display the clipboard that allows you
   to change a plugin from one page to another.
 - ``{% render_default %}`` : This is the garbage collector for
   plugins. Since some layout have more placeholders than other, when
   changing between layouts, some plugins may disapear. They will be
   displayed here if the placeholder they used to be linked to is not
   there anymore.
 - ``{% googleanalytics %}`` : Display the google analytics code.

Then there is blocks that you can extends to add some functionnality
to your theme.

It is a good idea to extends this file, so that if a modification is
needed, you theme will still be compatible with future ionyweb
versions.

Using different templates for a theme
-------------------------------------

Most of the time, a theme will be an index.html file then everything
else is manage with layouts.

But is certains circumstances, you need more.

Hopefully Ionyweb is flexible.

You can define in your MANIFEST.json a list of template that you will
be able to select in the page form::

    {"title": "Eurochene",
     "description": "Thème pour la Scierie Eurochêne",
     "author": "Agence Esprit Nomade",
     "website": "http://www.agence-esprit-nomade.com/",
     "date": "26/06/2012",
     "preview": "eurochene.png",
     "editable": false,
     "templates": [
         {"title": "Standard", "file": "index.html", "preview": "index.png"},
         {"title": "Home page", "file": "home.html", "preview": "home.png"},
         {"title": "Which Product", "file": "quel-produit.html", "preview": "which-product.png"},
         {"title": "Slideshow History", "file": "story.html", "preview": "story.png"},
         {"title": "Slideshow Metiers", "file": "metiers.html", "preview": "metiers.png"},
         {"title": "Slideshow Certification", "file": "certifications.html", "preview": "certification.png"},
         {"title": "Slideshow International", "file": "international.html", "preview": "international.png"},
         {"title": "Slideshow Chêne", "file": "chene.html", "preview": "chene.png"},
         {"title": "Slideshow Qualités et Normes", "file": "qualites_normes.html", "preview": "qualites.png"},
         {"title": "Slideshow Nos Références", "file": "references.html", "preview": "references.png"},
         {"title": "Slideshow Produits innovants", "file": "Produits-innovants.html", "preview": "produits-innovants.png"},
         {"title": "Slideshow Hêtre", "file": "hetre.html", "preview": "hetre.png"},
         {"title": "Slideshow Approvisionnement", "file": "approvisionnement.html", "preview": "approvisionnements.png"},
         {"title": "Slideshow Feuillus Divers", "file": "feuillus_divers.html", "preview": "feuillus-divers.png"}]
    }

The template variable is a list of available templates defined with a
title a file and a preview image. The preview should be about 200px high.

Each template file will be used to load the specific page template. Here is the ``certification.html`` template::

    {% extends 'themes/eurochene/default/index.html' %}
    {% load static from staticfiles %}
    {% load i18n %}
    
    {% block slideshow %}
    	<img src="{% static 'themes/eurochene/default/images/certifications/eurochene-scierie-certifications.jpg' %}"
    	     alt="{% trans "Eurochêne sawmill, Beech Forest French" %}"
    	     title="{% trans "Eurochêne sawmill, Beech Forest French" %}" />
    	<img src="{% static 'themes/eurochene/default/images/certifications/eurochene-scierie-bandeau-foret-hetre.jpg' %}"
    	     alt="{% trans "Eurochêne sawmill, Beech Forest French" %}"
    	     title="{% trans "Eurochêne sawmill, Beech Forest French" %}" />
    {% endblock %}



Customize the navigation
========================

One of the tricky thing you want to change each time you create a menu
is the navigation.

With ionyweb, the navigation is rendered with ``{% render_navigation %}``

The default navigation template ``templates/themes/navigation.html`` looks like this::

    {% load mptt_tags %}
    
    <ul>
      {% recursetree menu %}
      <li class="{% if page.lft >= node.lft and page.rght <= node.rght and page.tree_id == node.tree_id %}selected {% endif %}{% if node.draft %}draft{% endif %}">
        <a href="{{ node.get_absolute_url }}">{% firstof node.menu_title node.title %}</a>
        {% if children %}
        <ul class="submenu">
          {{ children }}
        </ul>
        {% endif %}
      </li>
      {% endrecursetree %}
    </ul>		

And it is loaded by the ``templates/theme/html5.html`` with ``{% render_navigation %}``.

If you need to change it, you can create a
``themes/YOUR_THEME/default/templates/navigation.html`` file which
will improve this. As an example, you can create this file::

    <ul class="nav">
    {% for m in menu %}
      {% if m.level == 0 %}
    	{% if m.app_page_type.model != 'pageapp_contact' %}
            <li{% if page.lft >= m.lft and page.rght <= m.rght and page.tree_id == m.tree_id %} class="activate"{% endif %}><a href="{{ m.get_absolute_url }}">{% firstof m.menu_title m.title %}</a></li>
    	{% else %}
    	</ul>
    	<ul class="contact">
    		<li><a href="{{ m.get_absolute_url }}">{% firstof m.menu_title m.title %}</a></li>
    	{% endif %}
      {% endif %}
    {% endfor %}
    </ul>

So that Ionyweb can always displays panels on top of theme content you must not use any z-index above 9000 as these are reserved for Ionyweb admin panels. 




-------
Layouts
-------

Files tree of a layout
======================

The layout works the same way but the MANIFEST.json is much simpler. ::

    {"title": "100% - 1 placeholder",
     "preview": "icon-layout.png"
    }

The preview must show the placeholder organization of the layout.

The layout is defined in the `layout.html` file. Every other file in
this directory is considered as a staticfiles and may be access with a browser.

You may access them using `/static/layouts/<slug>/file.png`

To access the layout template you can use `layouts/<slug>.html` or even `layouts/<slug>/`.

For example, see the contrib layouts of ionyweb::

    layouts/
    ├── 100
    │   ├── icon-layout.png
    │   ├── layout.html
    │   └── MANIFEST.json
    ├── 100_25-25-25-25_100
    │   ├── icon-layout.png
    │   ├── layout.html
    │   └── MANIFEST.json
    ├── 100_33-33-33_100
    │   ├── icon-layout.png
    │   ├── layout.html
    │   └── MANIFEST.json
    ├── 100_50-50_100
    │   ├── icon-layout.png
    │   ├── layout.html
    │   └── MANIFEST.json
    ├── 100_66-33_100_33-66_66-33_33-33-33
    │   ├── icon-layout.png
    │   ├── layout.html
    │   └── MANIFEST.json
    ├── 100_66-33_100_33-66_66-33_50-50
    │   ├── icon-layout.png
    │   ├── layout.html
    │   └── MANIFEST.json
    ├── 33-66
    │   ├── icon-layout.png
    │   ├── layout.html
    │   └── MANIFEST.json
    ├── 50-50_33-33-33_50-50
    │   ├── icon-layout.png
    │   ├── layout.html
    │   └── MANIFEST.json
    ├── 66-33
    │   ├── icon-layout.png
    │   ├── layout.html
    │   └── MANIFEST.json
    └── 66-33_33-66_66-33_33-66
        ├── icon-layout.png
        ├── layout.html
        └── MANIFEST.json
    
    10 directories, 30 files

Each slug of the list represents the structure of the layout.
The char '_' is a new row and the char '-' represents a column of the current row.
The values ​​used represent the width of each placeholder, as a percentage of the width of the site.

For example, layout `50-50_33-33-33_50-50` is a layout of three lines, first with two cells of 50% each, second with 3 cells of 33% and last one with two cells of 50% each.



Create customs layouts
======================

To add your customs layouts, create a new dir in your layouts project dir. The name of the dir will be the slug of the layout.

Now, create a `layout.html` file which contains the structure of the layout, i.e. the number of placeholders you want.

`Ionyweb` contains 10 default structures for layouts.

For example, this is the standard `layout.html` file to create a layout with 5 placeholders::

    {% extends "layout/5-placeholders.html" %}

You can use the default structure `x-placeholders.html` file, where `x` is between 1 and 10.
The rendered template looks like this ::

    {% extends "layout/base.html" %}
    {% load page_extras %}
    
    {% block layout %}

    {% render_placeholder "1" %}
    {% render_placeholder "2" %}
    {% render_placeholder "3" %}
    {% render_placeholder "4" %}
    {% render_placeholder "5" %}

    {% endblock layout %}

You can also define a custom structure file on the same schema.
You must extend the `layout/base.html` and load the `page_extras` templatetags.
Then, overlaod the block `layout` with your own code and use the `render_placeholder` tag to define a placeholder area.
    

Then, you MUST create the `layout.css` to design the placeholders.

If your design file is empty, each placeholder will be a 100% line of the layout.

For example, this file discribes a layout with a first line of 2 columns (50%-50%), 1 line of 1 column (100%) and 1 third row with 2 placeholders (65%-35%)::

    #placeholder-1 { width: 49%; float: left; }
    #placeholder-2 { width: 49%; float: right; }
    #placeholder-3 { clear: both; }
    #placeholder-4 { width: 64%; float: left; }
    #placeholder-5 { width: 34%; float: right; }
    #footer { clear: both; }    

Then you have to create a `MANIFEST.json` file than will give some informations about your layout::

    {"title": "100% - 1 placeholder",
     "preview": "icon-layout.png"
    }

By default, the title will be the directory slug of the layout and the
preview will load `/static/layouts/icon-layout.png`.

Just define the `LAYOUTS_DIRS` in your personnal settings, and now,
you can configure your pages with your new layout !
