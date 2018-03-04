import pysftp

with pysftp.Connection('hostname', username='me', password='secret') as sftp:
    with sftp.cd('public'):             # temporarily chdir to public
        sftp.put('/my/local/filename')  # upload file to public/ on remote
        sftp.get('remote_file')         # get a remote file
