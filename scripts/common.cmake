# ctest_command: ctest commmand
# ctest_model : dashboard model to use.
# ctest_source : path to source dir
# ctest_build : path to build dir
# ctest_buildname : name for the build.
# ctest_site: name for the site.
# ctest_generator : generator
# ctest_configure_options_file : file with command line options to pass the configure step.
# ctest_test_excludes_file : file with test exludes to pass to ctest_test() command.
# ctest_stages: all, configure, build, test
set (CTEST_SOURCE_DIRECTORY "${ctest_source}")
set (CTEST_BINARY_DIRECTORY "${ctest_build}")
set (CTEST_COMMAND "${ctest_command}")
set (CTEST_CMAKE_GENERATOR "${ctest_generator}")
set (CTEST_BUILD_NAME "${ctest_buildname}")
set (CTEST_SITE "${ctest_site}")

#FIXME: We need to configure this, not hardcode it!!!!
set (CTEST_BUILD_FLAGS "-j9")

set (CTEST_CMAKE_GENERATOR "${ctest_generator}")
if (EXISTS "${ctest_configure_options_file}")
    file(READ "${ctest_configure_options_file}" ctest_configure_options)
endif()

if (EXISTS "${ctest_test_excludes_file}")
    file(READ "${ctest_test_excludes_file}" ctest_test_excludes)
endif()

# Avoid non-ascii characters in tool output.
set(ENV{LC_ALL} C)

ctest_start(${ctest_model} ${ctest_source} ${ctest_build})

#==============================================================================
# Configure
#==============================================================================
if ("${ctest_stages}" STREQUAL "all" OR "${ctest_stages}" MATCHES ".*configure.*")
    ctest_configure(OPTIONS "--no-warn-unused-cli;${ctest_configure_options}"
                    RETURN_VALUE configure_result)

    #if (EXISTS "${ctest_build}/CMakeCache.txt")
    #    # If CMakeCache.txt is present. Let's upload that to the dashboard as well.
    #    # Helps debug issues.
    #    list (APPEND CTEST_NOTES_FILES "${ctest_build}/CMakeCache.txt")
    #endif()
    ctest_submit(PARTS Configure Notes)

    # If configuration failed, report error and stop test.
    if (NOT "${configure_result}" STREQUAL "0")
        message(FATAL_ERROR "Configure failed!!!")
    endif()
endif()

#==============================================================================
# Build
#==============================================================================
# Read ctest custom files from the project.
ctest_read_custom_files(${ctest_build})

if ("${ctest_stages}" STREQUAL "all" OR "${ctest_stages}" MATCHES ".*build.*")
    ctest_build(RETURN_VALUE build_result
                NUMBER_ERRORS build_number_errors
                NUMBER_WARNINGS build_number_warnings)
    ctest_submit(PARTS Build)

    # If build failed (or had non-zero errors), report error and stop test.
    if ( (NOT "${build_number_errors}" STREQUAL "0") OR
         (NOT "${build_result}" STREQUAL "0") )
         message(FATAL_ERROR "Build failed with ${build_number_errors} errors and ${build_number_warnings} warnings!!!")
    endif()
endif()
#==============================================================================
# Test
#==============================================================================
if ("${ctest_stages}" STREQUAL "all" OR "${ctest_stages}" MATCHES ".*test.*")
    if (ctest_test_excludes)
        ctest_test(EXCLUDE "${ctest_test_excludes}" RETURN_VALUE test_result)
    else()
        ctest_test(RETURN_VALUE test_result)
    endif()
    ctest_submit(PARTS Test)

    if (NOT "${test_result}" STREQUAL "0")
        message(FATAL_ERROR "Tests failed!!!")
    endif()
endif()
