import sys
import win10toast

# Lire l'information envoyée via stdin
information = sys.stdin.read()

print(information)
toaster = win10toast.ToastNotifier()
toaster.show_toast(information, information, duration=10)