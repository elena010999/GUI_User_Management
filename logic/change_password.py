#!/usr/bin/env python3
from logic.helper_functions import run_pkexec

def change_password(username):
    run_pkexec(
        ["passwd", username],
        f"Password changed successfully for '{username}'!",
        f"Failed to change password for '{username}'."
    )

