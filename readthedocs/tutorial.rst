
Note we have GoogleAnalytics enabled for this tutorial to help show our funders that the work
we do is useful to others.

|
|
|

Getting started
---------------

On your system, start VirtualBox.

This tutorial uses a virtual machine to help avoid issues that are due to system configuration.
In case you don't have a copy of the virtual machine, you can
download it from Zenodo `here`__. After the download finishes, click ``File`` in VirtualBox, then
``Import appliance``, then select the file you downloaded.

__ https://doi.org/10.5281/zenodo.3406325

During the import, you'll see an initialization wizard. Make sure that the virtual machine is configured with two CPUs.

Start the virtual machine and log in as user ``travis`` with password ``password``.

Once the system has booted, start both a terminal and Firefox by clicking their respective
icons. Use Firefox to navigate to the tutorial text at `<https://xenon-tutorial.readthedocs.io>`_.

In the terminal, confirm that the ``xenon`` command line interface
program can be found on the system:

.. code-block:: bash

   xenon --help

.. code-block:: bash

   xenon --version
   Xenon CLI v3.0.4, Xenon library v3.0.4, Xenon cloud library v3.0.2

|

If you run into trouble, :doc:`here are some pointers</when-things-dont-work>` on what you can do.

|

Interacting with filesystems
----------------------------

Essentially, ``xenon`` can be used to manipulate files and to interact with schedulers, where either one can be local
or remote. Let's start simple and see if we can do something with local files. First, check its help:

.. code-block:: bash

      xenon filesystem --help

The usage line suggests we need to pick one from ``{file,ftp,s3,sftp,webdav}``.
Again, choose what seems to be the simplest option (``file``), and again, check its help.

.. code-block:: bash

      xenon filesystem file --help

``xenon filesystem file``'s usage line seems to suggest that I need to pick one
from ``{copy,list,mkdir,remove,rename}``. Simplest one is probably ``list``, so:

.. code-block:: bash

      xenon filesystem file list --help

So we need a ``path`` as final argument.

In case you hadn't noticed the pattern, stringing together any number of ``xenon`` subcommands and appending ``--help``
to it will get you help on the particular combination of subcommands you supplied.

The focus of this tutorial is on using Xenon's command line interface, but be
aware that you can use xenon's functionality from other programming
languages through `xenon's  gRPC extension`__.

Where relevant, we have included equivalent code snippets,
written in Java and Python, as a separate tab.

__ https://github.com/xenon-middleware/xenon-grpc

Let's try listing the contents of ``/home/travis/fixtures/``.

.. tabs::

   .. group-tab:: Bash

      .. literalinclude:: code-tabs/bash/DirectoryListing.sh
         :language: bash

   .. group-tab:: Java

      .. literalinclude:: code-tabs/java/src/main/java/nl/esciencecenter/xenon/tutorial/DirectoryListing.java
         :language: java
         :linenos:

   .. group-tab:: Python

      .. literalinclude:: code-tabs/python/pyxenon_snippets/directory_listing.py
         :language: python
         :linenos:

The result should be more or less the same as that of ``ls -1``.

``xenon filesystem file list`` has a few options that let you specify the details of the list operation, e.g.
``--hidden``

.. tabs::

   .. group-tab:: Bash

      .. literalinclude:: code-tabs/bash/DirectoryListingShowHidden.sh
         :language: bash

   .. group-tab:: Java

      .. literalinclude:: code-tabs/java/src/main/java/nl/esciencecenter/xenon/tutorial/DirectoryListingShowHidden.java
         :language: java
         :linenos:

   .. group-tab:: Python

      .. literalinclude:: code-tabs/python/pyxenon_snippets/directory_listing_show_hidden.py
         :language: python
         :linenos:

and ``--recursive``

.. tabs::

   .. group-tab:: Bash

      .. literalinclude:: code-tabs/bash/DirectoryListingRecursive.sh
         :language: bash

   .. group-tab:: Java

      .. literalinclude:: code-tabs/java/src/main/java/nl/esciencecenter/xenon/tutorial/DirectoryListingRecursive.java
         :language: java
         :linenos:

   .. group-tab:: Python

      .. literalinclude:: code-tabs/python/pyxenon_snippets/directory_listing_recursive.py
         :language: python
         :linenos:

Now let's create a file and try to use ``xenon`` to copy it:

.. code-block:: bash

      cd /home/travis
      echo 'some content' > thefile.txt

Check the relevant help

.. code-block:: bash

      xenon filesystem file --help
      xenon filesystem file copy --help

So, the ``copy`` subcommand takes a source path and a target path:

.. tabs::

   .. group-tab:: Bash

      .. literalinclude:: code-tabs/bash/CopyFileLocalToLocalAbsolutePaths.sh
         :language: bash

   .. group-tab:: Java

      .. literalinclude:: code-tabs/java/src/main/java/nl/esciencecenter/xenon/tutorial/CopyFileLocalToLocalAbsolutePaths.java
         :language: java
         :linenos:

   .. group-tab:: Python

      .. literalinclude:: code-tabs/python/pyxenon_snippets/copy_file_local_to_local_absolute_paths.py
         :language: python
         :linenos:

Note that the source path may be standard input, and that the target path may be standard output:

.. code-block:: bash

      # read from stdin:
      cat thefile.txt | xenon filesystem file copy - mystdin.txt

      # write to stdout:
      xenon filesystem file copy thefile.txt - 1> mystdout.txt

``xenon filesystem file`` has a few more subcommands, namely ``mkdir``, ``rename`` and ``remove``. You can
experiment a bit more with those before moving on to the next section.

Access to remote filesystems
----------------------------

Of course the point of ``xenon`` is not to move around files on your local filesystem. There are enough tools to help you with
that. The idea is that you can also use ``xenon`` to move files to and from different types of remote servers, without having to
learn a completely different tool every time.

First, let's check which types of file servers ``xenon`` currently supports:

.. code-block:: bash

      xenon filesystem --help

The usage line shows that besides ``file`` we can also choose ``ftp, s3, sftp`` or ``webdav``. Let's try ``ftp`` first.

.. code-block:: bash

      xenon filesystem ftp --help

The usage line tells us that ``ftp`` has an mandatory parameter ``--location`` which we haven't seen yet. We can use this to specify
which server to connect to. Additionally, there are also optional ``--username`` and ``--password`` options in case we need
to log into the machine.

Let's see if we can use this to connect to a real machine on the internet. A public FTP server for testing should be available at
``test.rebex.net`` with the credentials ``demo`` and ``password``:

.. tabs::

   .. group-tab:: Bash

      .. literalinclude:: code-tabs/bash/FTPDirectoryListing.sh
         :language: bash

   .. group-tab:: Java

      .. literalinclude:: code-tabs/java/src/main/java/nl/esciencecenter/xenon/tutorial/FTPDirectoryListingShowHidden.java
         :language: java
         :linenos:

This should give you a listing of the server at ``test.rebex.net``.

Besides the commands we have already seen (``copy``, ``list``, etc.), ``ftp`` also supports a few new ones, namely ``upload``
and ``download``. We can use these to transer files to and from the server. For example, this command will download a file from
our example FTP server:

.. code-block:: bash

      # download a file from the ftp server
      xenon filesystem ftp --location test.rebex.net --username demo --password password download /readme.txt `pwd`/readme.txt

You can even print the remote file on your screen by copying it to stdout:

.. code-block:: bash

      # print a file from the ftp server on the screen
      xenon filesystem ftp --location test.rebex.net --username demo --password password download /readme.txt -

Note that when using ``copy`` on remote servers, ``xenon`` will attempt to copy the file on the server itself. Since we don't have write
access to this FTP server, the command will fail.

The strength of ``xenon`` is that you can now use the same syntax to access a different type of server. For example, the ``test.rebex.net``
server also offers a secure FTP (``sftp``) service for testing. We can access that service with ``xenon`` by simply changing ``ftp`` into ``sftp``:

.. code-block:: bash

      # list the files on the sftp server
      xenon filesystem sftp --location test.rebex.net --username demo --password password list /

      # download a file from the sftp server
      xenon filesystem sftp --location test.rebex.net --username demo --password password download /readme.txt `pwd`/readme2.txt

In case you are reluctant to type plaintext passwords on the command line, for example because of logging in
``~/.bash_history``, know that you can supply passwords from a file, as follows:

.. code-block:: bash

      # read password from the password.txt file
      xenon filesystem sftp --location test.rebex.net --username demo --password @password.txt list /

in which the file ``password.txt`` should contain the password. Since everything about the user ``xenon`` is public
knowledge anyway, such security precautions are not needed for this tutorial, so we'll just continue to use the
``--password PASSWORD`` syntax.

You can also transfer data from and to other types of file servers (such as ``WebDAV`` and ``S3``) in a similar fashion. We are working to add
support for other types such as GridFTP and iRODS. We will come back to transferring files in the sections below.

|
|
|

Interacting with schedulers
---------------------------

Now let's see if we can use schedulers, starting with `SLURM`__. For this part, we need access to a machine that is running
SLURM. To avoid problems related to network connectivity, we won't try to connect to a physically remote SLURM machine,
but instead, we'll use a dockerized SLURM installation. This way, we can mimic whatever infrastructure we need. The
setup will thus be something like this:

__ https://slurm.schedmd.com/

.. image:: _static/babushka.svg.png
   :height: 300px
   :alt: babushka
   :align: center

|
|

A copy of the SLURM Docker image (`xenonmiddleware/slurm`__:17) has been included in the virtual machine. Bring it
up with:

__ https://hub.docker.com/r/xenonmiddleware/slurm/

.. code-block:: bash

      docker run --detach --publish 10022:22 --hostname slurm17 xenonmiddleware/slurm:17

Use ``docker ps`` to check the state of the container

.. code-block:: bash

      docker ps

The last column in the resulting table lists the name of the container. By
default, ``docker`` assigns automatically generated names, like
``practical_robinson``, ``keen_goodall`` or ``infallible_morse``. You can use
this name to stop and remove a container once you're done with it, as follows:

.. code-block:: bash

      docker stop practical_robinson
      docker rm practical_robinson

Anyway, that's for later. For now, check that the container's status is
``healthy``, and see if you can ``ssh`` into it on port ``10022`` as user
``xenon`` with password ``javagat``:

.. code-block:: bash

      ssh -p 10022 xenon@localhost

      # if that works, exit again
      exit

Be aware that ``ssh`` can sometimes be a little picky. We've assembled a list of
tips and tricks for :doc:`troubleshooting SSH</troubleshooting-ssh>`.

Check the help to see how the ``slurm`` subcommand works:

.. code-block:: bash

      xenon scheduler slurm --help

Let's first ask what queues the SLURM scheduler has. For this, we need to specify
a location, otherwise ``xenon`` does not know who to ask for the list of queues. According to the help,
``LOCATION`` is any location format supported by ``ssh`` or ``local`` scheduler.
Our dockerized SLURM machine is reachable as ``ssh://localhost:10022``.
We'll also need to provide a ``--username`` and ``--password``
for that location, as follows:

.. tabs::

   .. group-tab:: Bash

      .. literalinclude:: code-tabs/bash/SlurmQueuesGetter.sh
         :language: bash

   .. group-tab:: Java

      .. literalinclude:: code-tabs/java/src/main/java/nl/esciencecenter/xenon/tutorial/SlurmQueuesGetter.java
         :language: java
         :linenos:

   .. group-tab:: Python

      .. literalinclude:: code-tabs/python/pyxenon_snippets/slurm_queues_getter.py
         :language: python
         :linenos:

Besides ``queues``, other ``slurm`` subcommands are ``exec``, ``submit``, ``list``, ``remove``, and ``wait``. Let's try
to have ``xenon`` ask SLURM for its list of jobs in each queue, as follows:

.. code-block:: bash

      xenon scheduler slurm --location ssh://localhost:10022 --username xenon --password javagat list
      # should work, but we don't have any jobs yet

Now, let's try to submit a job using ``slurm submit``. Its usage string suggests that we need to provide (the path
of) an ``executable``. Note that the executable should be present inside the container when SLURM starts its execution.
For the moment, we'll use ``/bin/hostname`` as the executable. It simply prints the name of the host on the command line.
For our docker container, it should return the hostname ``slurm17`` of the Docker
container, or whatever hostname you specified for it when you ran the ``docker run`` command earlier:

.. code-block:: bash

      # check the slurm submit help for correct syntax
      xenon scheduler slurm submit --help

      # let xenon submit a job with /bin/hostname as executable
      xenon scheduler slurm --location ssh://localhost:10022 --username xenon --password javagat \
      submit /bin/hostname

      # add --stdout to the submit job to capture its standard out so we know it worked:
      xenon scheduler slurm --location ssh://localhost:10022 --username xenon --password javagat \
      submit --stdout hostname.stdout.txt /bin/hostname

      # check to see if the output was written to file /home/xenon/hostname.stdout.txt
      xenon filesystem sftp --location localhost:10022 --username xenon --password javagat download hostname.stdout.txt -

Below are a few more examples of ``slurm submit``:

.. code-block:: bash

      # executables that take options prefixed with '-' need special syntax, e.g. 'ls -la'
      xenon scheduler slurm --location ssh://localhost:10022 --username xenon --password javagat \
      submit --stdout /home/xenon/ls.stdout.txt ls -- -la

      # check to see if the output was written to file /home/xenon/ls.stdout.txt
      xenon filesystem sftp --location localhost:10022 --username xenon --password javagat download ls.stdout.txt -

      # submit an 'env' job with environment variable MYKEY, and capture standard out so we know it worked
      xenon scheduler slurm --location ssh://localhost:10022 --username xenon --password javagat \
      submit --stdout /home/xenon/env.stdout.txt --env MYKEY=myvalue /usr/bin/env

      # check to see if the output from 'env' was written to file /home/xenon/env.stdout.txt
      xenon filesystem sftp --location localhost:10022 --username xenon --password javagat download env.stdout.txt -

|
|
|

Combining filesystems and schedulers
------------------------------------

So far, we've used ``xenon`` to manipulate files on the local filesystem, and to run system executables on the remote
machine. In typical usage, however, you would use ``xenon`` to run executables or scripts of your own, which means that
we need to upload such files from the local system to the remote system.

A typical workflow may thus look like this:

   1. upload input file(s)
   2. submit job
   3. download generated output file(s)

Use an editor to create a file ``sleep.sh`` with the following contents (the virtual machine comes with a bunch of editors
like ``gedit``, ``leafpad``, and ``nano``, but you can install a different editor from the repositories if you like):

.. literalinclude:: code-tabs/bash/sleep.sh
   :language: bash

You can test if your file is correct by:

.. code-block:: bash

      # last argument is the sleep duration in seconds
      bash sleep.sh 5

We need to upload ``sleep.sh`` to the remote machine. We can't use ``xenon filesystem file`` like we did before,
because we're copying between file systems, so let's look at what other options are available:

.. code-block:: bash

      xenon filesystem --help

      # let's try sftp protocol
      xenon filesystem sftp --help

      # we're interested in 'upload' for now
      xenon filesystem sftp upload --help

We'll also need to tell ``xenon`` what location we want to connect to, and what credentials to use. The SLURM Docker
container we used before is accessible via SFTP using the same location, username and password as before, so let's use
that:

.. tabs::

   .. group-tab:: Bash

      .. literalinclude:: code-tabs/bash/UploadFileLocalToSftpAbsolutePaths.sh
         :language: bash

   .. group-tab:: Java

      .. literalinclude:: code-tabs/java/src/main/java/nl/esciencecenter/xenon/tutorial/UploadFileLocalToSftpAbsolutePaths.java
         :language: java
         :linenos:

   .. group-tab:: Python

      .. literalinclude:: code-tabs/python/pyxenon_snippets/upload_file_local_to_sftp_absolute_paths.py
         :language: python
         :linenos:

Now that the script is in place, we can submit a ``bash`` job using ``xenon scheduler slurm submit`` like before, taking
the newly uploaded ``sleep.sh`` file as input to ``bash``, and using a sleep duration of 60 seconds:

.. code-block:: bash

      # step 2: submit job
      xenon scheduler slurm --location ssh://localhost:10022 --username xenon --password javagat \
      submit --stdout sleep.stdout.txt bash sleep.sh 60

      # (should return an identifier for the job)

With the job running, let's see if it shows up in any of the SLURM queues:

.. tabs::

   .. group-tab:: Bash

      .. literalinclude:: code-tabs/bash/SlurmJobListGetter.sh
         :language: bash

   .. group-tab:: Java

      .. literalinclude:: code-tabs/java/src/main/java/nl/esciencecenter/xenon/tutorial/SlurmJobListGetter.java
         :language: java
         :linenos:

   .. group-tab:: Python

      .. literalinclude:: code-tabs/python/pyxenon_snippets/slurm_job_list_getter.py
         :language: python
         :linenos:

When we submitted, we did not specify any queues, so the default queue ``mypartition`` was used:

.. code-block:: bash

      xenon scheduler slurm --location ssh://localhost:10022 --username xenon --password javagat list --queue mypartition
      # should have the job identifier in it that was printed on the command line

      xenon scheduler slurm --location ssh://localhost:10022 --username xenon --password javagat list --queue otherpartition
      # this queue is empty

With step 1 (upload) and step 2 (submit) covered, step 3 (download) remains:

.. tabs::

   .. group-tab:: Bash

      .. literalinclude:: code-tabs/bash/DownloadFileSftpToLocalAbsolutePaths.sh
         :language: bash

   .. group-tab:: Java

      .. literalinclude:: code-tabs/java/src/main/java/nl/esciencecenter/xenon/tutorial/DownloadFileSftpToLocalAbsolutePaths.java
         :language: java
         :linenos:

   .. group-tab:: Python

      .. literalinclude:: code-tabs/python/pyxenon_snippets/download_file_sftp_to_local_absolute_paths.py
         :language: python
         :linenos:

By this time you may start to consider putting those 3 commands in a script, as follows:

.. tabs::

   .. group-tab:: Bash

      .. literalinclude:: code-tabs/bash/AllTogetherNowWrong.sh
         :language: bash

   .. group-tab:: Java

      .. literalinclude:: code-tabs/java/src/main/java/nl/esciencecenter/xenon/tutorial/AllTogetherNowWrong.java
         :language: java
         :linenos:

However, if you create the script above and run it, you'll find that:

1. Xenon complains about some destination paths already existing.
2. The script finishes suspiciously quickly;

The first error is easily avoided by adding a ``--replace`` optional argument after ``upload`` and ``download``, but
that does not address the real issue: that of Xenon not waiting for the completion of our sleep job.

Not to worry though, we can use ``xenon scheduler slurm wait`` to wait for jobs to finish. In order to make this work,
we do need to capture the identifier for a specific job, otherwise we don't know what to wait for.

Adapt the script as follows and run it:

.. tabs::

   .. group-tab:: Bash

      .. literalinclude:: code-tabs/bash/AllTogetherNow.sh
         :language: bash

   .. group-tab:: Java

      .. literalinclude:: code-tabs/java/src/main/java/nl/esciencecenter/xenon/tutorial/AllTogetherNow.java
         :language: java
         :linenos:

   .. group-tab:: Python

      .. literalinclude:: code-tabs/python/pyxenon_snippets/all_together_now.py
         :language: python
         :linenos:

After about 60 seconds, you should have a local copy of ``sleep.stdout.txt``, with the correct contents this time.

Congratulations -- you have successfully completed the tutorial!

Cleanup
^^^^^^^

Use ``docker ps`` to check the state of the container:

.. code-block:: bash

      docker ps

The last column in the resulting table lists the name of the container. By
default, ``docker`` assigns automatically generated names, like
``practical_robinson``, ``keen_goodall`` or ``infallible_morse``. You can use
this name to stop and remove a container once you're done with it, as follows:

.. code-block:: bash

      docker stop practical_robinson
      docker rm practical_robinson

|
|
|

What's next?
------------

If you want, you can continue reading about relevant subjects, or try some of the suggested exercises.

Further reading
^^^^^^^^^^^^^^^
- Xenon's homepage on `GitHub`__
- Xenon's JavaDoc on `github.io`__
- PyXenon: The Python interface to Xenon (`github.com`__, `readthedocs.io`__)

__ https://github.com/xenon-middleware/xenon
__ http://xenon-middleware.github.io/xenon/versions/3.0.4/javadoc
__ https://github.com/xenon-middleware/pyxenon
__ http://pyxenon.readthedocs.io/en/latest/

Suggested exercises
^^^^^^^^^^^^^^^^^^^

- Repeat selected exercises, but test against a physically remote system instead of a Docker container. Requires
  credentials for the remote system.
- Repeat selected exercises using `WebDAV`__ instead of SFTP. We included the Docker container `xenonmiddleware/webdav`__
  as part of the virtual machine for testing.
- Use the ``s3`` file adaptor to connect to Amazon's
  `Simple Storage Service`__. Either use the Docker container `xenonmiddleware/s3`__ (included in this virtual machine) for
  testing on your own machine, or use an existing Amazon Web Services account for testing against the real thing.

__ https://en.wikipedia.org/wiki/WebDAV
__ https://hub.docker.com/r/xenonmiddleware/webdav/
__ https://aws.amazon.com/s3
__ https://hub.docker.com/r/xenonmiddleware/s3/


|
|
|
|
|
|

This document was generated from `its source files`__ using Sphinx.


|
|

__ https://github.com/xenon-middleware/xenon-tutorial/
