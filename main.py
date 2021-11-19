import os
import asyncio
import discord
from discord.ext.commands import Bot
import random

bot = Bot(command_prefix="¬")

playing = []


@bot.event
async def on_ready():
    print('Bot is ready as {0.user}'.format(bot))


@bot.command()
async def number(ctx, min, max):
    global playing
    if ctx.message.author.id in playing:
        return

    if type(min) == str or type(max) == str:
        embed = discord.Embed(title=f"Number Game - Error",
                              description=f"Error Message: `Min And Max Must Be Integers` \n**Usage** `{bot.command_prefix}number <min> <max>`",
                              color=0xf87272)
        await ctx.send(embed=embed)
    else:
        if int(min) < 0:
            embed = discord.Embed(title=f"Number Game - Error",
                                  description=f"Error Message: `The minimum is 0` \n**Usage** `{bot.command_prefix}number <min> <max>`",
                                  color=0xf87272)
            await ctx.send(embed=embed)
        elif int(max) > 1000000:
            embed = discord.Embed(title=f"Number Game - Error",
                                  description=f"Error Message: `The maximum is 1,000,000` \n**Usage** `{bot.command_prefix}number <min> <max>`",
                                  color=0xf87272)
            await ctx.send(embed=embed)
        elif str(min)[0] == "-":
            min = int(min) - int(int(min) * 2)
        elif str(max)[0] == "-":
            max = int(max) - int(int(max) * 2)
        else:

            if max < min or min > max:
                t = str(min)
                min = str(max)
                max = str(t)
            embed = discord.Embed(title=f"Number Game - {int(min)} - {int(max)}",
                                  description=f"I have thought of a number from {int(min)} - {int(max)}, try guess it in 9 attempts or less",
                                  color=0x0081fa)
            edit = await ctx.send(embed=embed)
            panelid = edit.id
            panelchannel = edit.channel.id

            number = random.randint(int(min), int(max))
            print(f"Executing number game for {ctx.message.author.name} with number " + str(number))
            playing.insert(0, ctx.message.author.id)
            print(playing)

            guessed = False
            attempts = 0
            repeat = []
            last = 0

            while not guessed:

                playpanel = await bot.get_channel(panelchannel).fetch_message(panelid)

                def auth_check(msg):
                    return msg.author == ctx.author and msg.channel == ctx.channel

                try:
                    msg = await bot.wait_for("message", check=auth_check, timeout=15)  # 15 seconds to reply
                    response = msg.content.lower()

                    try:
                        await msg.delete()
                    except discord.errors.Forbidden:
                        pass

                    last = response

                    if response.isnumeric():
                        attempts += 1
                        if int(response) not in range(int(min), int(int(max)) + 1):
                            clue = f"My number is in the range {min}-{max} its definitely not {response}"
                        elif int(response) in repeat:
                            clue = f"You have already guessed {response}"
                        elif int(response) < number:
                            clue = "Guess is too low, guess higher!"
                            repeat.append(int(response))
                        elif int(response) > number:
                            clue = "Guess is too high, guess lower!"
                            repeat.append(int(response))
                        elif int(response) == number:
                            if attempts > 1:
                                plural = "Attempts"
                            else:
                                plural = "Attempt"

                            clue = f"CONGRATULATIONS you guessed the number!\nthe number was {number}, you got it in {attempts} {plural}"
                            guessed = True
                            playing.remove(ctx.message.author.id)
                    else:
                        if str(response)[0] == "-":
                            clue = "Negative numbers aren't allowed"
                        else:
                            if str(response)[0] == f"{bot.command_prefix}":
                                clue = "The Answer Is Not A Command Lol (Not Counting As Attempt)"
                            else:
                                clue = f"Input Must Be Number (Not Counting As Attempt)"

                    panel = discord.Embed(title=f"Number Game - {int(min)} - {int(max)}",
                                          description=f"I have thought of a number from {int(min)} - {int(max)}, try guess it in 9 attempts or less\n\n\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\n  Attempts: `{attempts}`\n  Last Guess: `{last}`\n\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\n\n{clue}",
                                          color=0x39b5f3)
                    await playpanel.edit(embed=panel)

                except asyncio.TimeoutError:
                    guessed = True
                    embed = discord.Embed(
                        title="You took so long to reply that the game timed out! Better luck next time!",
                        color=0x0081fa)
                    await edit.edit(embed=embed)
                    playing.remove(ctx.message.author.id)


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


bot.run("OTExMzU2NTc3NTQ0NTQwMTgw.YZgM9A.A2LW7XmxHM8ED3mR-3tTOLMSDLI")
