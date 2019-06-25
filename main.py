import discord, asyncio, json, random
import utils

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
                    await self.send_message(channel, return_message)

                if key in ['dice','roll']:
                    return_message = await self.command_dice(args, channel)
                    await self.send_message(channel, return_message)


    #Bot Functions (Not Commands)
    #Sets a timer and returns a message to the destination provided when it is finished.
    async def set_timer(self, time, destination):
        await asyncio.sleep(time)
        await self.send_message(destination, "The timer has expired!")

    def roll_dice(self, dice, faces):
        if dice > 0 and faces > 0:
            result = [random.randint(1, faces) for i in range(dice)]
            string_result = [str(i) for i in result]
            return f"{', '.join(string_result)} | Sum: {sum(result)}"
        else:
            return "The number of faces and dice must be over zero."

    #Bot Commands
    async def command_timer(self, args, channel):
        return_message = "Please provide an argument for how long the timer should run for in seconds, e.g. ``timer 60``."
        if len(args) >= 1:
            if args[0].isdigit():
                time = int(args[0])
                self.loop.create_task(self.set_timer(time, channel))
                return_message = f"Set a timer for {time} seconds."
        return return_message

    async def command_dice(self, args, channel):
        return_message = "Please provide arguments for how many faces and how many dice to roll (default 6, 1), e.g. ``roll 6, 2``"
        dice = 1
        faces = 6
        if len(args) >= 2:
            if args[0].isdigit() and args[1].isdigit():
                dice, faces = int(args[0]), int(args[1])
                return_message = self.roll_dice(dice, faces)
        elif len(args) >= 1:
            if args[0].isdigit():
                faces = int(args[0])
                return_message = self.roll_dice(dice, faces)
        else:
            return_message = self.roll_dice(dice, faces)
        return return_message

            

#set up bot
if __name__ == "__main__":
    with open("config.json") as f:
        config = json.load(f)
    bot = DiscordBot(config['prefix'], config['description'])                   
    bot.run(config['bot_token'])

    



