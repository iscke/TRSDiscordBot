import discord, asyncio, json, random
import garnets, deck, utils

#Primary Bot class that handles messages received from Discord and processes them
class DiscordBot(discord.Client):
    def __init__(self, prefix, description):
        super().__init__()

        #prefix is the character placed before commands by users
        self.prefix = prefix
        self.description = description

        #register events
        self.event(self.on_ready)
        self.event(self.on_message)

        #load external handlers
        self.deckhandler = deck.DeckHandler()
        self.garnethandler = garnets.GarnetHandler()

    async def on_ready(self):
        print("Ready!")

    async def on_message(self, message):
        if message.content.startswith(self.prefix):
            #the bot cannot activate itself
            if message.author.id != self.user.id:
                #Beware! The channel can be private messages (channel.is_private)
                channel = message.channel
                command = utils.argParse(message.content[1:])
                key = command[0]
                args = command[1:]

                if key == 'timer':
                    return_message = await self.command_timer(args, channel)
                    await self.reply(channel, return_message)

                elif key in ['dice','roll']:
                    return_message = await self.command_dice(args)
                    await self.reply(channel, return_message)

                elif key in ['garnet','garnets','currency','points','point']:
                    return_message = await self.command_garnets(args)
                    await self.reply(channel, return_message)

                elif key in ['deck','decks','cards','card']:
                    return_message = await self.command_deck(args)
                    await self.reply(channel, return_message)

    #Bot Functions (Not Commands)
    #Sets a timer and returns a message to the destination provided when it is finished.
    async def set_timer(self, time, destination):
        await asyncio.sleep(time)
        await destination.send("The timer has expired!")

    #function that makes return messages cleaner by sending multiple messages if message is a list
    async def reply(self, destination, message):
        if type(message) == list:
            for i in message:
                await destination.send(i)
        elif type(message) == str:
                await destination.send(message)

    def find_user(self, name, server=None):
        #This works if <name> is a User ID, otherwise None
        user = self.get_user(name)
        #if it didnt work by ID and a server was provided in kwargs:
        if (not user) and server:
            user = server.get_member_named(name)
        #either a User OR MEMBER object or None
        return user

    def roll_dice(self, dice, faces):
        if dice > 0 and faces > 0:
            result = [random.randint(1, faces) for i in range(dice)]
            string_result = [str(i) for i in result]
            if len(result) > 1:
                return f"{', '.join(string_result)} | Sum: {sum(result)}"
            else:
                return f"{string_result[0]}"
        else:
            return "The number of faces and dice must be over zero."

    #Bot Commands
    async def command_timer(self, args, channel):
        if not len(args) or not args[0].isdigit:
            return "Please provide an argument for how long the timer should run for in seconds, e.g. ``timer 60``."
        time = int(args[0])
        self.loop.create_task(self.set_timer(time, channel))
        return f"Set a timer for {time} seconds."

    async def command_dice(self, args):
        if not len(args) or not all(arg.isdigit() for arg in args):
            return "Please provide arguments for how many faces and how many dice to roll (default 6, 1), e.g. ``roll 6, 2``"
        dice = 1
        faces = 6
        if len(args) >= 2:
                faces, dice = int(args[0]), int(args[1])
        elif len(args) >= 1:
                faces = int(args[0])
        return self.roll_dice(dice, faces)

    async def command_garnets(self, args):   
        return_message = await self.garnethandler.handle(args)
        return return_message

    async def command_deck(self, args):
        return_message = await self.deckhandler.handle(args)
        return return_message      

#set up bot
if __name__ == "__main__":
    with open("config.json") as f:
        config = json.load(f)
    bot = DiscordBot(config['prefix'], config['description'])                   
    bot.run(config['bot_token'])
