
Version 3.0.0
----------------------

Released on 2013-05-23

    * removed:    ongeza-git-changelog
    * added more options
        * git tag + commit + push is not done optionally by specifying:
          skip_tag, skip_commit, skip_push respectively
    * script fails when there is uncommitted junk in the repo
    * refactored quite a bit of the code to make it a bit more OOP


Version 2.0.2
----------------------

Released on 2013-05-23

    * CHANGES.md added to repo
        * added changelog summary for 2.0.1
    * minor updates to project README.md
    * renamed:    ongeza.py -> ongeza. updated setup script
    * renamed:    git-changelog -> ongeza-git-changelog
    * git tag list fix
        * changed git tag list command to sort by authordate
    * added some parsing of the git summaries
        * remove merge commits and commits with potentially bad messages


Version 2.0.1
----------------------

Released on 2013-03-15

  * git tag list fix
      * changed `git tag list` sub-command to sort by authordate
  * pypi script added to repo
      * updated gitignore to match distribute generated files
