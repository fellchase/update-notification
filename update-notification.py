#!/usr/bin/python3

import gi, os, optparse, socket
gi.require_version('Notify', '0.7')
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Notify


Notify.init('Update Notification')

parser = optparse.OptionParser()
parser.add_option("--aur-check", help="Specify AUR helper's update check command", default='yay -Qua', action="store", dest='aur_check')
parser.add_option("--aur-update", help="Specify AUR helper's update command", default="yay -Syu -a", action="store", dest='aur_updt')
parser.add_option("--shell-name", help="Specify your shell bash/zsh/fish", default="bash", action="store", dest='shell')
(opt_args, argv) = parser.parse_args()


def count_lines(text):
    list_rcower = text.split('\n')
    while True:
        try:
            list_rcower.remove('')
        except ValueError:
            break
    return len(list_rcower)


# Avoid putting pacman -Syyu -yes for all kind of command here as you may not want pacman taking some decisions on it own like removing conflicting packages
aur_command = "{} -c \"{} && echo && echo Press enter to update && read && {}; exec {}\"".format(opt_args.shell, opt_args.aur_check , opt_args.aur_updt, opt_args.shell)
sys_command = "{} -c \"checkupdates && echo && echo Press enter to update && read && sudo pacman -Syyu; exec {}\"".format(opt_args.shell ,opt_args.shell)


def button_callback(notification, action, info=None):
    if len(info) == 2:
        cmd = "xfce4-terminal --geometry 150x35 -T '{}' -e '{}' --tab -T '{}' -e '{}'".format(info[0]['title'], info[0]['command'], info[1]['title'], info[1]['command'])
    else:
        cmd = "xfce4-terminal --geometry 150x35 -T '{}' -e '{}'".format(info[0]['title'], info[0]['command'])
    print(cmd)

    os.system(cmd)
    quit(0)

try:
    # Check if internet connection is available
    socket.setdefaulttimeout(7)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("8.8.8.8", 53))
    print("Internet connection available")

    nsystem_updates = count_lines(os.popen('checkupdates').read())
    print("Number of system updates available " + str(nsystem_updates))
    print('Checking for updates system_update_chk')

    naur_updates = count_lines(os.popen(opt_args.aur_check).read())
    print("Number of AUR updates available " + str(naur_updates))
    print('Checking for updates aur_update_chk')
    
    # The English Grammar has to be perfect right?
    if nsystem_updates != 0:
        if nsystem_updates == 1:
            sys_string = "1 system update available"
        else:
            sys_string = str(nsystem_updates) + " system updates available"
    else:
        sys_string = ''

    if naur_updates != 0:
        if naur_updates == 1:
            aur_string = "1 AUR update available"
        else:
            aur_string = str(naur_updates) + " AUR updates available"
    else:
        aur_string = ''

    # Display the notification
    if naur_updates == 0 and nsystem_updates == 0:
        quit()
    elif naur_updates >= 1 and nsystem_updates == 0:
        sys_notification = Notify.Notification.new("Update Notification", aur_string, "system-software-update")
        sys_notification.add_action('clicked', 'Update', button_callback, [
            {'title': 'Updating AUR Packages', 'command': aur_command}])
    elif naur_updates == 0 and nsystem_updates >= 1:
        sys_notification = Notify.Notification.new("Update Notification", sys_string, "system-software-update")
        sys_notification.add_action('clicked', 'Update', button_callback, [
            {'title': 'Updating System Software', 'command': sys_command}])
    elif naur_updates >= 1 and nsystem_updates >= 1:
        sys_notification = Notify.Notification.new("Update Notification", '\n' + sys_string + '\n' + aur_string, "system-software-update")
        sys_notification.add_action('clicked', 'Update', button_callback, [
            {'title': 'Updating System Software', 'command': sys_command}, 
            {'title': 'Updating AUR Packages', 'command': aur_command}])

    sys_notification.show()
except Exception as e:
    print("No internet connection")
    print(e)
    Notify.Notification.new("Update Notification", "No internet connection", "system-software-update").show()
    quit(0)
finally:
    print("Closing the socket")
    s.close()

GLib.MainLoop().run()
