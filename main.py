import logging
import os
import pickle
import threading
import argparse

import ConfigParser
from Discordia.GameLogic import GameSpace
from Discordia.Interface.DiscordInterface import DiscordInterface
from Discordia.Interface.Rendering.DesktopApp import WindowRenderer, update_display
from Discordia.Interface.WorldAdapter import WorldAdapter

LOG = logging.getLogger("Discordia")
logging.basicConfig(level=logging.INFO)


def main():
    parser = argparse.ArgumentParser(description="Run an instance of a Discordia server",
                                     prog="Discordia")
    parser.add_argument('-W --show_window', dest='show_window', action='store_const', const=True, default=False,
                        help="Show a window containing a live view of the entire world. WARNING: CPU-intensive.")
    args = parser.parse_args()

    # Read in world file if found
    if os.path.isfile(r'./world.p'):
        world: GameSpace.World = pickle.load(open(r'./world.p', 'rb'))
    else:
        world = GameSpace.World(ConfigParser.WORLD_NAME, ConfigParser.WORLD_WIDTH, ConfigParser.WORLD_HEIGHT)

    adapter = WorldAdapter(world)

    display = WindowRenderer(adapter)

    threading.Thread(target=update_display, args=(display, args.show_window), daemon=True).start()
    discord_interface = DiscordInterface(adapter)
    # discord_interface.bot.loop.create_task(update_display(display))
    # threading.Thread(target=discord_interface.bot.run, args=(ConfigParser.DISCORD_TOKEN,), daemon=True).start()
    LOG.info("Discordia Server has successfully started. Press Ctrl+C to quit.")
    discord_interface.bot.run(ConfigParser.DISCORD_TOKEN)


if __name__ == '__main__':
    main()
