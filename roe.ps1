<#
.SYNOPSIS
    Mission Briefing & Operation Framework for Project: UPSIDE DOWN.
    Target: HAWKINS.MAD
#>

Clear-Host

# --- THE VOID COLORS ---
$Vines = "DarkGray"
$Blood = "DarkRed"
$Ozone = "Cyan"
$Clock = "Yellow"

function Show-Briefing {
    Write-Host @"
    .          .           .           .           .           .       .       .                  .

    .         .            .           .            .          .       .       .                 .
 
    .          .           .           .           .           .        .       .                 .

    ____  _   _ _____   _   _ ____  ____ ___ ____  _____   _   _ ____  _____ ______           _______
  _______ _    _ ______   _    _ _____   _____ _____ _____  ______   _____   ______          __ _   _ 
 |__   __| |  | |  ____| | |  | |  __ \ / ____|_   _|  __ \|  ____| |  __ \ / __ \ \        / /| \ | |
    | |  | |__| | |__    | |  | | |__) | (___   | | | |  | | |__    | |  | | |  | \ \  /\  / / |  \| |
    | |  |  __  |  __|   | |  | |  ___/ \___ \  | | | |  | |  __|   | |  | | |  | |\ \/  \/ /  | .   |
    | |  | |  | | |____  | |__| | |     ____) |_| |_| |__| | |____  | |__| | |__| | \  /\  /   | |\  |
    |_|  |_|  |_|______|  \____/|_|    |_____/|_____|_____/|______| |_____/ \____/   \/  \/    |_| \_|
                                                                                                       
"@ -ForegroundColor $Blood

    Write-Host "`n[+] MISSION BRIEFING: THE UPSIDE DOWN" -ForegroundColor $Ozone
    Write-Host "[+] Status: TRAPPED" -ForegroundColor $Blood
    Write-Host "------------------------------------------------------------" -ForegroundColor $Vines
    
    $Briefing = @"
The terminal in front of you isn't running standard code anymore. 
The bits are decaying. The packets are bleeding. 
You are a prisoner of the Mindflayer's Hive Mind.

Every server is a vine, every user is a drone, and the Domain Controllers 
are the pulsating hearts of a dark dimension.
"@
    Write-Host $Briefing -ForegroundColor $Vines
    
    Start-Sleep -Seconds 1
    Write-Host "------------------------------------------------------------" -ForegroundColor $Vines
    Write-Typewriter "The lights are flickering. The air is growing cold." -color $White
    Write-Typewriter "You aren't auditing a network anymore, You are the Part of IT" -color $White
    Write-Typewriter "You were performing the Penetration Test on Network and MindFlayer Trapped you into His Network!" -color $Red -delay 80

    Write-Host "`n[+] THE ANTAGONIST: VECNA" -ForegroundColor $Clock
    Write-Host "He knows you are here. He can hear your keystrokes. The grandfather clock is ticking." -ForegroundColor $Vines

    Write-Host "`n[+] YOUR OBJECTIVE: ESCAPE" -ForegroundColor $Ozone
    Write-Host "1. Pierce the Veil: Break through the child domain's defenses."
    Write-Host "2. Navigate the Shadows: Use the ghosts of deleted users."
    Write-Host "3. Slay the Root: Seize Domain Admin credentials of HAWKINS.MAD."
    Write-Host "4. Close the Gate: Run the final containment script." -ForegroundColor $Vines

    Write-Host "`n[+] RULES OF THE VOID" -ForegroundColor $Blood
    Write-Host " - The Hive Mind is Watching (AV is aggressive)."
    Write-Host " - Trust No One (Not even service accounts)."
    Write-Host " - The Clock is Ticking (Reach the Root or become the architecture)."
    Write-Host "------------------------------------------------------------" -ForegroundColor $Vines
}

function Write-Typewriter ($text, $color = $White, $delay = 40) {
    Write-Host -NoNewline $color
    $text.ToCharArray() | ForEach-Object {
        Write-Host -NoNewline $_
        if ($_ -ne ' ') { Start-Sleep -Milliseconds $delay }
    }
    Write-Host $Reset
}

function Start-GrandfatherClock {
    Write-Host "`n[!] The Grandfather Clock chimes in the distance..." -ForegroundColor $Clock
    for ($i = 1; $i -le 4; $i++) {
        Write-Host "TICK-TOCK... " -NoNewline -ForegroundColor $Clock
        # Simulate a glitchy terminal delay
        Start-Sleep -Milliseconds (Get-Random -Minimum 800 -Maximum 1200)
    }
    Write-Host "`n"
}

# --- INITIALIZATION ---
Show-Briefing
Start-GrandfatherClock

Write-Host "[*] Establishing connection to the Lab..." -ForegroundColor $Vines
$TargetDomain = "HAWKINS.MAD"
Write-Host "[+] Current Domain: $TargetDomain" -ForegroundColor $Ozone

# --- PHASE 1: PIERCE THE VEIL ---
Write-Host "`n[>] Phase 1: Piercing the Veil..." -ForegroundColor $Ozone
# Logic for initial discovery goes here