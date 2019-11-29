# Arch Linux Update Notification
![update-notification](https://user-images.githubusercontent.com/11918572/69885341-a9ed8780-1302-11ea-9723-bd5a85b0d0d2.png)

Arch Linux Update Notification Python script runs at start-up and shows notification about new updates available and also opens up terminal to install updates.

# Purpose 
I just created this because I didn't want to install GUI package manager and just wanted notification which opened up terminal with update command already entered so I can update sytem through the terminal. I had to choose Python over bash because `notify-send` doesn't allow buttons.

# Dependencies
`gi` module in Python 3 most likely installed on your system as dependency for other programs that send such notifications.

# Installation on XFCE
Just download this script somewhere go to "Session & startup" in XFCE and in application autostart tab add entry for this script, command for the script will be
`python3 /location/to/update-notification.py`
This script will run everytime on startup and check for updates if there are updates available it'll send a notification.

## Usage
Default shell is bash, default AUR helper is yay

```
Usage: update-notification.py [options]

Options:
  -h, --help            show this help message and exit
  --aur-check=AUR_CHECK
                        Specify AUR helper's update check command
  --aur-update=AUR_UPDT
                        Specify AUR helper's update command
  --shell-name=SHELL    Specify your shell bash/zsh/fish
```

# Non XFCE
You just need to change name of your terminal currently it's set to `xfce4-terminal` you can change it to `konsole` with relevant arguments for [opening 2 tabs](https://github.com/fellchase/update-notification/blob/b47fbdd5b29aa5d487cf01b33c99f6cbfd4f4316/update-notification.py#L35) and [opening single tab](https://github.com/fellchase/update-notification/blob/b47fbdd5b29aa5d487cf01b33c99f6cbfd4f4316/update-notification.py#L37)


# Support
If you found this useful or want to share opinions about it you can contact me on [@fellchase](https://twitter.com/fellchase) you can also buy me a coffee so I don't fall asleep while studying via [paypal.me/fellchase](https://www.paypal.me/fellchase)
