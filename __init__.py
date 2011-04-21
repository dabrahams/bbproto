# Why is this file here?
#
# Buildbot leaves droppings in the directory where it finds
# master.cfg.  We don't want those droppings polluting this source
# tree.  So instead of running buildbot directly on master.cfg, we run
# it on a symlink living in our parent directory.  When master.cfg
# loads bbproto, python finds this file.
#
# However, when we run buildbot checkconfig directly from this
# directory for testing purposes, master.cfg still needs to be able to
# load bbproto.  Thus the symlink in this directory called "bbproto."
