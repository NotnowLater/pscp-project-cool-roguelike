"""" Store all the audio reference """

import audio

### BGM
main_bgm = audio.AudioPlayBack("sounds/scifimain.mp3", True)


### SFX 
punch_1 = audio.AudioPlayBack("sounds/sfx_punch.mp3", False)
explosive_grenade = audio.AudioPlayBack("sounds/sfx_explosive_grenade.mp3", False)
flash_grenade = audio.AudioPlayBack("sounds/sfx_flash_grenade.mp3", False)
nano_patch = audio.AudioPlayBack("sounds/sfx_nano_patch.mp3", False)
ammo_box = audio.AudioPlayBack("sounds/sfx_ammo_box.mp3", False)
gun_1 = audio.AudioPlayBack("sounds/sfx_gunf1.mp3", False)
gun_2 = audio.AudioPlayBack("sounds/sfx_gunf2.mp3", False)
knife_1 = audio.AudioPlayBack("sounds/sfx_knife.mp3", False)
game_over = audio.AudioPlayBack("sounds/sfx_game_over.mp3", False)
boom = audio.AudioPlayBack("sounds/sfx_spaceship_explosion.mp3", False)
