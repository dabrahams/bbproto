BuildBot Configuration Prototype
================================ 

A tiny, but general, exploratory buildmaster configuration.

Goals
-----

* Reveal a clean way to set up a nontrivial standalone buildbot master configuration today
* Discover what buildbot could do for users to make such configurations easier

Again, this is a *standalone* solution, not dependent on anything but
buildbot itself.  The [BoostPro BBot](http://github.com/boostpro/bbot)
project implements these techniques, to the extent possible, in a
library (along with other enhancements).

Desiderata
----------

1. Maintain a clean source directory (Buildbot leaves droppings in the
   "bot directory" where it finds the master.cfg file)
   
2. Support modular code and flexible project organization

3. Support `buildbot reconfig` 

4. Support `buildbot checkconfig` from the root of the source tree

5. Avoid the complex module reloading gymnastics often needed to support `buildbot reconfig`.

6. Especially avoid the need to maintain
   [explicit `reload(...)` calls](https://github.com/buildbot/metabbotcfg/blob/512d4c5a970e91f96ea4fcd7c519e3866d383698/master.cfg#L3)
   that need to be updated as the source tree changes.
   
7. Cloning a single configuration repository (and perhaps its
   git submodules) prepares the entire configuration
   
8. Customizations of `buildbot create-master`-generated files (see
   `public_html`) can be stored in the source repository.

9. Avoid complexity

Testing
-------

To see the prototype in action, 

* use a filesystem that supports symbolic links (pre-Vista NTFS won't do)
* clone this repository *in an empty directory*; the clone **must be called `bbproto`**.
* `cd bbproto`
* run the `test` executable that's in the current directory
   
Status and Recommendations
--------------------------

1. **A clean source directory** can be maintained only at the cost of
   requiring the user to create a symbolic link to the configuration
   file from the bot directory, as the `test` script does, *and*
   requiring the source directory to maintain the name `bbotproto` as
   described in the "Testing" section above (traditionally it doesn't
   matter what you call the top-level of a source checkout, but it
   matters here). Buildbot now leaves its droppings in the bot directory
   and the source tree remains untouched.  Buildbot could be improved
   by allowing the user to specify separate `--bot-directory=` and
   configuration file arguments on the `create-master` command line so
   that this symlink would be unneeded.
   
   In the current release 0.8.3, and in the development trunk prior to
   2011-04-17, `buildbot checkconfig` would do its work in a temporary
   *shallow copy* of the bot directory.  That added a further
   restriction that the symbolic link be absolute and not relative,
   and complicated the use of Python submodules.

2. **Modular code** implies the ability to use Python submodules.
   That is currently complicated by goals 3 and 4 (see below).  With
   respect to **flexible organization**, there may be modules we need
   to get into `sys.path` that aren't directly contained in the
   configuration directory.  For example, I use a 3rd-party project as
   a git submodule in one of my configurations, and it doesn't have a
   top-level `__init__.py` file.  Unfortunately, `master.cfg` isn't
   loaded as an ordinary module and so doesn't get a `__file__`
   attribute that we can use as the basis for modifications to
   `sys.path`.  To make such modifications, `master.cfg` must
   immediately import a module in the same directory so it can
   reference its `__file__` (in this project, `master.py`).  Buildbot
   could be improved by giving configuration files some reliable way
   to find out what directory they were loaded from.

3. `buildbot reconfig` forces the master.cfg file to be reloaded,
   but if you made changes to other files, they won't be reloaded.  In
   this project, `master.cfg` detects whether it's being reloaded, and
   if so, releases all modules in the configuration directory tree
   that came in during its previous load.  This accounts for
   approximately 10 lines of boilerplate code that would be better to
   have somewhere in buildbot.

4. Supporting `buildbot checkconfig` **from the root** of the source tree
   is complicated by the solution to goal 1, above.  Keeping a clean
   source tree requires that buildbot is not run from this directory
   in production.  The ugly workaround is the symbolic link, called
   `bbproto`, to its own directory at the top level.  Buildbot could
   be improved by explicitly supporting `buildbot checkconfig` from
   the root of the source tree.

5. We've clearly failed to avoid **complex module reloading
   gymnastics**, but if Buildbot followed the recommendation of item 3,
   we could.

6. We *have* managed to **avoid explicit `reload(...)` calls** that
   need to be updated as the source tree changes.  Yay, us!
   
7. **Preparing the entire configuration** requires establishing a symbolic
   link as described in item 1, so we've failed in goal 7.
   
8. I think we could store **customized `buildbot
   create-master`-generated files in the source repository** but the
   user would have to create more symbolic links as part of the
   configuration process.  I'm not sure what to recommend here, yet.
   Perhaps once there's a separate `--bot-directory` argument, it
   would work to have Buildbot look first for these files in a
   directory next to the `.cfg` file, and only afterward fall back to
   the bot directory.

9. Did we **avoid complexity?** You be the judge.


