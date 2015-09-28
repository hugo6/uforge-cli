# Didn't find a way to run all the testSuite at once in the main.
# So to run a test enter command : python -m unittest test.<NAME OF THE TEST SUITE>.

import httplib2
import base64
import unittest
import sys
import os

from uforgecli.commands.user.user import User_Cmd
from uforgecli.commands.user.user_format import User_Format_Cmd
from uforgecli.commands.user.user_quota import User_Quota_Cmd
from uforgecli.commands.user.user_admin import User_Admin_Cmd
from uforgecli.commands.user.user_os import User_Os_Cmd
from uforgecli.commands.user.user_role import User_Role_Cmd
from uforgecli.commands.user.user_api import User_Api_Cmd
from uforgecli.commands.user.user_org import User_Org_Cmd
from uforgecli.commands.entitlement.entitlement import Entitlement_Cmd
from uforgecli.commands.subscription.subscription import Subscription_Cmd
from uforgecli.commands.subscription.subscription_admin import Subscription_Admins
from uforgecli.commands.subscription.subscription_role import Subscription_Roles
from uforgecli.commands.subscription.subscription_format import Subscription_Format
from uforgecli.commands.subscription.subscription_os import Subscription_Os
from uforgecli.commands.subscription.subscription_quota import Subscription_Quota
from uforgecli.commands.role.role import Role_Cmd
from uforgecli.commands.role.role_entitlement import Role_Entitlement_Cmd
from uforgecli.commands.images.images import Images_Cmd
from uforgecli.commands.org.org import Org_Cmd
from uforgecli.commands.org.org_user import Org_User_Cmd
from uforgecli.commands.org.org_category import Org_Category_Cmd
from uforgecli.commands.org.org_golden import Org_Golden_Cmd
from uforgecli.commands.org.org_os import Org_Os_Cmd
from uforgecli.commands.org.org_repo import Org_Repo_Cmd
from uforgecli.commands.org.org_repo_os import Org_Repo_Os_Cmd
from uforgecli.commands.org.org_format import Org_Format_Cmd
from uforgecli.commands.os.os import Os_Cmd
from uforgecli.commands.os.os_milestone import Os_Milestone_Cmd
from uforgecli.commands.pimages.pimages import Pimages_Cmd
from uforgecli.commands.usergrp.usergrp import Usergrp_Cmd
from uforgecli.commands.usergrp.usergrp_user import UserGroup_User_Cmd
from uforgecli.commands.template.template import Template_Cmd
from uforge.application import Api

if not "TEST_USER" in os.environ or not "TEST_PASSWORD" in os.environ or not "TEST_URL" in os.environ:
        print "Set env variable [TEST_USER], [TEST_PASSWORD], and [TEST_URL]"
        sys.exit(1)

login = os.environ['TEST_USER']
password = os.environ['TEST_PASSWORD']
url = os.environ['TEST_URL']

userTest = 'root'
userTest2 = 'pedro'
userToCreate = 'Frankenstein'
userToCreatePassword = "Hakunamatata"

userFormatsTest = 'lxc kvm'

subscriptionTest = "test"

userQuotaTypeTest = 'scan'
userQuotaLimitTest = '50'
userRoleTest1 = 'consumer'
userRoleTest2 = 'designer'

userSubscriptionQuotaUpdate = '--name default --type scan --unlimited'

subscriptionAdminTest1 = 'pedro'
subscriptionAdminTest2 = 'root'
subscriptionRoleTest1 = 'consumer'
subscriptionRoleTest2 = 'designer'
subscriptionFormatTest1 = 'esx'
subscriptionFormatTest2 = 'emi-xen'
subscriptionOsTest1 = 'Windows'

roleRoleTest = 'partner'
roleRoleCreateTest = 'mundir'

roleEntitlementCreateTest1 = 'image_generate'
roleEntitlementCreateTest2 = 'marketplace_access'

imagesIdTest = '5'

orgCreate = 'kangourou'
orgNumber = '01'

orgCategoryTest = 'kangouro'
orgCategoryTestCategoryName = 'pedro'

orgGoldenListArgs = '--arch x86_64 --version 5.6 --name CentOS'
orgGoldenCreate = '--arch x86_64 --version 5.6 --name CentOS --edition Standard --goldenDate 2014-04-28 --goldenName Pedro --language English --type Core'

orgOsCreate = '--arch x86_64 --name CentOS --version 2'
orgOsEnableDisable = '--name CentOS'

orgRepoName = '--name pedro'
orgRepoCreate = orgRepoName + ' --repoUrl http://distros-repository.usharesoft.com/pedro --type RPM'
orgRepoUpdate = '--id 1 --repoUrl http://distros-repository.usharesoft.com/pedro2'

orgRepoOsRepoId = '2'
orgRepoOsAttachDetach = '--arch x86_64 --name CentOS --version 5'

osMilestoneVersion = '--darch x86_64 --dname CentOS --dversion 7'
osMilestoneAddNewName = 'SuperVersion'
osMilestoneAddNewDate = '2015-05-11'
osMilestoneModifyNewDate = '2015-08-27'

usergrpTest = 'userGrpTest'
usergrpTestAddAccounts = 'root'

usergrpTestUserAddAfter = 'dimitri'

orgFormatEnableDisable = 'qcow2 ovf09'

class UserTestSuite(unittest.TestSuite):
        def __init__(self):
                unittest.TestSuite.__init__(self,map(TestUser,
                                                     ("test_user_02_format_disable",
                                                      "test_user_03_format_enable",
                                                      "test_user_05_disable",
                                                      "test_user_04_enable",
                                                      "test_user_10_admin_demote",
                                                      "test_user_11_admin_promote",
                                                      "test_user_13_os_disable",
                                                      "test_user_14_os_enable",
                                                      "test_user_16_role_add",
                                                      "test_user_17_role_remove",
                                                      "test_user_20_org_add",
                                                      "test_user_21_org_remove",
                                                      "test_user_01_format_list",
                                                      "test_user_06_quota_list",
                                                      "test_user_07_list",
                                                      "test_user_08_info",
                                                      "test_user_09_quota_modify",
                                                      "test_user_12_os_list",
                                                      "test_user_15_role_list",
                                                      "test_user_18_api_quota",
                                                      "test_user_19_org_list",
                                                      "test_user_22_create")))



class TestMotherClass(unittest.TestCase):
        client = httplib2.Http()
        headers = {}
        headers['Authorization'] = 'Basic ' + base64.encodestring( login + ':' + password)
        global api
        api = Api(url, client=client, headers=headers)

class TestUser(TestMotherClass):

        def test_user_01_format_list(self):
                user_format = User_Format_Cmd()
                user_format.set_globals(api,login,password)
                t = user_format.do_list("--account "+userTest)
                self.assertEquals(t,0)

        def test_user_02_format_disable(self):
                user_format = User_Format_Cmd()
                user_format.set_globals(api,login,password)
                t = user_format.do_disable("--account "+userTest+" --formats "+userFormatsTest)
                self.assertEquals(t,0)

        def test_user_03_format_enable(self):
                user_format = User_Format_Cmd()
                user_format.set_globals(api,login,password)
                t = user_format.do_enable("--account "+userTest+" --formats "+userFormatsTest)
                self.assertEquals(t,0)

        def test_user_04_enable(self):
                user = User_Cmd()
                user.set_globals(api,login,password)
                t = user.do_enable("--account "+userTest2)
                self.assertEquals(t,0)

        def test_user_05_disable(self):
                user = User_Cmd()
                user.set_globals(api,login,password)
                t = user.do_disable("--account "+userTest2)
                self.assertEquals(t,0)

        def test_user_06_quota_list(self):
                user_quota = User_Quota_Cmd()
                user_quota.set_globals(api,login,password)
                t = user_quota.do_list("--account "+userTest2)
                self.assertEquals(t,0)

        def test_user_07_list(self):
                user = User_Cmd()
                user.set_globals(api,login,password)
                t = user.do_list(None)
                self.assertEquals(t,0)

        def test_user_08_info(self):
                user = User_Cmd()
                user.set_globals(api,login,password)
                t = user.do_info("--account "+userTest2)
                self.assertEquals(t,0)

        def test_user_09_quota_modify(self):
                user_quota = User_Quota_Cmd()
                user_quota.set_globals(api,login,password)
                t = user_quota.do_modify("--account "+userTest2+" --type "+userQuotaTypeTest+" --limit "+userQuotaLimitTest)
                self.assertEquals(t,0)

        def test_user_10_admin_demote(self):
                user_admin = User_Admin_Cmd()
                user_admin.set_globals(api,login,password)
                t = user_admin.do_demote("--account "+userTest2)
                self.assertEquals(t,0)

        def test_user_11_admin_promote(self):
                user_admin = User_Admin_Cmd()
                user_admin.set_globals(api,login,password)
                t = user_admin.do_promote("--account "+userTest2)
                self.assertEquals(t,0)

        def test_user_12_os_list(self):
                user_os = User_Os_Cmd()
                user_os.set_globals(api,login,password)
                t = user_os.do_list("--account "+userTest)
                self.assertEquals(t,0)

        def test_user_13_os_disable(self):
                user_os = User_Os_Cmd()
                user_os.set_globals(api,login,password)
                t = user_os.do_disable("--account "+userTest+" --name Cent*")
                self.assertEquals(t,0)

        def test_user_14_os_enable(self):
                user_os = User_Os_Cmd()
                user_os.set_globals(api,login,password)
                t = user_os.do_enable("--account "+userTest+" --name Cent*")
                self.assertEquals(t,0)

        def test_user_15_role_list(self):
                user_role = User_Role_Cmd()
                user_role.set_globals(api,login,password)
                t = user_role.do_list("--account "+userTest)
                self.assertEquals(t,0)

        def test_user_16_role_add(self):
                user_role= User_Role_Cmd()
                user_role.set_globals(api,login,password)
                t = user_role.do_add("--account "+userTest+" --roles "+userRoleTest1+" "+userRoleTest2)
                self.assertEquals(t,0)

        def test_user_17_role_remove(self):
                user_role = User_Role_Cmd()
                user_role.set_globals(api,login,password)
                t = user_role.do_remove("--account "+userTest+" --roles "+userRoleTest1+" "+userRoleTest2)
                self.assertEquals(t,0)

        def test_user_18_api_quota(self):
                user_api = User_Api_Cmd()
                user_api.set_globals(api,login,password)
                t = user_api.do_quota("--account "+userTest2+" --apimax 50")
                self.assertEquals(t,0)

        def test_user_19_org_list(self):
                user_org = User_Org_Cmd()
                user_org.set_globals(api,login,password)
                t = user_org.do_list("--account "+userTest)
                self.assertEquals(t,0)

        def test_user_20_org_add(self):
                user_org = User_Org_Cmd()
                user_org.set_globals(api,login,password)
                t = user_org.do_add("--account "+userTest2+" --admin")
                self.assertEquals(t,0)

        def test_user_21_org_remove(self):
                user_org = User_Org_Cmd()
                user_org.set_globals(api,login,password)
                t = user_org.do_remove("--account "+userTest2+" --admin")
                self.assertEquals(t,0)

        def test_user_22_create(self):
                userList = api.Users.Getall()
                exist = False
                for item in userList.users.user:
                        if item.loginName == userToCreate:
                                exist = True
                if not exist:
                        user = User_Cmd()
                        user.set_globals(api,login,password)
                        t = user.do_create("--account " + userToCreate + " --code default --email " + userToCreate + "@usharesoft.com --accountPassword " + userToCreatePassword)
                        self.assertEquals(t,0)
                else:
                        unittest.skip("User Has already been created.")

class EntitlementTestSuite(unittest.TestSuite):
        def __init__(self):
                unittest.TestSuite.__init__(self,map(TestEntitlement, ("test_entitlement_01_list",)))

class TestEntitlement(TestMotherClass):

        def test_entitlement_01_list(self):
                entitlement = Entitlement_Cmd()
                entitlement.set_globals(api,login,password)
                t = entitlement.do_list("")
                self.assertEquals(t,0)

class SubscriptionTestSuite(unittest.TestSuite):
        def __init__(self):
                unittest.TestSuite.__init__(self,map(TestSubscription,
                                                     ("test_subscription_03_create",
                                                      "test_subscription_01_list",
                                                      "test_subscription_04_update",
                                                      "test_subscription_02_info",
                                                      "test_subscription_06_disable",
                                                      "test_subscription_07_enable",
                                                      "test_subscription_08_admin_add",
                                                      "test_subscription_09_admin_remove",
                                                      "test_subscription_10_role_add",
                                                      "test_subscription_11_role_remove",
                                                      "test_subscription_12_format_add",
                                                      "test_subscription_13_format_remove",
                                                      "test_subscription_14_os_add",
                                                      "test_subscription_15_os_remove",
                                                      "test_subscription_05_delete",
                                                      )))

class TestSubscription(TestMotherClass):

        def test_subscription_01_list(self):
                subscription = Subscription_Cmd()
                subscription.set_globals(api,login,password)
                t = subscription.do_list("")
                self.assertEquals(t,0)

        def test_subscription_02_info(self):
                subscription = Subscription_Cmd()
                subscription.set_globals(api,login,password)
                t = subscription.do_info("--name "+subscriptionTest)
                self.assertEquals(t,0)

        def test_subscription_03_create(self):
                subscription = Subscription_Cmd()
                subscription.set_globals(api,login,password)
                t = subscription.do_create("--name "+subscriptionTest+" --code test")
                self.assertEquals(t,0)

        def test_subscription_04_update(self):
                subscription = Subscription_Cmd()
                subscription.set_globals(api,login,password)
                t = subscription.do_update("--name "+subscriptionTest+" --active")
                self.assertEquals(t,0)

        def test_subscription_05_delete(self):
                subscription = Subscription_Cmd()
                subscription.set_globals(api,login,password)
                t = subscription.do_delete("--name "+subscriptionTest)
                self.assertEquals(t,0)

        def test_subscription_06_disable(self):
                subscription = Subscription_Cmd()
                subscription.set_globals(api,login,password)
                t = subscription.do_disable("--name "+subscriptionTest)
                self.assertEquals(t,0)

        def test_subscription_07_enable(self):
                subscription = Subscription_Cmd()
                subscription.set_globals(api,login,password)
                t = subscription.do_enable("--name "+subscriptionTest)
                self.assertEquals(t,0)

        def test_subscription_08_admin_add(self):
                subscription_admin = Subscription_Admins()
                subscription_admin.set_globals(api,login,password)
                t = subscription_admin.do_add("--name "+subscriptionTest+" --admins "+subscriptionAdminTest1+" "+subscriptionAdminTest2)
                self.assertEquals(t,0)

        def test_subscription_09_admin_remove(self):
                subscription_admin = Subscription_Admins()
                subscription_admin.set_globals(api,login,password)
                t = subscription_admin.do_remove("--name "+subscriptionTest+" --admins "+subscriptionAdminTest1+" "+subscriptionAdminTest2)
                self.assertEquals(t,0)

        def test_subscription_10_role_add(self):
                subscription_role = Subscription_Roles()
                subscription_role.set_globals(api,login,password)
                t = subscription_role.do_add("--name "+subscriptionTest+" --roles "+subscriptionRoleTest1+" "+subscriptionRoleTest2)
                self.assertEquals(t,0)

        def test_subscription_11_role_remove(self):
                subscription_role = Subscription_Roles()
                subscription_role.set_globals(api,login,password)
                t = subscription_role.do_remove("--name "+subscriptionTest+" --roles "+subscriptionRoleTest1+" "+subscriptionRoleTest2)
                self.assertEquals(t,0)

        def test_subscription_12_format_add(self):
                subscription_format = Subscription_Format()
                subscription_format.set_globals(api,login,password)
                t = subscription_format.do_add("--name "+subscriptionTest+" --formats "+subscriptionRoleTest1+" "+subscriptionRoleTest2)
                self.assertEquals(t,0)

        def test_subscription_13_format_remove(self):
                subscription_format = Subscription_Format()
                subscription_format.set_globals(api,login,password)
                t = subscription_format.do_remove("--name "+subscriptionTest+" --formats "+subscriptionFormatTest1+" "+subscriptionFormatTest2)
                self.assertEquals(t,0)

        def test_subscription_14_os_add(self):
                subscription_os = Subscription_Os()
                subscription_os.set_globals(api,login,password)
                t = subscription_os.do_add("--name "+subscriptionTest+" --os "+subscriptionOsTest1)
                self.assertEquals(t,0)

        def test_subscription_15_os_remove(self):
                subscription_os = Subscription_Os()
                subscription_os.set_globals(api,login,password)
                t = subscription_os.do_remove("--name "+subscriptionTest+" --os "+subscriptionOsTest1)
                self.assertEquals(t,0)

        def test_subscription_15_quota_update(self):
                subscription_quota = Subscription_Quota()
                subscription_quota.set_globals(api,login,password)
                t = subscription_quota.do_update(userSubscriptionQuotaUpdate)
                self.assertEquals(t,0)

class RoleTestSuite(unittest.TestSuite):
        def __init__(self):
                unittest.TestSuite.__init__(self,map(TestRole,
                                                     ("test_role_01_list",
                                                      "test_role_02_info",
                                                      "test_role_03_create",
                                                      "test_role_05_entitlement_add",
                                                      "test_role_06_entitlement_remove",
                                                      "test_role_04_delete"
                                                      )))

class TestRole(TestMotherClass):

        def test_role_01_list(self):
                role = Role_Cmd()
                role.set_globals(api,login,password)
                t = role.do_list("")
                self.assertEquals(t,0)

        def test_role_02_info(self):
                role = Role_Cmd()
                role.set_globals(api,login,password)
                t = role.do_info("--name "+roleRoleTest)
                self.assertEquals(t,0)

        def test_role_03_create(self):
                roleList = api.Orgs(orgNumber).Roles.Getall()
                exist = False
                for item in roleList.roles.role:
                        if item.name == roleRoleCreateTest:
                                exist = True
                if exist:
                        unittest.skip("Role has already been created.")
                else:
                        role = Role_Cmd()
                        role.set_globals(api,login,password)
                        t = role.do_create("--name "+roleRoleCreateTest)
                        self.assertEquals(t,0)

        def test_role_05_entitlement_add(self):
                role_entitlement = Role_Entitlement_Cmd()
                role_entitlement.set_globals(api,login,password)
                t = role_entitlement.do_add("--name "+roleRoleCreateTest+" --entitlements "+roleEntitlementCreateTest1+" "+roleEntitlementCreateTest2)
                self.assertEquals(t,0)

        def test_role_06_entitlement_remove(self):
                role_entitlement = Role_Entitlement_Cmd()
                role_entitlement.set_globals(api,login,password)
                t = role_entitlement.do_remove("--name "+roleRoleCreateTest+" --entitlements "+roleEntitlementCreateTest1+" "+roleEntitlementCreateTest2)
                self.assertEquals(t,0)

        def test_role_04_delete(self):
                role = Role_Cmd()
                role.set_globals(api,login,password)
                t = role.do_delete("--name "+roleRoleCreateTest)
                self.assertEquals(t,0)

class ImagesTestSuite(unittest.TestSuite):
        def __init__(self):
                unittest.TestSuite.__init__(self,map(TestImages,
                                                     ("test_images_01_list",
                                                      "test_images_02_info"
                                                      )))

class TestImages(TestMotherClass):

        def test_images_01_list(self):
                images = Images_Cmd()
                images.set_globals(api,login,password)
                t = images.do_list("--account "+userTest)
                self.assertEquals(t,0)

        def test_images_02_info(self):
                images = Images_Cmd()
                images.set_globals(api,login,password)
                t = images.do_info("--account "+userTest+" --id "+imagesIdTest)
                self.assertEquals(t,0)

class OrgTestSuite(unittest.TestSuite):
        def __init__(self):
                unittest.TestSuite.__init__(self,map(TestOrg,
                                                     ("test_org_24_create",
                                                      "test_org_05_category_create",
                                                      "test_org_04_category_list",
                                                      "test_org_06_category_delete",
                                                      "test_org_07_category_reset",
                                                      "test_org_02_info",
                                                      "test_org_01_list",
                                                      "test_org_03_user_list",
                                                      "test_org_09_golden_create",
                                                      "test_org_08_golden_list",
                                                      "test_org_11_os_add",
                                                      "test_org_12_os_disable",
                                                      "test_org_13_os_enable",
                                                      "test_org_10_os_list",
                                                      "test_org_15_repo_create",
                                                      "test_org_16_repo_update",
                                                      "test_org_14_repo_list",
                                                      "test_org_18_repo_os_list",
                                                      "test_org_20_repo_os_detach",
                                                      "test_org_17_repo_delete",
                                                      "test_org_22_format_enable",
                                                      "test_org_21_format_list",
                                                      "test_org_23_format_disable"
                                                      )))

class TestOrg(TestMotherClass):

        def test_org_01_list(self):
                org = Org_Cmd()
                org.set_globals(api,login,password)
                t = org.do_list("")
                self.assertEquals(t,0)

        def test_org_02_info(self):
                org = Org_Cmd()
                org.set_globals(api,login,password)
                t = org.do_info("")
                self.assertEquals(t,0)

        def test_org_03_user_list(self):
                org_user = Org_User_Cmd()
                org_user.set_globals(api,login,password)
                t = org_user.do_list("")
                self.assertEquals(t,0)

        def test_org_04_category_list(self):
                org_category = Org_Category_Cmd()
                org_category.set_globals(api,login,password)
                t = org_category.do_list("")
                self.assertEquals(t,0)

        def test_org_05_category_create(self):
                org_category = Org_Category_Cmd()
                org_category.set_globals(api,login,password)
                t = org_category.do_create("--name " +orgCategoryTestCategoryName + " --org " + orgCreate)
                self.assertEquals(t,0)

        def test_org_06_category_delete(self):
                org_category = Org_Category_Cmd()
                org_category.set_globals(api,login,password)
                t = org_category.do_delete("--name " +orgCategoryTestCategoryName + " --org " + orgCreate)
                self.assertEquals(t,0)

        def test_org_07_category_reset(self):
                org_category = Org_Category_Cmd()
                org_category.set_globals(api,login,password)
                t = org_category.do_reset("--org " + orgCreate)
                self.assertEquals(t,0)

        def test_org_08_golden_list(self):
                org_golden = Org_Golden_Cmd()
                org_golden.set_globals(api,login,password)
                t = org_golden.do_list(orgGoldenListArgs)
                self.assertEquals(t,0)

        def test_org_09_golden_create(self):
                org_golden = Org_Golden_Cmd()
                org_golden.set_globals(api,login,password)
                t = org_golden.do_create(orgGoldenCreate)
                self.assertEquals(t,0)

        def test_org_10_os_list(self):
                org_os = Org_Os_Cmd()
                org_os.set_globals(api,login,password)
                t = org_os.do_list("")
                self.assertEquals(t,0)

        def test_org_11_os_add(self):
                org_os = Org_Os_Cmd()
                org_os.set_globals(api,login,password)
                t = org_os.do_add(orgOsCreate)
                self.assertEquals(t,0)

        def test_org_12_os_disable(self):
                org_os = Org_Os_Cmd()
                org_os.set_globals(api,login,password)
                t = org_os.do_disable(orgOsEnableDisable)
                self.assertEquals(t,0)

        def test_org_13_os_enable(self):
                org_os = Org_Os_Cmd()
                org_os.set_globals(api,login,password)
                t = org_os.do_enable(orgOsEnableDisable)
                self.assertEquals(t,0)

        def test_org_14_repo_list(self):
                org_repo = Org_Repo_Cmd()
                org_repo.set_globals(api,login,password)
                t = org_repo.do_list("")
                self.assertEquals(t,0)

        def test_org_15_repo_create(self):
                org_repo = Org_Repo_Cmd()
                org_repo.set_globals(api,login,password)
                t = org_repo.do_create(orgRepoCreate)
                self.assertEquals(t,0)

        def test_org_16_repo_update(self):
                org_repo = Org_Repo_Cmd()
                org_repo.set_globals(api,login,password)
                t = org_repo.do_update(orgRepoUpdate)
                self.assertEquals(t,0)

        def test_org_17_repo_delete(self):

                all_repos = api.Orgs(orgNumber).Repositories.Getall()
                exist = False
                for item in all_repos.repositories.repository:
                        if item.name == orgRepoName:
                                exist = True
                                orgRepoDeleteId = item.dbId
                                org_repo = Org_Repo_Cmd()
                                org_repo.set_globals(api,login,password)
                                t = org_repo.do_delete("--ids " + orgRepoDeleteId)
                                self.assertEquals(t,0)
                if not exist:
                        unittest.SkipTest("Repo ID not found, maybe a problem at repo creation.")

        def test_org_18_repo_os_list(self):
                org_repo_os = Org_Repo_Os_Cmd()
                org_repo_os.set_globals(api,login,password)
                t = org_repo_os.do_list("--repoId " + orgRepoOsRepoId)
                self.assertEquals(t,0)

        def test_org_19_repo_os_attach(self):
                org_repo_os = Org_Repo_Os_Cmd()
                org_repo_os.set_globals(api,login,password)
                t = org_repo_os.do_attach("--repoIds " + orgRepoOsRepoId + " " + orgRepoOsAttachDetach)
                self.assertEquals(t,0)

        def test_org_20_repo_os_detach(self):
                org_repo_os = Org_Repo_Os_Cmd()
                org_repo_os.set_globals(api,login,password)
                t = org_repo_os.do_detach("--repoIds " + orgRepoOsRepoId + " " + orgRepoOsAttachDetach)
                self.assertEquals(t,0)

        def test_org_21_format_list(self):
                org_format = Org_Format_Cmd()
                org_format.set_globals(api,login,password)
                t = org_format.do_list("")
                self.assertEquals(t,0)

        def test_org_22_format_enable(self):
                org_format = Org_Format_Cmd()
                org_format.set_globals(api,login,password)
                t = org_format.do_enable("--format " + orgFormatEnableDisable)
                self.assertEquals(t,0)

        def test_org_23_format_disable(self):
                org_format = Org_Format_Cmd()
                org_format.set_globals(api,login,password)
                t = org_format.do_disable("--format " + orgFormatEnableDisable)
                self.assertEquals(t,0)

        def test_org_24_create(self):
                orgs = api.Orgs(orgNumber).Getall()
                exist = False
                for item in orgs.orgs.org:
                        if item.name == orgCreate:
                                exist = True
                if exist:
                        unittest.skip("Organization already created.")
                else:
                        org = Org_Cmd()
                        org.set_globals(api,login,password)
                        t = org.do_create("--org " + orgCreate)
                        self.assertEquals(t,0)

class OsTestSuite(unittest.TestSuite):
        def __init__(self):
                unittest.TestSuite.__init__(self,map(TestOs,
                                                     ("test_os_01_list",
                                                      "test_os_02_milestone_add",
                                                      "test_os_03_milestone_list",
                                                      "test_os_04_milestone_modify",
                                                      "test_os_05_milestone_remove"
                                                      )))

class TestOs(TestMotherClass):

        def test_os_01_list(self):
                org = Os_Cmd()
                org.set_globals(api,login,password)
                t = org.do_list("")
                self.assertEquals(t,0)

        def test_os_02_milestone_add(self):
                os_milestone = Os_Milestone_Cmd()
                os_milestone.set_globals(api,login,password)
                t = os_milestone.do_add(osMilestoneVersion + " --date " + osMilestoneAddNewDate + " --name " + osMilestoneAddNewName)
                self.assertEquals(t,0)

        def test_os_03_milestone_list(self):
                os_milestone = Os_Milestone_Cmd()
                os_milestone.set_globals(api,login,password)
                t = os_milestone.do_list(osMilestoneVersion)
                self.assertEquals(t,0)

        def test_os_04_milestone_modify(self):
                os_milestone = Os_Milestone_Cmd()
                os_milestone.set_globals(api,login,password)
                t = os_milestone.do_modify(osMilestoneVersion + " --date " + osMilestoneModifyNewDate + " --name " + osMilestoneAddNewName)
                self.assertEquals(t,0)

        def test_os_05_milestone_remove(self):
                os_milestone = Os_Milestone_Cmd()
                os_milestone.set_globals(api,login,password)
                t = os_milestone.do_remove(osMilestoneVersion + " --name " + osMilestoneAddNewDate)
                self.assertEquals(t,0)

class PimagesTestSuite(unittest.TestSuite):
        def __init__(self):
                unittest.TestSuite.__init__(self,map(TestPimages,
                                                     ("test_pimages_01_list",
                                                      "test_pimages_02_info"
                                                      )))

class TestPimages(TestMotherClass):

        def test_pimages_01_list(self):
                pimages = Pimages_Cmd()
                pimages.set_globals(api,login,password)
                t = pimages.do_list("--account " + userTest)
                self.assertEquals(t,0)

        def test_pimages_02_info(self):
                pimages = Pimages_Cmd()
                pimages.set_globals(api,login,password)
                t = pimages.do_info("--account " + userTest + " --id 3")
                self.assertEquals(t,0)

class UserGroupTestSuite(unittest.TestSuite):
        def __init__(self):
                unittest.TestSuite.__init__(self,map(TestUserGroup,
                                                     ("test_usergrp_01_create",
                                                      "test_usergrp_02_list",
                                                      "test_usergrp_05_user_add",
                                                      "test_usergrp_03_info",
                                                      "test_usergrp_06_user_remove",
                                                      "test_usergrp_04_delete"
                                                      )))

class TestUserGroup(TestMotherClass):

        def test_usergrp_01_create(self):
                usergrp = Usergrp_Cmd()
                usergrp.set_globals(api,login,password)
                t = usergrp.do_create("--name " + usergrpTest + " --email " + usergrpTest + "@usharesoft.com --usergrpPassword " + usergrpTest + " --accounts " + usergrpTestAddAccounts)
                self.assertEquals(t,0)

        def test_usergrp_02_list(self):
                usergrp = Usergrp_Cmd()
                usergrp.set_globals(api,login,password)
                t = usergrp.do_list("")
                self.assertEquals(t,0)

        def test_usergrp_03_info(self):
                usergrp = Usergrp_Cmd()
                usergrp.set_globals(api,login,password)
                t = usergrp.do_info("--name " + usergrpTest)
                self.assertEquals(t,0)

        def test_usergrp_04_delete(self):
                usergrp = Usergrp_Cmd()
                usergrp.set_globals(api,login,password)
                t = usergrp.do_delete("--name " + usergrpTest)
                self.assertEquals(t,0)

        def test_usergrp_05_user_add(self):
                usergrp_user = UserGroup_User_Cmd()
                usergrp_user.set_globals(api,login,password)
                t = usergrp_user.do_add("--name " + usergrpTest + " --accounts " + usergrpTestUserAddAfter)
                self.assertEquals(t,0)

        def test_usergrp_06_user_remove(self):
                usergrp_user = UserGroup_User_Cmd()
                usergrp_user.set_globals(api,login,password)
                t = usergrp_user.do_add("--name " + usergrpTest + " --accounts " + usergrpTestUserAddAfter)
                self.assertEquals(t,0)

class TemplateTestSuite(unittest.TestSuite):
        def __init__(self):
                unittest.TestSuite.__init__(self,map(TestTemplate,
                                                     ("test_template_01_list",
                                                      "test_template_02_info",
                                                      "test_template_03_images",
                                                      "test_template_04_pimages"
                                                      )))

class TestTemplate(TestMotherClass):

        def test_template_01_list(self):
                template = Template_Cmd()
                template.set_globals(api,login,password)
                t = template.do_list("--account root")
                self.assertEquals(t,0)

        def test_template_02_info(self):
                templateList = api.Users(userTest).Appliances.Getall()
                templateList = templateList.appliances.appliance
                if len(templateList) == 0:
                        unittest.skip("No Template list for userTest.")
                else:
                        templateID = str(templateList[0].dbId)
                        template = Template_Cmd()
                        template.set_globals(api,login,password)
                        t = template.do_info("--account " + userTest + " --id " + templateID + "")
                        self.assertEquals(t,0)

        def test_template_03_images(self):
                templateList = api.Users(userTest).Appliances.Getall()
                templateList = templateList.appliances.appliance
                if len(templateList) == 0:
                        unittest.skip("No Template list for userTest.")
                else:
                        templateID = str(templateList[0].dbId)
                        template = Template_Cmd()
                        template.set_globals(api,login,password)
                        t = template.do_images("--account " + userTest + " --id " + templateID)
                        self.assertEquals(t,0)

        def test_template_04_pimages(self):
                templateList = api.Users(userTest).Appliances.Getall()
                templateList = templateList.appliances.appliance
                if len(templateList) == 0:
                        unittest.skip("No Template list for userTest.")
                else:
                        templateID = str(templateList[0].dbId)
                        template = Template_Cmd()
                        template.set_globals(api,login,password)
                        t = template.do_pimages("--account " + userTest + " --id " + templateID)
                        self.assertEquals(t,0)

if __name__ == '__main__':
        v = sys.version_info

        import xmlrunner
        runner = unittest.TextTestRunner()
        userTestSuite = UserTestSuite()
        subscriptionTestSuite = SubscriptionTestSuite()
        osTestSuite = OsTestSuite()
        userGroupTestSuite = UserGroupTestSuite()
        templateTestSuite = TemplateTestSuite()
        pimagesTestSuite = PimagesTestSuite()
        entitlementTestSuite = EntitlementTestSuite()
        imagesTestSuite = ImagesTestSuite()
        runner.run = unittest.TestSuite([userTestSuite,
                                         subscriptionTestSuite,
                                         osTestSuite,
                                         userGroupTestSuite,
                                         templateTestSuite,
                                         pimagesTestSuite,
                                         entitlementTestSuite,
                                         imagesTestSuite])


# if v >= (2,7):
#         import xmlrunner
#         unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'))
# else:
#         unittest.main()
