import os
import shutil

CONFIG_BASE_PATH = r"E:\azerothcore-build\bin\RelWithDebInfo\configs"


# Declare config settings for each config file here
config_files = {
    "authserver.conf": {
        "Appender.Console": '1,5,1,"1 9 3 6 5 8"',
        "Appender.Auth": "2,5,1,Auth.log,w",
    },
    "worldserver.conf": {
        "DataDir": r".\Data",
        "Appender.Console": '1,4,1,"1 9 3 6 5 8"',
        "Appender.Server": "2,5,1,Server.log,w",
        "Appender.Playerbots": "2,5,1,Playerbots.log,w",
        "Appender.Errors": "2,2,1,Errors.log",
        "GameType": 6,
        "PreventAFKLogout": 2,
        "Warden.Enabled": 0,
        "Visibility.ObjectSparkles": 0,
        "ActivateWeather": 0,
        "EnablePlayerSettings": 1,              # for mod-individual-progression
        "EnableLowLevelRegenBoost": 0,
        "NoResetTalentsCost": 1,
        # "Rate.Rest.InGame": 0,
        # "Rate.Rest.Offline.InTavernOrCity": 0,
        # "Rate.Rest.Offline.InWilderness": 0,
        "Rate.Rest.MaxBonus": 0.75,
        "ToggleXP.Cost": 100,
        # "SkillGain.Crafting": 2,
        # "SkillGain.Defense": 2,
        # "SkillGain.Gathering": 2,
        # "SkillGain.Weapon": 2	,
        # "Rate.Reputation.Gain": 2,
        # "Rate.XP.Kill": 1.1,
        # "Rate.XP.Quest" : 1.3,
        # "Rate.XP.Pet": 1.2,
        # "Rate.Honor": 3,
        # "Rate.ArenaPoints": 3,
        "Death.CorpseReclaimDelay.PvP": 0,
        "Death.CorpseReclaimDelay.PvE": 0,
        # "Rate.Drop.Money": 1.2,
        "Item.SetItemTradeable": 0,
        "Quests.IgnoreAutoAccept": 1,
        "Quests.IgnoreAutoComplete": 1,
        # "Rate.RewardQuestMoney": 1.2,
        "Corpse.Decay.NORMAL": 180,
        "Rate.Corpse.Decay.Looted": 0.01,       # for mod-aoe-loot
        # "LeaveGroupOnLogout.Enabled": 1,
        # "Rate.InstanceResetTime": 0.2,
        "DungeonFinder.CastDeserter": 0,
        "MinPetitionSigns": 0,
        "Guild.BankInitialTabs": 6,
        "Battleground.CastDeserter": 0,
        "MailDeliveryDelay": 5,
        "AllowTwoSide.Interaction.Calendar": 1,
        "AllowTwoSide.Interaction.Chat": 1,
        "AllowTwoSide.Interaction.Channel": 1,
        "AllowTwoSide.Interaction.Group": 1,
        "AllowTwoSide.Interaction.Guild": 1,
        "AllowTwoSide.Interaction.Arena": 1,
        "AllowTwoSide.Interaction.Auction": 1,
    },
    r"modules\AutoBalance.conf": {
        "AutoBalance.Enable.5M": 0,
    },
    # r"modules\mod_account_mount.conf": {
    # },
    r"modules\individualProgression.conf": {
        "IndividualProgression.VanillaPowerAdjustment": 0.6,
        "IndividualProgression.VanillaHealingAdjustment": 0.6,
        "IndividualProgression.TBCPowerAdjustment": 0.6,
        "IndividualProgression.TBCHealingAdjustment": 0.6,
        "IndividualProgression.doableNaxx40Bosses_4H": 1,
        "IndividualProgression.doableNaxx40Bosses_Gluth": 1,
        "IndividualProgression.doableNaxx40Bosses_Patchwerk": 1,
        "IndividualProgression.doableNaxx40Bosses_Razuvious": 1,
        "IndividualProgression.MoltenCore.ManualRuneHandling": 0,
        "IndividualProgression.MoltenCore.AqualEssenceCooldownReduction": 60,
        "IndividualProgression.VanillaHunterPets": 0,
        "IndividualProgression.WarlockDemonTrainers": 0,
        "IndividualProgression.RequiredZulGurubProgression": 0,
        "IndividualProgression.RequiredZulAmanProgression": 9,
    },
    r"modules\mod_ahbot.conf": {
        # WARN set the GUID to 0 and disable the seller until you have created the ahbot character!
        "AuctionHouseBot.GUIDs": "1063",
        "AuctionHouseBot.EnableSeller": "true",
    },
    r"modules\mod_aoe_loot.conf": {
    },
    r"modules\mod_autosort.conf": {
    },
    r"modules\mod-time_is_time.conf": {
        "TimeIsTime.HourOffset": "-2",
    },
    r"modules\playerbots.conf": {
        "AiPlayerbot.RandomBotGuildCount": 0,
        "AiPlayerbot.DeleteRandomBotGuilds": 1,
        "AiPlayerbot.UseGroundMountAtMinLevel": 40,
        "AiPlayerbot.UseFastGroundMountAtMinLevel": 60,
        "AiPlayerbot.UseFlyMountAtMinLevel": 70,
        "AiPlayerbot.RandomBotMinLevel": 10,
        "AiPlayerbot.RandomBotMaxLevel": 60,
        "AiPlayerbot.DisableDeathKnightLogin": 1,
        "AiPlayerbot.RandomBotFixedLevel": 1,
    },
}


# Update config files
has_errors = False
for config_file in config_files:
    filename = CONFIG_BASE_PATH + "\\" + config_file

    # Copy new .dist file to .conf
    if os.path.exists(filename):
        print("Deleting old config file", filename)
        os.remove(filename)
    shutil.copyfile(filename + ".dist", filename)

    with open(filename, "r") as fp:
        data = fp.readlines()

    print("Processing", config_file)
    for k, v in config_files[config_file].items():
        found = False
        for index, line in enumerate(data):
            if not line.startswith("#") and line != "\n" and "=" in line:
                if line.split("=")[0].rstrip() == k:
                    data[index] = f"{k} = {v}\n"
                    print(f"{line[:-1]}\t->\t{k} = {v}")
                    found = True
                    break
        if not found:
            print("ERROR: Could not find config option", k)
            has_errors = True
    print()

    with open(filename, "w") as fp:
        fp.writelines(data)

if has_errors:
    print("\nErrors found, please check the output for more info")
else:
    print("\nDone, no errors found")
