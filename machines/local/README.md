Running a local test instance
=============================

This repository is set up to facilitate testing when the `KW_BUILDBOT_TESTING`
environment variable is set. This causes all builders except the `local`
builder to be disabled (the others are imported so that they are at least
syntax-checked). In the `local` machine, add a `slave.py` describing your test
slave as well as any project files you are testing. These will be automatically
picked up.
