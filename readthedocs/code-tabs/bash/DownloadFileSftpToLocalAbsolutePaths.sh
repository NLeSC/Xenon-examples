# step 3: download generated output file(s)
xenon filesystem sftp --location ssh://localhost:10022 --username xenon --password javagat \
download /home/xenon/sleep.stdout.txt /home/alice/xenon/sleep.stdout.txt
