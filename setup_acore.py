import os
import shutil

CONFIG_BASE_PATH = r"E:\azerothcore-build\bin\RelWithDebInfo\configs"
ACORE_BASE_PATH = r"E:\azerothcore-wotlk"
ACORE_CUSTOM_SQL_PATH = ACORE_BASE_PATH + r"\data\sql\custom\db_world"
CUSTOM_SQL_BASE_PATH = r"F:\Azerothcore\Custom-SQL"

config_files = {
    "authserver.conf": {
        "Appender.Console": '1,5,1,"1 9 3 6 5 8"',
        "Appender.Auth": "2,5,1,Auth.log,w",
    },
    "worldserver.conf": {
        "DataDir": r"E:\azerothcore-build\bin\RelWithDebInfo\Data",
        "Appender.Console": '1,4,1,"1 9 3 6 5 8"',
        "Appender.Server": "2,5,1,Server.log,w",
        "Appender.Playerbots": "2,5,1,Playerbots.log,w",
        "Appender.Errors": "2,2,1,Errors.log",
        "Warden.Enabled": 0,
        "InstantLogout": 0,
        "EnableLowLevelRegenBoost": 0,
        "NoResetTalentsCost": 1,
        "Rate.Rest.InGame": 0,
        "Rate.Rest.Offline.InTavernOrCity": 0,
        "Rate.Rest.Offline.InWilderness": 0,
        "Rate.Rest.MaxBonus": 0,
        "ToggleXP.Cost": 100,
        "SkillGain.Crafting": 2,
        "SkillGain.Defense": 2,
        "SkillGain.Gathering": 2,
        "SkillGain.Weapon": 2	,
        "Rate.Reputation.Gain": 2,
        "Rate.XP.Kill": 1.1,
        "Rate.XP.Quest": 1.1,
        "Rate.XP.Pet": 1.1,
        "Rate.Honor": 3,
        "Rate.ArenaPoints": 3,
        "Death.CorpseReclaimDelay.PvP": 0,
        "Death.CorpseReclaimDelay.PvE": 0,
        "Rate.Drop.Money": 1.3,
        "Item.SetItemTradeable": 0,
        "Quests.IgnoreAutoAccept": 1,
        "Quests.IgnoreAutoComplete": 1,
        "Rate.RewardQuestMoney": 1.3,
        "Corpse.Decay.NORMAL": 180,
        "LeaveGroupOnLogout.Enabled": 1,
        "Rate.InstanceResetTime": 0.2,
        "DungeonFinder.CastDeserter": 0,
        "MinPetitionSigns": 0,
        "Guild.BankInitialTabs": 6,
        "Battleground.CastDeserter": 0,
        "MailDeliveryDelay": 5,
        "AllowTwoSide.Interaction.Calendar": 1,
        "AllowTwoSide.Interaction.Chat": 1,
        "AllowTwoSide.Interaction.Emote": 1,
        "AllowTwoSide.Interaction.Channel": 1,
        "AllowTwoSide.Interaction.Group": 1,
        "AllowTwoSide.Interaction.Guild": 1,
        "AllowTwoSide.Interaction.Arena": 1,
        "AllowTwoSide.Interaction.Auction": 1,
        "AllowTwoSide.Interaction.Mail": 1,
        "AllowTwoSide.WhoList": 1,
        "AllowTwoSide.AddFriend": 1,
        "AllowTwoSide.Trade": 1,
    },
    r"modules\AutoBalance.conf": {
        "AutoBalance.Enable.5M": 0,
    },
    # r"modules\individualProgression.conf": {
    #     "IndividualProgression.EnforceGroupRules": 0,
    #     "IndividualProgression.QuestXPFix": 0,
    #     "IndividualProgression.MoltenCore.ManualRuneHandling": 0,
    #     "IndividualProgression.MoltenCore.AqualEssenceCooldownReduction": 60,
    #     "IndividualProgression.SimpleConfigOverride": 0,
    # },
    r"modules\mod_account_mount.conf": {
    },
    r"modules\mod-time_is_time.conf": {
        "TimeIsTime.HourOffset": "-4",
    },
    r"modules\playerbots.conf": {
        "AiPlayerbot.RandomBotGuildCount": 0,
        "AiPlayerbot.DeleteRandomBotGuilds": 1,
        "AiPlayerbot.UseGroundMountAtMinLevel": 30,
        "AiPlayerbot.UseFastGroundMountAtMinLevel": 50,
        "AiPlayerbot.UseFlyMountAtMinLevel": 65,
        "AiPlayerbot.LootRollLevel": 0,
        "AiPlayerbot.RandomBotMinLevel": 10,
        "AiPlayerbot.RandomBotMaxLevel": 60,
        "AiPlayerbot.DisableDeathKnightLogin": 1,
        "AiPlayerbot.RandomBotFixedLevel": 1,
    },
}


# Copy custom SQL files
# for _, _, files in os.walk(CUSTOM_SQL_BASE_PATH):
#     for file in files:
#         shutil.copyfile(CUSTOM_SQL_BASE_PATH + "\\" + file, ACORE_CUSTOM_SQL_PATH)


# Update config files
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
            print("Could not find config option", k)
    print()

    with open(filename, "w") as fp:
        fp.writelines(data)

print("\nDone")
