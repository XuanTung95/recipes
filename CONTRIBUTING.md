Contributing to Recipes
=======================

tl;dr: join [Discord](https://github.com/flutter/flutter/wiki/Chat), be [courteous](https://github.com/flutter/flutter/blob/master/CODE_OF_CONDUCT.md),
follow the steps below to set up a development environment.

Welcome
-------

We invite you to join the Flutter team, which is made up of volunteers and sponsored folk alike!
There are many ways to contribute, including writing code, filing issues on GitHub, helping people
on our mailing lists, our chat channels, or on Stack Overflow, helping to triage, reproduce, or
fix bugs that people have filed, adding to our documentation,
doing outreach about Flutter, or helping out in any other way.

For additional context please read the Flutter's [CONTRIBUTING document](https://github.com/flutter/flutter/blob/master/CONTRIBUTING.md).

Initial setup
-------------

### Sign in to Gerrit

Gerrit is a free, web-based team code collaboration tool. Software developers in a team can review each other's
modifications on their source code using a Web browser and approve or reject those changes. It integrates closely
with Git, a distributed version control system. Flutter uses Gerrit/Git for source code control to take advantage
of the existent LUCI integrations.

A `git` client must be pre-installed in your system.

Visit [Flutter's Gerrit Host](https://flutter-review.googlesource.com/) and click the sign in link on the
top right section of the page.


### Create a gerrit account

Visit the [Settings page of the Flutter Gerrit Host](https://flutter-review.googlesource.com/settings/). It will
offer to create a gerrit account, follow the on screen instructions to create the account.


### Generate passwords

Visit the [Settings page of the Flutter Gerrit Host](https://flutter-review.googlesource.com/settings/). Scroll
down close to the bottom and click on the `obtain password link`, click on allow, copy the command from the new window
and run it on your git terminal. This will cache your credentials in your local environment.


### Sign CLA

Visit the [Settings page of the Flutter Gerrit Host](https://flutter-review.googlesource.com/settings/). Scroll down
close to the bottom and click on the `new contributor agreement` link, select Google CLA, review the CLA and accept the
agreement.


### Check out the repository

Finally you can finish your setup by cloning the git repository:

```
git clone https://flutter.googlesource.com/recipes
cd recipes
```

Creating a change list (pull request)
-------------------------------------

Once you have created a gerrit account, generated passwords (ran the associated commands), and accepted
the CLA, you can start submitting a CL (change list, what Gerrit calls PRs).

The following commands can be used to create a new change list and sent it for review:

```
git checkout -b <new_branch>
# prepare your patch, run git add <files> or git rm <files> as appropriate
git commit
git push origin HEAD:refs/for/main
```

If this is your first CL and you get an error related to  "missing Change-Id in message footer",
run the command provided in the hint section above the error. This is is required only in the first
CL to enable the hook to automatically add a change ID to the CL.

Then, run the following commands to attempt to submit the CL again:

```
git commit --amend --no-edit
git push origin HEAD:refs/for/main
```
