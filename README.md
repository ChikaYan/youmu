# Youmu
This is mainly a bot for dealing with touhou stuff. Currently it supports Japanese hiragana/katakana -> romaji conversion, touhou soku hosting management (including hamachi hosting) and pixiv arts sharing.
The original bot is meant to be run on my server only. However feel free to use, reuse and abuse the code and host your own youmu.

Command List
---------------
**Info**: the prefix for Youmu is !?
### Touhou Hisoutensoku ###
Command | Usage
--------|-------
`:!?addhost [IP:Port]` | Add your public IP address and port for soku
`:!?addhost [IP:Port] (hamachi [Room ID])` | Add your hamachi IP and port, as well as the hamachi room ID
`:!?addhamachi [Room ID] [Password]` | Add a hamachi room information
`:!?host ([Message])`| Start hosting at pre-stored IP address and port. If [Message] is given, the message will be shown in the hosting message as well.
`:!?endhost` | End current host
`:!?showhost` | List all currently active hosts
`:!?soku` | Mention all the members that have told their IP to Youmu and call them to soku!
