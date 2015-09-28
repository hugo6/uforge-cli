
__author__="UShareSoft"

from ussclicore.argumentParser import ArgumentParser, ArgumentParserError
from ussclicore.cmd import Cmd, CoreGlobal
from texttable import Texttable
from uforgecli.utils.org_utils import org_get
from ussclicore.utils import generics_utils, printer
from uforgecli.utils.uforgecli_utils import *
from uforgecli.utils import org_utils
from uforge.objects import uforge
from uforgecli.utils import *
import shlex
from uforgecli.utils.compare_utils import compare


class User_Format_Cmd(Cmd, CoreGlobal):
        """User format administration"""

        cmd_name = "format"

        def __init__(self):
                super(User_Format_Cmd, self).__init__()

        def arg_list(self):
                doParser = ArgumentParser(add_help = True, description="List all the format from a user.")

                mandatory = doParser.add_argument_group("mandatory arguments")
                optional = doParser.add_argument_group("optional arguments")

                mandatory.add_argument('--account', dest='account', type=str, required=True, help="List image formats (enabled and disabled) for provided user")

                optional.add_argument('--org', dest='org', type=str, required=False, help="List image formats (enabled and disabled) for provided user by a specific organisation.")

                return doParser

        def do_list(self, args):
                try:
                        doParser = self.arg_list()
                        doArgs = doParser.parse_args(shlex.split(args))
                        org = org_utils.org_get(self.api, doArgs.org)

                        printer.out("Getting format list for user \""+doArgs.account+"\" :")
                        if doArgs.org is not None:
                                formatsUser = self.api.Users(doArgs.account).Formats.Getall(org=org.dbId)
                        else:
                                formatsUser = self.api.Users(doArgs.account).Formats.Getall()
                        if formatsUser is None or len(formatsUser.imageFormats.imageFormat) == 0:
                                printer.out("There is no format for the user \""+doArgs.account+"\" in [" + org.name + "].")
                                return 0
                        else:
                                formatsUser = generics_utils.order_list_object_by(formatsUser.imageFormats.imageFormat, "name")
                                printer.out("Format list for user \""+doArgs.account+"\":")
                                table = Texttable(200)
                                table.set_cols_align(["c", "c", "c"])
                                table.header(["Format", "Access", "Active"])
                                for item in formatsUser:
                                        if item.access:
                                                access = "X"
                                        else:
                                                access = ""
                                        if item.active:
                                                active = "X"
                                        else:
                                                active = ""
                                        table.add_row([item.name, access, active])
                                print table.draw() + "\n"
                        return 0

                except ArgumentParserError as e:
                        printer.out("In Arguments: "+str(e), printer.ERROR)
                        self.help_list()
                except Exception as e:
                        return handle_uforge_exception(e)

        def help_list(self):
                doParser = self.arg_list()
                doParser.print_help()

        def arg_enable(self):
                doParser = ArgumentParser(add_help = True, description="Enable image format access for provided user")

                mandatory = doParser.add_argument_group("mandatory arguments")
                optional = doParser.add_argument_group("optional arguments")

                mandatory.add_argument('--account', dest='account', type=str, required=True, help="List image formats (enabled and disabled) for provided user")
                mandatory.add_argument('--formats', dest='formats', nargs='+', type=str, required=True, help="Format list to enable/disable. You can use Unix matching system (*,?,[seq],[!seq]) and multiple match separating by space.")

                optional.add_argument('--org', dest='org', type=str, required=False, help="Organization where the format to enable is. If not entered, default organization selected.")

                return doParser

        def do_enable(self, args):
                try:
                        doParser = self.arg_enable()
                        doArgs = doParser.parse_args(shlex.split(args))
                        org = org_utils.org_get(self.api, doArgs.org)

                        formatsOrg = self.api.Orgs(org.dbId).Formats.Getall()
                        formatsOrg = generics_utils.order_list_object_by(formatsOrg.imageFormats.imageFormat, "name")

                        formatsList = imageFormats()
                        formatsList.imageFormats = pyxb.BIND()

                        formatsOrg = compare(formatsOrg, doArgs.formats, "name")

                        for item in formatsOrg:
                                image = imageFormat()
                                image = item
                                if not item.access:
                                        image.active = True
                                        image.access = True
                                        printer.out("The format ["+item.name+"] has been enabled for ["+doArgs.account+"] in ["+org.name+"].", printer.OK)
                                else:
                                        printer.out("The format ["+item.name+"] is already enabled for ["+doArgs.account+"] in ["+org.name+"].",printer.WARNING)
                                formatsList.imageFormats.append(image)
                                break

                        formats = self.api.Users(doArgs.account).Formats.Update(Org=org.name,body=formatsList)
                        formats=generics_utils.order_list_object_by(formats.imageFormats.imageFormat, "name")

                        table = Texttable(200)
                        table.set_cols_align(["c", "c", "c"])
                        table.header(["Format", "Access", "Active"])

                        for item in formats:
                                if item.access:
                                        access = "X"
                                else:
                                        access = ""
                                if item.active:
                                        active = "X"
                                else:
                                        active = ""
                                table.add_row([item.name, access, active])

                        printer.out("Formats list for user \""+doArgs.account+"\" :")
                        print table.draw() + "\n"
                        return 0

                except ArgumentParserError as e:
                        printer.out("In Arguments: "+str(e), printer.ERROR)
                        self.help_enable()
                except Exception as e:
                        return handle_uforge_exception(e)

        def help_enable(self):
                doParser = self.arg_enable()
                doParser.print_help()

        def arg_disable(self):
                doParser = ArgumentParser(add_help = True, description="Disable format access for provided user")

                mandatory = doParser.add_argument_group("mandatory arguments")
                optional = doParser.add_argument_group("optional arguments")

                mandatory.add_argument('--account', dest='account', type=str, required=True, help="List image formats (enabled and disabled) for provided user")
                mandatory.add_argument('--formats', dest='formats', nargs='+', type=str, required=True, help="Format list to enable/disable. You can use Unix matching system (*,?,[seq],[!seq]) and multiple match separating by space.")

                optional.add_argument('--org', dest='org', type=str, required=False, help="Organization where the format to disable is. If not entered, default organization selected.")

                return doParser

        def do_disable(self, args):
                try:
                        doParser = self.arg_disable()
                        doArgs = doParser.parse_args(shlex.split(args))
                        org = org_utils.org_get(self.api, doArgs.org)

                        formatsOrg = self.api.Orgs(org.dbId).Formats.Getall()
                        formatsOrg = generics_utils.order_list_object_by(formatsOrg.imageFormats.imageFormat, "name")

                        formatsList = imageFormats()
                        formatsList.imageFormats = pyxb.BIND()

                        formatsOrg = compare(formatsOrg, doArgs.formats, "name")

                        for item in formatsOrg:
                                image = imageFormat()
                                image = item
                                if not item.access:
                                        image.access = False
                                        printer.out("The format ["+item.name+"] has been disabled for ["+doArgs.account+"] in ["+org.name+"].", printer.OK)
                                else:
                                        printer.out("The format ["+item.name+"] is already disabled for ["+doArgs.account+"] in ["+org.name+"].", printer.WARNING)
                                formatsList.imageFormats.append(image)
                                break

                        formats = self.api.Users(doArgs.account).Formats.Update(Org=org.name,body=formatsList)
                        formats=generics_utils.order_list_object_by(formats.imageFormats.imageFormat, "name")

                        table = Texttable(200)
                        table.set_cols_align(["c", "c", "c"])
                        table.header(["Format", "Access", "Active"])

                        for item in formats:
                                if item.access:
                                        access = "X"
                                else:
                                        access = ""
                                if item.active:
                                        active = "X"
                                else:
                                        active = ""
                                table.add_row([item.name, access, active])

                        printer.out("Formats list for user \""+doArgs.account+"\" :")
                        print table.draw() + "\n"
                        return 0

                except ArgumentParserError as e:
                        printer.out("In Arguments: "+str(e), printer.ERROR)
                        self.help_disable()
                except Exception as e:
                        return handle_uforge_exception(e)

        def help_disable(self):
                doParser = self.arg_disable()
                doParser.print_help()
