import os
from asyncio import sleep
from datetime import datetime
from os import remove
from telethon import events, functions, types
from telethon.errors import (
    BadRequestError,
    ChatAdminRequiredError,
    ImageProcessFailedError,
    PhotoCropSizeSmallError,
)
from requests import get
from telethon.tl.functions.photos import GetUserPhotosRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.utils import get_input_location

from astro import LOGS, TEMP_DOWNLOAD_DIRECTORY

from telethon.errors.rpcerrorlist import MessageTooLongError
from telethon.tl.functions.channels import (
    EditAdminRequest,
    EditBannedRequest,
    EditPhotoRequest,
)
from telethon.tl.functions.messages import UpdatePinnedMessageRequest
from telethon.tl.types import (
    ChannelParticipantsAdmins,
    ChatAdminRights,
    ChatBannedRights,
    MessageEntityMentionName,
    MessageMediaPhoto,
)
from alphax.plugins.sql.locks_sql import get_locks, is_locked, update_lock
from alphax.plugins.sql.mute_sql import is_muted, mute, unmute
from astro.config import Config 
BOT_NAME = Config.BOT_NAME
MANAGER = Config.MANAGER

# notes #
PP_TOO_SMOL = "`The image is too small`"
PP_ERROR = "`Failure while processing the image`"
NO_ADMIN = "I am not an admin here!😂"
NO_PERM = "`No sufficient permissions!`"
NO_SQL = "`Running on Non-SQL mode!`"

CHAT_PP_CHANGED = "`Chat Picture Changed`"
CHAT_PP_ERROR = (
    "`Some issue with updating the pic,`"
    "`maybe coz I'm not an admin,`"
    "`or don't have enough rights.`"
)
INVALID_MEDIA = "`Invalid Extension`"

BANNED_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)

UNBAN_RIGHTS = ChatBannedRights(
    until_date=None,
    send_messages=None,
    send_media=None,
    send_stickers=None,
    send_gifs=None,
    send_games=None,
    send_inline=None,
    embed_links=None,
)

LOCKS = """
LockTypes:
➟ bots
➟ email
➟ commands
➟ forward
➟ url
➟ msg
➟ media
➟ sticker
➟ gif
➟ gamee
➟ ainline
➟ gpoll
➟ adduser
➟ cpin
➟ changeinfo
Use `/lock <locktypes>` to lock it.
"""

MUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=True)

UNMUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=False)

@tgbot.on(events.NewMessage(pattern="/setgpic"))
async def setgpic(gpic): 
  if MANAGER == "ON":
    if not gpic.is_group:
        await gpic.reply(event, "`I don't think this is a group.`")
        return
    replymsg = await gpic.get_reply_message()
    chat = await gpic.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    photo = None

    if not admin and not creator:
        x = await gpic.reply(NO_ADMIN)
        return

    if replymsg and replymsg.media:
        if isinstance(replymsg.media, MessageMediaPhoto):
            photo = await gpic.client.download_media(message=replymsg.photo)
        elif "image" in replymsg.media.document.mime_type.split("/"):
            photo = await gpic.client.download_file(replymsg.media.document)
        else:
            x = await gpic.reply(INVALID_MEDIA)

    if photo:
        try:
            await gpic.client(
                EditPhotoRequest(gpic.chat_id, await gpic.client.upload_file(photo))
            )
            x = await gpic.reply(CHAT_PP_CHANGED)

        except PhotoCropSizeSmallError:
            x = await gpic.reply(PP_TOO_SMOL)
        except ImageProcessFailedError:
            x = await gpic.reply(PP_ERROR)
            
  else: 
    await tgbot.send_message(gpic.chat_id, "**MASTER!!** __please enable MANAGER SERVICE__ by using `.set Config MANAGER ON`")
@tgbot.on(events.NewMessage(pattern="/promote ?(.*)"))
async def promote(promt):
  if MANAGER == "ON":
    chat = await promt.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        await promt.reply(NO_ADMIN)
        return
    new_rights = ChatAdminRights(
        add_admins=False,
        invite_users=True,
        change_info=False,
        ban_users=True,
        delete_messages=True,
        pin_messages=True,
    )
    await promt.reply("`Promoting...`")
    user, rank = await get_user_from_event(promt)
    if not rank:
        rank = "ADMEEN"  # just in case
    if not user:
        return
    try:
        await promt.client(EditAdminRequest(promt.chat_id, user.id, new_rights, rank))
        await promt.reply(f"Promoted Successfully! Enjoy!!\nby {BOT_NAME}")
    except BadRequestError:
        await promt.reply(NO_PERM)
        return
  else: 
    await tgbot.send_message(promt.chat_id, "**MASTER!!** __please enable MANAGER SERVICE__ by using `.set Config MANAGER ON`")

@tgbot.on(events.NewMessage(pattern="/demote ?(.*)"))
async def demote(event):
  if MANAGER == "ON":
    chat = await event.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    
    if not admin and not creator:
        await event.reply(NO_ADMIN)
        return
    await event.reply("`Demoting...`")
    rank = "Admeen"  # dummy rank, lol.
    user = await get_user_from_event(event)
    user = user[0]
    if user:
        pass
    else:
        return
    # New rights after demotion
    newrights = ChatAdminRights(
        add_admins=None,
        invite_users=None,
        change_info=None,
        ban_users=None,
        delete_messages=None,
        pin_messages=None,
    )
    # Edit Admin Permission
    try:
        await event.client(EditAdminRequest(event.chat_id, user.id, newrights, rank))
    except BadRequestError:
        await event.reply(NO_PERM)
        return
    await event.reply("Done.... Demoted 😂😂")
  else:
    await tgbot.send_message(event.chat_id, "**MASTER!!** __please enable MANAGER SERVICE__ by using `.set Config MANAGER ON`")
@tgbot.on(events.NewMessage(pattern="/pin_m ?(.*)"))
async def pin(msg):
  if MANAGER == "ON":
    chat = await msg.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # If not admin and not creator, return
    if not admin and not creator:
        await event.reply(NO_ADMIN)
        return
    to_pin = msg.reply_to_msg_id
    if not to_pin:
        await msg.reply("`Reply to a message to pin it.`")
        return
    options = msg.pattern_match.group(1)
    is_silent = True
    if options.lower() == "loud":
        is_silent = False

    try:
        await msg.client(UpdatePinnedMessageRequest(msg.to_id, to_pin, is_silent))
    except BadRequestError:
        await msg.reply(NO_PERM)
        return
    await msg.reply("`Pinned Successfully!`")
    user = await get_user_from_id(msg.sender_id, msg)
  else:
    await tgbot.send_message(msg.chat_id, "**MASTER!!** __please enable MANAGER SERVICE__ by using `.set Config MANAGER ON`")
    
@tgbot.on(events.NewMessage(pattern="/purge ?(.*)"))
async def _(event):
  if MANAGER == "ON":
    if event.fwd_from:
        return
    if event.reply_to_msg_id:
        i = 1
        msgs = []
        from_user = None
        input_str = event.pattern_match.group(1)
        if input_str:
            from_user = await client.get_entity(input_str)
            logger.info(from_user)
        for message in tgbot.get_messages(
            event.chat_id, min_id=event.reply_to_msg_id, from_user=from_user
        ):
            i = i + 1
            msgs.append(message)
            if len(msgs) == 100:
                await client.delete_messages(event.chat_id, msgs, revoke=True)
                msgs = []
        if len(msgs) <= 100:
            await client.delete_messages(event.chat_id, msgs, revoke=True)
            msgs = []
            await event.delete()
        else:
            await event.reply("**PURGE** Failed!")
            
  else:
    await tgbot.send_message(event.chat_id, "**MASTER!!** __please enable MANAGER SERVICE__ by using `.set Config MANAGER ON`")
@tgbot.on(events.NewMessage(pattern="/kick ?(.*)"))
async def kick(usr):
  if MANAGER == "ON":
    # Admin or creator check
    chat = await usr.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # If not admin and not creator, return
    if not admin and not creator:
        await usr.reply(NO_ADMIN)
        return

    user, reason = await get_user_from_event(usr)
    if not user:
        await usr.reply("`Couldn't fetch user.`")
        return

    await usr.reply("`Kicking...`")
    try:
        await usr.client.kick_participant(usr.chat_id, user.id)
        await sleep(0.5)
    except Exception as e:
        await usr.reply(NO_PERM + f"\n{str(e)}")
        return

    if reason:
        await usr.reply(f"`Kicked` [{user.first_name}](tg://user?id={user.id})`!`\nReason: {reason}")
    else:
        await usr.reply(f"`Kicked` [{user.first_name}](tg://user?id={user.id})`!`")
        
  else:
    await tgbot.send_message(event.chat_id, "**MASTER!!** __please enable MANAGER SERVICE__ by using `.set Config MANAGER ON`")

# Special For Alphax-UB 
# ©AlphaxUB™

BANNED_RIGHTS = ChatBannedRights(
  until_date = None,
  view_messages = True,
  send_messages = True,
  send_media = True,
  send_stickers = True,
  send_gifs = True,
  send_games = True,
  send_inline = True,
  embed_links = True,
)
UNBAN_RIGHTS = ChatBannedRights(
  until_date = None,
  send_messages = None,
  send_media = None,
  send_stickers = None,
  send_gifs = None,
  send_games = None,
  send_inline = None,
  embed_links = None,
)



@tgbot.on(events.NewMessage(pattern="/(ban|unban) ?(.*)"))
async def _(event):
  if MANAGER == "ON":
    if event.fwd_from:
      return
      datetime.now()
      to_ban_id = None
      rights = None
      input_cmd = event.pattern_match.group(1)
      if input_cmd == "ban":
        rights = BANNED_RIGHTS
      elif input_cmd == "unban":
        rights = UNBAN_RIGHTS
      input_str = event.pattern_match.group(2)
      reply_msg_id = event.reply_to_msg_id
      if reply_msg_id:
        r_mesg = await event.get_reply_message()
        to_ban_id = r_mesg.from_id
      elif input_str and "all" not in input_str:
        to_ban_id = int(input_str)
      else:
        return False
      try:
        await tgbot(EditBannedRequest(event.chat_id, to_ban_id, rights))
      except (Exception) as exc:
        await event.reply(str(exc))
      else:
        await event.reply(f" {input_cmd}ned **Successfully")
  else:
    await tgbot.send_message(event.chat_id, "**MASTER!!** __please enable MANAGER SERVICE__ by using `.set Config MANAGER ON`")

@tgbot.on(events.NewMessage(pattern="/mute ?(.*)"))
async def startmute(event):
  if MANAGER == "ON":
    private = False
    if event.fwd_from:
        return
    elif event.is_private:
        await event.reply("Unexpected issues or ugly errors may occur!")
        await asyncio.sleep(3)
        private = True
    reply = await event.get_reply_message()
    if event.pattern_match.group(1) is not None:
        userid = event.pattern_match.group(1)
    elif reply is not None:
        userid = reply.sender_id
    elif private is True:
        userid = event.chat_id
    else:
        return await event.reply("Please reply to a user or add their into the command to mute them."
        )
        chat_id = event.chat_id
    chat = await event.get_chat()
    if "admin_rights" in vars(chat) and vars(chat)["admin_rights"] is not None:
        if chat.admin_rights.delete_messages is True:
            pass
        else:
            return await event.reply("You can't mute a person if you dont have delete messages permission",
            )
    elif "creator" in vars(chat):
        pass
    elif private:
        pass
    else:
        return await event.reply("You can't mute a person without admin rights")
    if is_muted(userid, event.chat_id):
        return await event.reply("This user is already muted in this chat")
    try:
        mute(userid, event.chat_id)
    except Exception as e:
        await event.reply("Error occured!\nError is " + str(e))
    else:
        await event.reply("Successfully muted that person")
  else:
    await tgbot.send_message(event.chat_id, "**MASTER!!** __please enable MANAGER SERVICE__ by using `.set Config MANAGER ON`")

    
@tgbot.on(events.NewMessage(pattern="/unmute ?(.*)"))
async def endmute(event):
  if MANAGER == "ON":
    private = False
    if event.fwd_from:
        return
    elif event.is_private:
        await event.reply("Unexpected issues or ugly errors may occur!")
        await asyncio.sleep(3)
        private = True
    reply = await event.get_reply_message()
    if event.pattern_match.group(1) is not None:
        userid = event.pattern_match.group(1)
    elif reply is not None:
        userid = reply.sender_id
    elif private is True:
        userid = event.chat_id
    else:
        return await event.reply("Please reply to a user or add their into the command to unmute them.")
    chat_id = event.chat_id
    if not is_muted(userid, event.chat_id):
        return await event.reply("This user is not muted in this chat")
    try:
        unmute(userid, event.chat_id)
    except Exception as e:
        await event.reply("Error occured!\nError is " + str(e))
    else:
        await event.reply("Successfully unmuted that person")
  else:
    await tgbot.send_message(event.chat_id, "**MASTER!!** __please enable MANAGER SERVICE__ by using `.set Config MANAGER ON`")

@tgbot.on(events.NewMessage(incoming=True))
async def watcher(event):
    if is_muted(event.sender_id, event.chat_id):
        await event.delete()
@tgbot.on(events.NewMessage(pattern="/locktypes(.*)"))
async def _(event):
  if MANAGER == "ON":
    await event.reply(LOCKS)
  else:
    await tgbot.send_message(event.chat_id, "**MASTER!!** __please enable MANAGER SERVICE__ by using `.set Config MANAGER ON`")
@tgbot.on(events.NewMessage(pattern="/lock (.*)"))
async def _(event):
  if MANAGER == "ON":
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    peer_id = event.chat_id
    if input_str in (("bots", "commands", "email", "forward", "url", "msg", "media", "sticker", "gif", "gamee", "ainline", "gpoll", "adduser", "cpin", "changeinfo")):
        update_lock(peer_id, input_str, True)
        await event.reply("Locked {}".format(input_str))
    else:
        msg = None
        media = None
        sticker = None
        gif = None
        gamee = None
        ainline = None
        gpoll = None
        adduser = None
        cpin = None
        changeinfo = None
        if input_str:
            if "msg" in input_str:
                msg = True
            if "media" in input_str:
                media = True
            if "sticker" in input_str:
                sticker = True
            if "gif" in input_str:
                gif = True
            if "gamee" in input_str:
                gamee = True
            if "ainline" in input_str:
                ainline = True
            if "gpoll" in input_str:
                gpoll = True
            if "adduser" in input_str:
                adduser = True
            if "cpin" in input_str:
                cpin = True
            if "changeinfo" in input_str:
                changeinfo = True
        banned_rights = types.ChatBannedRights(
            until_date=None,
            # view_messages=None,
            send_messages=msg,
            send_media=media,
            send_stickers=sticker,
            send_gifs=gif,
            send_games=gamee,
            send_inline=ainline,
            send_polls=gpoll,
            invite_users=adduser,
            pin_messages=cpin,
            change_info=changeinfo,
        )
        try:
            result = await tgbot(
                functions.messages.EditChatDefaultBannedRightsRequest(
                    peer=peer_id, banned_rights=banned_rights
                )
            )
        except Exception as e:  # pylint:disable=C0103,W0703
            await event.reply(str(e))
        else:
            await event.reply("Current Chat Default Permissions Changed Successfully, in API"
            )
  else:
    await tgbot.send_message(event.chat_id, "**MASTER!!** __please enable MANAGER SERVICE__ by using `.set Config MANAGER ON`")

@tgbot.on(events.NewMessage(pattern="/unlock ?(.*)"))
async def _(event):
  if MANAGER == "ON":
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    peer_id = event.chat_id
    if input_str in (("bots", "commands", "email", "forward", "url", "msg", "media", "sticker", "gif", "gamee", "ainline", "gpoll", "adduser", "cpin", "changeinfo")):
        update_lock(peer_id, input_str, False)
        await event.reply("UnLocked {}".format(input_str))
    else:
        await event.reply("Use `.lock` without any parameters to unlock API locks")
  else:
    await tgbot.send_message(event.chat_id, "**MASTER!!** __please enable MANAGER SERVICE__ by using `.set Config MANAGER ON`")

@tgbot.on(events.MessageEdited())  # pylint:disable=E0602
@tgbot.on(events.NewMessage())  # pylint:disable=E0602
async def check_incoming_messages(event):
    peer_id = event.chat_id
    if is_locked(peer_id, "commands"):
        entities = event.message.entities
        is_command = False
        if entities:
            for entity in entities:
                if isinstance(entity, types.MessageEntityBotCommand):
                    is_command = True
        if is_command:
            try:
                await event.delete()
            except Exception as e:
                await event.reply(
                    "I don't seem to have ADMIN permission here. \n`{}`".format(str(e))
                )
                update_lock(peer_id, "commands", False)
    if is_locked(peer_id, "forward"):
        if event.fwd_from:
            try:
                await event.delete()
            except Exception as e:
                await event.reply(
                    "I don't seem to have ADMIN permission here. \n`{}`".format(str(e))
                )
                update_lock(peer_id, "forward", False)
    if is_locked(peer_id, "email"):
        entities = event.message.entities
        is_email = False
        if entities:
            for entity in entities:
                if isinstance(entity, types.MessageEntityEmail):
                    is_email = True
        if is_email:
            try:
                await event.delete()
            except Exception as e:
                await event.reply(
                    "I don't seem to have ADMIN permission here. \n`{}`".format(str(e))
                )
                update_lock(peer_id, "email", False)
    if is_locked(peer_id, "url"):
        entities = event.message.entities
        is_url = False
        if entities:
            for entity in entities:
                if isinstance(
                    entity, (types.MessageEntityTextUrl, types.MessageEntityUrl)
                ):
                    is_url = True
        if is_url:
            try:
                await event.delete()
            except Exception as e:
                await event.reply(
                    "I don't seem to have ADMIN permission here. \n`{}`".format(str(e))
                )
                update_lock(peer_id, "url", False)
  
@tgbot.on(events.ChatAction())  # pylint:disable=E0602
async def _(event):
    # TODO: exempt admins from locks
    # check for "lock" "bots"
    if is_locked(event.chat_id, "bots"):
        # bots are limited Telegram accounts,
        # and cannot join by themselves
        if event.user_added:
            users_added_by = event.action_message.from_id
            is_ban_able = False
            rights = types.ChatBannedRights(until_date=None, view_messages=True)
            added_users = event.action_message.action.users
            for user_id in added_users:
                user_obj = await borg.get_entity(user_id)
                if user_obj.bot:
                    is_ban_able = True
                    try:
                        await borg(
                            functions.channels.EditBannedRequest(
                                event.chat_id, user_obj, rights
                            )
                        )
                    except Exception as e:
                        await event.reply(
                            "I don't seem to have ADMIN permission here. \n`{}`".format(
                                str(e)
                            )
                        )
                        update_lock(event.chat_id, "bots", False)
                        break
            if Config.G_BAN_LOGGER_GROUP is not None and is_ban_able:
                ban_reason_msg = await event.reply(
                    "!warn [user](tg://user?id={}) Please Do Not Add BOTs to this chat.".format(
                        users_added_by
                    )
                )

@tgbot.on(events.NewMessage(pattern="/info ?(.*)"))
async def who(event):
  if MANAGER == "ON":
    cat = await event.reply("Astro Assistant steal some data from This guuyyy.🌚."
    )
    if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TEMP_DOWNLOAD_DIRECTORY)
    replied_user = await get_user(event)
    try:
        photo, caption = await fetch_info(replied_user, event)
    except AttributeError:
        await event.reply("`Could not fetch info of that user.`")
        return
    message_id_to_reply = event.message.reply_to_msg_id
    if not message_id_to_reply:
        message_id_to_reply = None
    try:
        await tgbot.send_file(
            event.chat_id,
            photo,
            caption=caption,
            link_preview=False,
            force_document=False,
            reply_to=message_id_to_reply,
            parse_mode="html",
        )
        if not photo.startswith("http"):
            os.remove(photo)
        await cat.delete()
    except TypeError:
        await cat.edit(caption, parse_mode="html")
  else: 
    await tgbot.send_message(event.chat_id, "**MASTER!!** __please enable MANAGER SERVICE__ by using `.set Config MANAGER ON`")

async def get_user(event):
    """Get the user from argument or replied message."""
    if event.reply_to_msg_id and not event.pattern_match.group(1):
        previous_message = await event.get_reply_message()
        replied_user = await event.client(
            GetFullUserRequest(previous_message.sender_id)
        )
    else:
        user = event.pattern_match.group(1)
        if user.isnumeric():
            user = int(user)
        if not user:
            self_user = await event.client.get_me()
            user = self_user.id
        if event.message.entities:
            probable_user_mention_entity = event.message.entities[0]
            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                replied_user = await event.client(GetFullUserRequest(user_id))
                return replied_user
        try:
            user_object = await event.client.get_entity(user)
            replied_user = await event.client(GetFullUserRequest(user_object.id))
        except (TypeError, ValueError) as err:
            await event.edit(str(err))
            return None
    return replied_user


async def fetch_info(replied_user, event):
    """Get details from the User object."""
    replied_user_profile_photos = await event.client(
        GetUserPhotosRequest(
            user_id=replied_user.user.id, offset=42, max_id=0, limit=80
        )
    )
    replied_user_profile_photos_count = "User haven't set profile pic"
    try:
        replied_user_profile_photos_count = replied_user_profile_photos.count
    except AttributeError:
        pass
    user_id = replied_user.user.id
    first_name = replied_user.user.first_name
    last_name = replied_user.user.last_name
    try:
        dc_id, location = get_input_location(replied_user.profile_photo)
    except:
        dc_id = "Couldn't fetch ViU ID!"
    common_chat = replied_user.common_chats_count
    username = replied_user.user.username
    user_bio = replied_user.about
    is_bot = replied_user.user.bot
    restricted = replied_user.user.restricted
    verified = replied_user.user.verified
    photo = await event.client.download_profile_photo(
        user_id, TEMP_DOWNLOAD_DIRECTORY + str(user_id) + ".jpg", download_big=True
    )
    first_name = (
        first_name.replace("\u2060", "")
        if first_name
        else ("This User has no First Name")
    )
    last_name = (
        last_name.replace("\u2060", "") if last_name else ("This User has no Last Name")
    )
    username = "@{}".format(username) if username else ("This User has no Username")
    user_bio = "This User has no About" if not user_bio else user_bio
    caption = "<b>USER INFO FROM ALPHAX-UB :</b>\n\n"
    caption += f"👤First Name: {first_name} {last_name}\n"
    caption += f"🤵Username: {username}\n"
    caption += f"🔖ID: <code>{user_id}</code>\n"
    caption += f"🌏Data Centre ID: {dc_id}\n"
    caption += f"🖼Number of Profile Pics: {replied_user_profile_photos_count}\n"
    caption += f"🤖Is Bot: {is_bot}\n"
    caption += f"🔏Is Restricted: {restricted}\n"
    caption += f"🌐Is Verified by Telegram: {verified}\n\n"
    caption += f"✍️Bio: \n<code>{user_bio}</code>\n\n"
    caption += f"👥Common Chats with this user: {common_chat}\n"
    caption += f"🔗Permanent Link To Profile: "
    caption += f'<a href="tg://user?id={user_id}">{first_name}</a>'
    return photo, caption


@tgbot.on(events.NewMessage(pattern="/id ?(.*)"))
async def getid(event):
  if MANAGER == "ON":
      replied_user = await get_user(event)
      user_id = replied_user.user.id
      await tgbot.send_message(event.chat_id, f"User ID: `{user_id}`")
  else:
    await tgbot.send_message(event.chat_id, "**MASTER!!** __please enable MANAGER SERVICE__ by using `.set Config MANAGER ON`")

async def get_user_from_event(event):
    args = event.pattern_match.group(1).split(" ", 1)
    extra = None
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        user_obj = await event.client.get_entity(previous_message.sender_id)
        extra = event.pattern_match.group(1)
    elif args:
        user = args[0]
        if len(args) == 2:
            extra = args[1]

        if user.isnumeric():
            user = int(user)

        if not user:
            await event.reply("`Pass the user's username, id or reply!`")
            return
        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]

            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj
        try:
            user_obj = await event.client.get_entity(user)
        except (TypeError, ValueError) as err:
            await event.reply(str(err))
            return None

    return user_obj, extra


async def get_user_from_id(user, event):
    if isinstance(user, str):
        user = int(user)

    try:
        user_obj = await event.client.get_entity(user)
    except (TypeError, ValueError) as err:
        await event.reply(str(err))
        return None
    return user_obj
