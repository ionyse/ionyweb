===============================
Working with Themes and Layouts
===============================

Some themes and layouts are provided with modulo.

In the code they are on `modulo/contrib`.

In your modulo project, you can also put some local themes and layout.

Don't forget to define the `LAYOUTS_DIR` and `THEMES_DIR` in you settings. ::
    
    LAYOUTS_DIRS = (
        os.path.join(ABSOLUTE_PATH, 'layouts'),
    )
    
    THEMES_DIRS = (
        os.path.join(ABSOLUTE_PATH, 'themes'),
    )

Files tree of a theme
=====================

On a theme, you must create a `MANIFEST.json`::

    {"title": "Jungle Land",
     "description": "A stylish warm brown design suitable for environmental community and nature business website.",
     "author": "styleshout",
     "website": "http://www.styleshout.com/",
     "date": "01/09/2009",
     "preview": ["jungleland.jpg"]
    }

You can define one or more preview images that will slideshow to present your theme.

Then you must to have a `templates` directory with all your template
inside.  They will be find there by the
`modulo.loaders.themes_templates.Loader` when you are looking for
`'themes/jungleland/index.html'`

All the other file outside the `templates` dir are static files and will be collected.

For example::

    themes/
    └── jungleland
        ├── css
        │   ├── ie6.css
        │   ├── Jungleland.css
        │   ├── reset.css
        │   └── screen.css
        ├── images
        │   ├── arrow-up.gif
        │   ├── bg.gif
        │   ├── bullet.gif
        │   ├── button-bg.png
        │   ├── button-hover-bg.png
        │   ├── clock.gif
        │   ├── comment.gif
        │   ├── content-bg.jpg
        │   ├── email.gif
        │   ├── feed-icon14.gif
        │   ├── feed-icon16.gif
        │   ├── firefox-gray.jpg
        │   ├── footer-bg.png
        │   ├── gravatar.jpg
        │   ├── header-bg.jpg
        │   ├── header-search.png
        │   ├── img-featured.jpg
        │   ├── img-post.jpg
        │   ├── left-nav-bg.gif
        │   ├── quote.gif
        │   ├── ribbon.gif
        │   ├── ribbon.png
        │   ├── right-nav-bg.gif
        │   ├── search.png
        │   ├── sep-bg.jpg
        │   ├── thumb-1.jpg
        │   ├── thumb-2.jpg
        │   ├── thumb-3.jpg
        │   ├── thumb-4.jpg
        │   ├── thumb.jpg
        │   └── twitter.gif
        ├── jungleland.jpg
        ├── MANIFEST.json
        └── templates
            ├── archives.html
            ├── blog.html
            ├── index.html
            └── style.html
    
    4 directories, 41 files

Files tree of a layout
======================

The layout works the same way except that there is no MAFIFEST.json or preview.

The layout is defined in the `layout.html` file. Every other file in
this directory is considered as a staticfiles and may be access with a browser.

You may access them using `/static/layouts/<slug>/file.png`

To access the layout template you can use `layouts/<slug>.html` or even `layouts/<slug>/`.

For example, see the contrib layouts of modulo::

    layouts
    ├── 100
    │   ├── layout.css
    │   └── layout.html
    │   └── MANIFEST.json
    │   └── icon-layout.png
    ├── 100_100
    │   ├── layout.css
    │   └── layout.html
    ├── 100_100_100
    │   ├── layout.css
    │   └── layout.html
    ├── 100_100_100_100
    │   ├── layout.css
    │   └── layout.html
    ├── 100_65-35
    │   ├── layout.css
    │   └── layout.html
    └── 50-50_100
        ├── layout.css
        └── layout.html
    
    6 directories, 12 files

Each slug of the list represents the structure of the layout.
The char '_' is a new row and the char '-' represents a column of the current row.
The values ​​used represent the width of each placeholder, as a percentage of the width of the site.

For example, layout `100_100_100` is a layout of three lines, each containing a placeholder of 100% of the width.
Similarly, the layout `100_65-35` consists of two lines. The first one contains a placeholder 100% width
and the second 2 placeholders 65% and 35% of the width.


Create customs layouts
======================

To add your customs layouts, create a new dir in your layouts project dir. The name of the dir will be the slug of the layout.

Now, create a `layout.html` file which contains the structure of the layout, i.e. the number of placeholders you want.
`Modulo` contains 10 default structures for layouts.

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
