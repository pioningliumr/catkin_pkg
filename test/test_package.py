import unittest

from catkin_pkg.package import Package, validate_package, InvalidPackage, \
    Dependency

from mock import Mock


class PackageTest(unittest.TestCase):

    def get_maintainer(self):
        maint = Mock()
        maint.email = 'foo@bar.com'
        maint.name = 'John Foo'
        return maint

    def test_init(self):
        maint = self.get_maintainer()
        pack = Package(name='foo',
                       version='0.0.0',
                       maintainers=[maint],
                       licenses=['BSD'])
        self.assertEqual(None, pack.filename)
        self.assertEqual([], pack.urls)
        self.assertEqual([], pack.authors)
        self.assertEqual([maint], pack.maintainers)
        self.assertEqual(['BSD'], pack.licenses)
        self.assertEqual([], pack.build_depends)
        self.assertEqual([], pack.buildtool_depends)
        self.assertEqual([], pack.run_depends)
        self.assertEqual([], pack.test_depends)
        self.assertEqual([], pack.conflicts)
        self.assertEqual([], pack.replaces)
        self.assertEqual([], pack.exports)
        pack = Package('foo',
                       name='bar',
                       version='0.0.0',
                       licenses=['BSD'],
                       maintainers=[self.get_maintainer()])
        self.assertEqual('foo', pack.filename)

        self.assertRaises(TypeError, Package, unknownattribute=42)

    def test_init_dependency(self):
        dep = Dependency('foo',
                         version_lt=1,
                         version_lte=2,
                         version_eq=3,
                         version_gte=4,
                         version_gt=5)
        self.assertEquals('foo', dep.name)
        self.assertEquals(1, dep.version_lt)
        self.assertEquals(2, dep.version_lte)
        self.assertEquals(3, dep.version_eq)
        self.assertEquals(4, dep.version_gte)
        self.assertEquals(5, dep.version_gt)
        self.assertRaises(TypeError, Dependency, 'foo', unknownattribute=42)

    def test_init_kwargs_string(self):
        pack = Package('foo',
                       name='bar',
                       package_format='1',
                       version='0.0.0',
                       version_abi='pabi',
                       description='pdesc',
                       licenses=['BSD'],
                       maintainers=[self.get_maintainer()])
        self.assertEqual('foo', pack.filename)
        self.assertEqual('bar', pack.name)
        self.assertEqual('1', pack.package_format)
        self.assertEqual('pabi', pack.version_abi)
        self.assertEqual('0.0.0', pack.version)
        self.assertEqual('pdesc', pack.description)

    def test_init_kwargs_object(self):
        mmain = [self.get_maintainer(), self.get_maintainer()]
        mlis = ['MIT', 'BSD']
        mauth = [self.get_maintainer(), self.get_maintainer()]
        murl = [Mock(), Mock()]
        mbuilddep = [Mock(), Mock()]
        mbuildtooldep = [Mock(), Mock()]
        mrundep = [Mock(), Mock()]
        mtestdep = [Mock(), Mock()]
        mconf = [Mock(), Mock()]
        mrepl = [Mock(), Mock()]
        mexp = [Mock(), Mock()]
        pack = Package(name='bar',
                       version='0.0.0',
                       maintainers=mmain,
                       licenses=mlis,
                       urls=murl,
                       authors=mauth,
                       build_depends=mbuilddep,
                       buildtool_depends=mbuildtooldep,
                       run_depends=mrundep,
                       test_depends=mtestdep,
                       conflicts=mconf,
                       replaces=mrepl,
                       exports=mexp)
        self.assertEqual(mmain, pack.maintainers)
        self.assertEqual(mlis, pack.licenses)
        self.assertEqual(murl, pack.urls)
        self.assertEqual(mauth, pack.authors)
        self.assertEqual(mbuilddep, pack.build_depends)
        self.assertEqual(mbuildtooldep, pack.buildtool_depends)
        self.assertEqual(mrundep, pack.run_depends)
        self.assertEqual(mtestdep, pack.test_depends)
        self.assertEqual(mconf, pack.conflicts)
        self.assertEqual(mrepl, pack.replaces)
        self.assertEqual(mexp, pack.exports)

    def test_validate_package(self):
        pack = Package('foo',
                       name='bar_2go',
                       package_format='1',
                       version='0.0.0',
                       version_abi='pabi',
                       description='pdesc',
                       licenses=['BSD'],
                       maintainers=[self.get_maintainer()])
        validate_package(pack)
        # check invalid names
        pack.name = '2bar'
        self.assertRaises(InvalidPackage, validate_package, pack)
        pack.name = 'bar bza'
        self.assertRaises(InvalidPackage, validate_package, pack)
        pack.name = 'bar-bza'
        self.assertRaises(InvalidPackage, validate_package, pack)
        pack.name = 'BAR'
        self.assertRaises(InvalidPackage, validate_package, pack)
        # check authors emails
        pack.name = 'bar'
        auth1 = Mock()
        auth1.email = None
        auth2 = Mock()
        auth2.email = None
        pack.authors = [auth1, auth2]
        validate_package(pack)
        auth1.email = 'foo@bar.com'
        validate_package(pack)
        auth1.email = 'foo[at]bar.com'
        validate_package(pack)
        auth1.email = 'foo bar.com'
        self.assertRaises(InvalidPackage, validate_package, pack)
        auth1.email = 'foo<bar.com'
        self.assertRaises(InvalidPackage, validate_package, pack)
