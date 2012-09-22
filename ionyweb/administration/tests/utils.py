# -*- coding: utf-8 -*-
from django.utils import unittest
from django.conf import settings
from djangorestframework.response import ErrorResponse
from ionyweb.administration.utils import (check_object_html_id as cohi,
                                         check_placeholder_html_id as cphi,
                                         is_page_placeholder_html_id)


class AdministrationUtilsTestCase(unittest.TestCase):

    # -----
    # Tests of utils.check_object_html_id() => cohi()
    # -----

    def test_cohi_default_param_type(self):
        """
        By default, COHI() has to accept only plugin relation html id.
        """
        # Accept a valid html id plugin
        html_id_plugin = '%s%d' % (settings.HTML_ID_PLUGIN, 1)
        items_returned = cohi(html_id_plugin)
        self.assertEqual(items_returned, [settings.SLUG_PLUGIN, '1'])
        # Reject a valid html id App
        html_id_app = '%s%d' % (settings.HTML_ID_APP, 1)
        self.assertRaises(ErrorResponse, cohi, html_id_app)
        
                         
    def test_cohi_one_type_in_param(self):
        """
        Test if cohi() with App type accept only App html id.
        """
        # Params
        types = [settings.SLUG_APP]
        # Accept a valid app html id
        html_id_app = '%s%d' % (settings.HTML_ID_APP, 1)
        items_returned = cohi(html_id_app, types)
        self.assertEqual(items_returned, [settings.SLUG_APP, '1'])
        # Reject a valid plugin html id
        html_id_plugin = '%s%d' % (settings.HTML_ID_PLUGIN, 1)
        self.assertRaises(ErrorResponse, cohi, html_id_plugin, types)

    def test_cohi_two_types_in_param(self):
        """
        Test if cohi() accepts 2 types of html id.
        """
        # Params
        types = [settings.SLUG_PLUGIN, settings.SLUG_APP]
        # Accept a valid html id plugin
        html_id_plugin = '%s%d' % (settings.HTML_ID_PLUGIN, 1)
        items_returned = cohi(html_id_plugin, types)
        self.assertEqual(items_returned, [settings.SLUG_PLUGIN, '1'])
        # Accept a valid html id app
        html_id_app = '%s%d' % (settings.HTML_ID_APP, 1)
        items_returned = cohi(html_id_app, types)
        self.assertEqual(items_returned, [settings.SLUG_APP, '1'])
        # Reject other html id
        html_id_wrong = 'truc-machin-4'
        self.assertRaises(ErrorResponse, cohi, html_id_wrong, types)

    # -----
    # Tests of utils.check_placeholder_html_id() => cphi()
    # -----

    def test_cphi_no_extras_id(self):
        """
        Accept only classic html id, like content-placeholder-4.
        """
        # Accept a valid html id
        valid_html_id = '%s%s%d' % (settings.SLUG_CONTENT,
                              settings.HTML_ID_PLACEHOLDER,
                              3)
        items_returned = cphi(valid_html_id)
        self.assertEqual(items_returned, [settings.SLUG_CONTENT, 
                                          settings.SLUG_PLACEHOLDER,
                                          '3'])
        # Reject a specific html id
        self.assertRaises(ErrorResponse,
                          cphi, settings.HTML_ID_PLACEHOLDER_DEFAULT)

    def test_cphi_with_one_extras_id(self):
        """
        Accept classic and one specific html id.
        """
        # Params
        extras_id = [settings.HTML_ID_PLACEHOLDER_DEFAULT]
        # Accept a valid html id
        valid_html_id = '%s%s%d' % (settings.SLUG_CONTENT,
                              settings.HTML_ID_PLACEHOLDER,
                              3)
        items_returned = cphi(valid_html_id, extras_id)
        self.assertEqual(items_returned, [settings.SLUG_CONTENT, 
                                          settings.SLUG_PLACEHOLDER,
                                          '3'])
        # Accept Default Placeholder
        items_returned = cphi(settings.HTML_ID_PLACEHOLDER_DEFAULT,
                              extras_id)
        self.assertEqual(items_returned,
                         settings.HTML_ID_PLACEHOLDER_DEFAULT)
        # Reject Clipboard Placeholder
        self.assertRaises(ErrorResponse,
                          cphi, settings.HTML_ID_PLACEHOLDER_CLIPBOARD)

    def test_cphi_with_two_extras_id(self):
        """
        Accept classic and two specific html id.
        """
        # Params
        extras_id = [settings.HTML_ID_PLACEHOLDER_DEFAULT,
                     settings.HTML_ID_PLACEHOLDER_CLIPBOARD]
        # Accept a valid html id
        valid_html_id = '%s%s%d' % (settings.SLUG_CONTENT,
                              settings.HTML_ID_PLACEHOLDER,
                              3)
        items_returned = cphi(valid_html_id, extras_id)
        self.assertEqual(items_returned, [settings.SLUG_CONTENT, 
                                          settings.SLUG_PLACEHOLDER,
                                          '3'])
        # Accept Default Placeholder
        items_returned = cphi(settings.HTML_ID_PLACEHOLDER_DEFAULT,
                              extras_id)
        self.assertEqual(items_returned,
                         settings.HTML_ID_PLACEHOLDER_DEFAULT)
        # Accept Clipboard Placeholder
        items_returned = cphi(settings.HTML_ID_PLACEHOLDER_CLIPBOARD,
                              extras_id)
        self.assertEqual(items_returned,
                         settings.HTML_ID_PLACEHOLDER_CLIPBOARD)

    def test_is_page_placeholder_html_id(self):
        layout_slug_content = settings.SLUG_CONTENT
        self.assertTrue(is_page_placeholder_html_id(layout_slug_content))

        layout_slug_content_prefix = '%s_%s' % (settings.SLUG_CONTENT,
                                                'foobar')
        self.assertTrue(is_page_placeholder_html_id(layout_slug_content_prefix))

        placeholder_html_id = '%s%s' % (layout_slug_content_prefix,
                                        settings.HTML_ID_PLACEHOLDER)
        self.assertTrue(is_page_placeholder_html_id(placeholder_html_id))

        wrong_placeholder_html_id = '%s%s' % ('foobar',
                                              settings.HTML_ID_PLACEHOLDER)
        self.assertFalse(is_page_placeholder_html_id(wrong_placeholder_html_id))
        
