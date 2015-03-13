cmake_minimum_required(VERSION 2.8.8)

# This should be run with two command line arguments.  The first
# is the base url name to search for user forks (-Durl_prefix:STRING=...)
# The second is the username to check (-Dusername:STRING=...)

find_program(GIT_COMMAND NAMES git git.cmd)

execute_process(COMMAND "${GIT_COMMAND}" "remote" "-v"
                OUTPUT_VARIABLE remotes)


string(REGEX MATCH "origin.*\\(fetch" line "${remotes}")


string(REGEX MATCH "[^ \t]+[ \t]+([^ \t]+)[ \t]+[^\t ]+" myurl "${line}")

string(REGEX MATCH "[^/]+$" repoName "${CMAKE_MATCH_1}")

# used for testing before submodules moved to gitlab with lowercase origin URLS
string(TOLOWER "${repoName}" repoName)

set(userFork "${url_prefix}/${username}/${repoName}")

message("${userFork}")

execute_process(COMMAND "${GIT_COMMAND}" "remote" "add" "tmp" "${userFork}")

execute_process(COMMAND "${GIT_COMMAND}" "fetch" "tmp"
                RESULT_VARIABLE fetchResult)

if(fetchResult)
    message("Fetch failed, continuing...")
endif()

execute_process(COMMAND "${GIT_COMMAND}" "remote" "remove" "tmp")
