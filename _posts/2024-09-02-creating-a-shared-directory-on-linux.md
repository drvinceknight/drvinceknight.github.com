---
layout: post
title: "Creating a shared directory on linux"
date: 2024-09-02
categories: how-to
comments: true
---

This is a quick how to reminder for creating shared directories on linux. This
is mainly to avoid committing large amounts of data files and instead using a
shared computer that can be `scp`'d back and forth to.

### Create a shared group

```
$ sudo groupadd jokeying
```

Here I'm creating a group called `jokeying` (for a paper I'm working on).

### Adding users to the new shared group

```
$ sudo usermod -a -G jokeying vince
$ sudo usermod -a -G jokeying geraint
```

### Seeing who is a member of a group

```
$ getent group jokeying
```

### Creating a shared directory

From [this stack overflow page](https://unix.stackexchange.com/questions/70700/whats-the-most-appropriate-directory-where-to-place-files-shared-between-users) a good place
to have a shared directory that is expected to change is: `/var/`.

```
$ sudo mkdir /var/jokeying-results
```

### Setting up the permissions for the directory

```
$ sudo chgrp -R jokeying /var/jokeying-results/
$ sudo chmod -R 2775 /var/jokeying-results/
```

I do not fully follow what each of those options do. The details can be found
[here](https://www.tecmint.com/create-a-shared-directory-in-linux/).

### Writing a script to keep the shared directory synced

```
rsync -aO <local_dir> <remote>:/var/jokeying-results
rsync -aO <remote>:/var/jokeying-results <local_dir>
```

This runs rsync in both directions. The `a` flag uses archive mode. The `O` flag
ensures that the rsync does not try to modify time stamps.
