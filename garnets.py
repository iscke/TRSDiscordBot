
class GarnetHandler:
    def __init__(self):
        pass

    async def handle(self, args, channel):
        return_message = "Please specify what you would like to do: set"
        if len(args) > 0:
            #This command has subcommands, which are listed here
            if args[0] == 'set':
                return_message = await self.command_set(args[1:])

            if args[0] == 'add':
                return_message = await self.command_add(args[1:])

        return return_message

    async def command_set(self, args):
        return "not implemented"
    async def command_add(self, args):
        return "not implemented"
