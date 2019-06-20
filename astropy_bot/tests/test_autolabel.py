# For these tests, we patch the repo and pull request handler directly rather
# than the requests to the server, as we assume the repo and pull request
# handlers are tested inside baldrick.

from unittest.mock import MagicMock

from astropy_bot.autolabel import autolabel_subpackages


class TestAutolabel:

    def setup_method(self, method):

        self.files = ['CHANGES.rst', 'astropy/io/fits/convenience.py',
                      'astropy/io/fits/fitstime.py',
                      'astropy/io/fits/tests/test_fitstime.py',
                      'astropy/coordinates/baseframe.py',
                      'astropy/visualization/wcsaxes/coordinate_helpers.py']

        self.all_labels = ['analytic_functions', 'config', 'constants',
                           'convolution', 'coordinates', 'cosmology',
                           'io.ascii', 'io.fits', 'io.misc', 'io.misc.asdf',
                           'io.registry', 'io.votable', 'modeling', 'nddata',
                           'samp', 'stats', 'table', 'time', 'timeseries',
                           'uncertainty', 'units', 'utils', 'visualization',
                           'visualization.wcsaxes', 'vo', 'vo.conesearch',
                           'wcs', 'wcs.wcsapi']

        self.pr_handler = MagicMock()
        self.pr_handler.number = 1234
        self.pr_handler.labels = ['Docs']
        self.pr_handler.milestone = None
        self.pr_handler.set_labels = self.set_labels
        self.pr_handler.get_modified_files = self.get_modified_files

        self.repo_handler = MagicMock()
        self.repo_handler.get_all_labels = self.get_all_labels

    # Patched methods:
    def get_modified_files(self):
        return self.files

    def get_all_labels(self):
        return self.all_labels

    def set_labels(self, labels):
        self.labels = labels

    # Tests:
    def test_autolabel_subpackages(self, app):
        with app.app_context():
            autolabel_subpackages(self.pr_handler, self.repo_handler)

        # make sure 'Docs' stays in there:
        assert 'Docs' in self.pr_handler.labels

        # now check that all the subpackage labels are added:
        assert 'io.fits' in self.labels
        assert 'coordinates' in self.labels
        assert 'visualization.wcsaxes' in self.labels
