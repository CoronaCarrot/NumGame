import os
import asyncio
import discord
from discord.ext.commands import Bot
import random

bot = Bot(command_prefix="!")


@bot.event
async def on_ready():
    print('Bot is ready as {0.user}'.format(bot))


@bot.command()
async def number(ctx):
    embed = discord.Embed(title="Number Game - 1 - 300",
                          description="I have thought of a number from 1 - 100, try guess it in 9 attempts or less",
                          color=0x0081fa)
    edit = await ctx.send(embed=embed)
    panelID = edit.id
    panelchannel = edit.channel.id

    number = random.randint(1, 100)
    print(number)

    guessed = False
    attempts = 0
    repeat = []
    last = 0

    while not guessed:

        userGuess = 0
        attempts += 1

        playpanel = await bot.get_channel(panelchannel).fetch_message(panelID)

        def auth_check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        try:
            msg = await bot.wait_for("message", check=auth_check, timeout=15)  # 15 seconds to reply
            response = msg.content.lower()

            try:
                await msg.delete()
            except discord.errors.Forbidden:
                pass

            if response.isnumeric():
                last = response
                if int(response) not in range(1, 300):
                    await ctx.send(f"My number is in the range 1-100 its definitely not {response}")
                elif int(response) in repeat:
                    await ctx.send(f"You have already guessed {response}")
                elif int(response) < number:
                    await ctx.send("Guess is too low, guess higher!")
                    repeat.append(number)
                elif int(response) > number:
                    await ctx.send("Guess is too high, guess lower!")
                    repeat.append(number)
                elif int(response) == number:
                    if attempts > 1:
                        plural = "Attempts"
                    else:
                        plural = "Attempt"
            else:
                await ctx.send("Input Must Be Number", delete_after=5)

            panel = discord.Embed(title="Number Game - 1 - 300", description=f"I have thought of a number from 1 - 300, try guess it in 9 attempts or less\n\n\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\n  Attempts: {attempts}\n  Last Guess: {last}\n\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~", color=0x39b5f3)
            await playpanel.edit(embed=panel)

        except asyncio.TimeoutError:
            guessed = True
            embed = discord.Embed(title="You took so long to reply that the game timed out! Better luck next time!",
                                  color=0x0081fa)
            await edit.edit(embed=embed)


#      if counter == 9:
#          print("Out of guesses! Game Over! The number was " + str(number) + "!")
#          Guessed = True
#          continue

#      if userGuess == number:
#          print("CONGRATULATIONS! The number was " + str(number) + "!")
#          Guessed = True
#      elif userGuess > 300:
#          print("Your number is too high...")
#      elif userGuess < 1:
#          print("Your guess is too low...")
#      elif userGuess < number and userGuess < 301 and userGuess > 0:
#          print("Try guessing higher...")
#          counter = counter + 1
#      elif userGuess > number and userGuess < 301 and userGuess > 0:
#          print("Try guessing lower...")
#          counter = counter + 1


bot.run("OTEwMTQ0MzI1NDQ1MzU3NTc4.YZOj9A.xf-ItvZ-A_W3IJnbJg6EZKhfNKo")
