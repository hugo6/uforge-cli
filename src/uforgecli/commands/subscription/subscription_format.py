__author__ = "UShareSoft"

from texttable import Texttable
from ussclicore.argumentParser import ArgumentParser, ArgumentParserError
from ussclicore.cmd import Cmd, CoreGlobal
from uforgecli.utils import org_utils
from uforgecli.utils.compare_utils import compare
from ussclicore.utils import printer
from ussclicore.utils import generics_utils
from uforgecli.utils.uforgecli_utils import *
from uforge.objects import uforge
from uforgecli.utils import uforgecli_utils
import pyxb
import shlex


class Subscription_Format(Cmd, CoreGlobal):
        """Manage subscription profile formats"""

        cmd_name = "format"

        def __init__(self):
                super(Subscription_Format, self).__init__()

        def arg_add(self):
                doParser = ArgumentParser(prog=self.cmd_name + " add", add_help=True, description="Add formats to a subscription profile")

                mandatory = doParser.add_argument_group("mandatory arguments")
                optional = doParser.add_argument_group("optional arguments")

                mandatory.add_argument('--name', dest='name', required=True, help="the name of the subscription profile")
                mandatory.add_argument('--formats', dest='format', nargs='+', required=True, help="format(s) for which the current command should be executed. You can use Unix matching system (*,?,[seq],[!seq]) and multiple match separating by space.")
                optional.add_argument('--org', dest='org', required=False, help="the organization name. If no organization is provided, then the default organization is used.")
                return doParser

        def do_add(self, args):
                try:
                        # add arguments
                        doParser = self.arg_add()
                        doArgs = doParser.parse_args(shlex.split(args))

                        printer.out("Getting subscription profile with name [" + doArgs.name + "]...")
                        org = org_utils.org_get(self.api, doArgs.org)
                        subscriptions = self.api.Orgs(org.dbId).Subscriptions().Getall(Search=None)
                        formats = self.api.Orgs(org.dbId).Formats.Getall()
                        if formats is None:
                                printer.out("The organisation as no format available.")
                                return 0

                        exist = False
                        for item in subscriptions.subscriptionProfiles.subscriptionProfile:
                                if item.name == doArgs.name:
                                        exist = True
                                        all_formats = imageFormats()
                                        all_formats.imageFormats = pyxb.BIND()

                                        for f in item.formats.format:
                                                already_format = imageFormat()
                                                already_format.access = f.access
                                                already_format.active = f.active
                                                already_format.name = f.name
                                                already_format.preselected = f.preselected
                                                already_format.uri = f.uri

                                                all_formats.imageFormats.append(already_format)

                                        newFormats = compare(formats.imageFormats.imageFormat, doArgs.format, "name")

                                        for nr in newFormats:
                                                new_format = imageFormat()
                                                new_format.access = True
                                                new_format.active = True
                                                new_format.name = nr.name
                                                new_format.preselected = False
                                                new_format.uri = nr.uri
                                                all_formats.imageFormats.append(new_format)
                                                printer.out("Added format " + new_format.name + " for subscription.")

                                        self.api.Orgs(org.dbId).Subscriptions(org.dbId).Formats.Update(all_formats)
                                        printer.out("Some formats added for subscription profile [" + doArgs.name + "]...", printer.OK)
                        if not exist:
                                printer.out("Subscription profile requested don't exist in [" + org.name + "]")
                        return 0

                except ArgumentParserError as e:
                        printer.out("ERROR: In Arguments: " + str(e), printer.ERROR)
                        self.help_add()
                except Exception as e:
                        return handle_uforge_exception(e)

        def help_add(self):
                doParser = self.arg_add()
                doParser.print_help()

        def arg_remove(self):
                doParser = ArgumentParser(prog=self.cmd_name + " remove", add_help=True, description="Remove one or several formats from a subscription profile")

                mandatory = doParser.add_argument_group("mandatory arguments")
                optional = doParser.add_argument_group("optional arguments")

                mandatory.add_argument('--name', dest='name', required=True, help="the name of the subscription profile")
                mandatory.add_argument('--formats', dest='formats', nargs='+', required=True, help="format(s) for which the current command should be executed. You can use Unix matching system (*,?,[seq],[!seq]) and multiple match separating by space.")
                optional.add_argument('--org', dest='org', required=False, help="the organization name. If no organization is provided, then the default organization is used.")
                return doParser

        def do_remove(self, args):
                try:
                        # add arguments
                        doParser = self.arg_remove()
                        doArgs = doParser.parse_args(shlex.split(args))

                        printer.out("Getting subscription profile with name [" + doArgs.name + "]...")
                        org = org_utils.org_get(self.api, doArgs.org)
                        subscriptions = self.api.Orgs(org.dbId).Subscriptions().Getall(Search=None)

                        exist = False
                        for item in subscriptions.subscriptionProfiles.subscriptionProfile:
                                if item.name == doArgs.name:
                                        exist = True
                                        all_formats = imageFormats()
                                        all_formats.imageFormats = pyxb.BIND()

                                        newFormats = compare(item.formats.format, doArgs.formats, "name")

                                        for format in item.formats.format:
                                                for deleteList in newFormats.formats.format:
                                                        if format.name == deleteList.name:
                                                                printer.out("Removed format " + format.name + " for subscription.")
                                                        else:
                                                                already_format = imageFormat()
                                                                already_format.access = format.access
                                                                already_format.active = format.active
                                                                already_format.name = format.name
                                                                already_format.preselected = format.preselected
                                                                already_format.uri = format.uri
                                                                all_formats.imageFormats.append(already_format)

                                        # call UForge API
                                        self.api.Orgs(org.dbId).Subscriptions(org.dbId).Formats.Update(all_formats)
                                        printer.out("Somes roles removed from subscription profile [" + doArgs.name + "]...", printer.OK)

                        if not exist:
                                printer.out("Subscription profile requested don't exist in [" + org.name + "]")
                        return 0

                except ArgumentParserError as e:
                        printer.out("ERROR: In Arguments: " + str(e), printer.ERROR)
                        self.help_remove()
                except Exception as e:
                        return handle_uforge_exception(e)

        def help_remove(self):
                doParser = self.arg_remove()
                doParser.print_help()