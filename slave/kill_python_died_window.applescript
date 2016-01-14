#!/usr/bin/osascript

tell application "System Events"
    repeat with theProcess in processes
            tell theProcess
                set processName to name
                set windowCount to number of windows
                set pid to id
                repeat with x from 1 to windowCount
                    set winname to name of window x
                    if winname is missing value then
                        tell window x to click button "ignore"
                    end if
                    log winname
                end repeat
            end tell
    end repeat
end tell
