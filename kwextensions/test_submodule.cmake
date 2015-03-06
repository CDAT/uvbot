cmake_minimum_required(VERSION 2.8.8)

find_program(GIT_COMMAND NAMES git git.cmd)

execute_process(COMMAND "${GIT_COMMAND}" "rev-parse" "HEAD"
                OUTPUT_VARIABLE headRevision
                OUTPUT_STRIP_TRAILING_WHITESPACE)

execute_process(COMMAND "${GIT_COMMAND}" "merge-base" "HEAD" "origin/master"
                OUTPUT_VARIABLE mergeBaseRevision
                OUTPUT_STRIP_TRAILING_WHITESPACE)

message(STATUS "current submodule HEAD:        ${headRevision}")
message(STATUS "merge base with origin/master: ${mergeBaseRevision}")

string(COMPARE EQUAL "${headRevision}" "${mergeBaseRevision}" submoduleIsGood)

if(NOT submoduleIsGood)
    message(WARNING "Error: commits are not merged to master.")
endif()

execute_process(COMMAND "${GIT_COMMAND}" "rev-list" "--first-parent" "${mergeBaseRevision}~..master"
                OUTPUT_VARIABLE masterFirstParentList)

string(FIND "${masterFirstParentList}" "${headRevision}" index)

if(index STREQUAL "-1")
    message(WARNING "Error: head is not in the first parent list of master.")
endif()
