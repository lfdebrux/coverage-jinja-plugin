
import unittest

import coverage
from jinja2 import Environment
from jinja2.loaders import PackageLoader
from jinja2.exceptions import TemplateSyntaxError

import os.path


class JinjaPluginTestCase(unittest.TestCase):
    """Base class for tests of the Jinja2 coverage.py plugin."""

    def _render(self, template_filename, context={}):
        "Helper method"
        env = Environment(
                loader=PackageLoader('tests', 'templates'),
                extensions=[],
            )
        template = env.get_template(template_filename)
        return template.render(context).strip()

    def do_jinja_coverage(self, template, context={}):
        """Run a Jinja coverage test.

        Args:
            template (str): the filename of the template.
            context (dict): data for the template.

        Returns:
            A tuple: (rendered_text, line_data)
            rendered_text: the rendered text.
            line_data: a list of line numbers executed.

        """
        template_dir = 'tests/templates'
        cov = coverage.Coverage(source=[template_dir])
        cov.config.plugins.append('jinja_coverage')
        cov.config.plugin_options['jinja_coverage'] = {'template_directory': template_dir}
        cov.start()
        text = self._render(template, context)
        cov.stop()
        cov.save()
        abs_path = os.path.abspath(os.path.join(template_dir, template))
        line_data = cov.data.lines(abs_path)
        return text, line_data
