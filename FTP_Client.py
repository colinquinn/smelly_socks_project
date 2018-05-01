def post_csv():
    global CSV_FILE_NAME
    sftp = chilkat.CkSFtp()
    success = sftp.UnlockComponent("MARQUE.CB1112018_qbN4VB2x10pV")
    if (success != True):
        print(sftp.lastErrorText())
        sys.exit()

    sftp.put_ConnectTimeoutMs(5000)
    sftp.put_IdleTimeoutMs(10000)

    hostname = "sftp://sftp.gdom.net"
    port = 22
    success = sftp.Connect(hostname,port)
    if (success != True):
        print(sftp.lastErrorText())
        sys.exit()

    success = sftp.AuthenticatePw("smellysocks","dai0xaeJ")
    if (success != True):
        print(sftp.lastErrorText())
        sys.exit()

    success = sftp.InitializeSftp()
    if (success != True):
        print(sftp.lastErrorText())
        sys.exit()

    handle = sftp.openFile(CSV_FILE_NAME,"writeOnly","createTruncate")
    if (sftp.get_LastMethodSuccess() != True):
        print(sftp.lastErrorText())
        sys.exit()

    #  Upload from the local file to the SSH server.
    success = sftp.UploadFile(handle,"./csv_library/" + CSV_FILE_NAME)
    if (success != True):
        print(sftp.lastErrorText())
        sys.exit()

    #  Close the file.
    success = sftp.CloseHandle(handle)
    if (success != True):
        print(sftp.lastErrorText())
        sys.exit()

    print("Success.")
    