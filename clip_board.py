
#  Important: It is helpful to send the contents of the
#  sftp.LastErrorText property when requesting support.

sftp = chilkat.CkSFtp()
#
# #  Any string automatically begins a fully-functional 30-day trial.
success = sftp.UnlockComponent("Anything for 30-day trial")
if (success != True):
    print(sftp.lastErrorText())
    sys.exit()

#  Set some timeouts, in milliseconds:
sftp.put_ConnectTimeoutMs(5000)
sftp.put_IdleTimeoutMs(10000)

#  Connect to the SSH server.
#  The standard SSH port = 22
#  The hostname may be a hostname or IP address.

hostname = "sftp://sftp.gdom.net"
port = 22
success = sftp.Connect(hostname,port)
if (success != True):
    print(sftp.lastErrorText())
    sys.exit()

#  Authenticate with the SSH server.  Chilkat SFTP supports
#  both password-based authenication as well as public-key
#  authentication.  This example uses password authenication.
success = sftp.AuthenticatePw("smellysocks","dai0xaeJ")
if (success != True):
    print(sftp.lastErrorText())
    sys.exit()

#  After authenticating, the SFTP subsystem must be initialized:
success = sftp.InitializeSftp()
if (success != True):
    print(sftp.lastErrorText())
    sys.exit()

#  Open a file for writing on the SSH server.
#  If the file already exists, it is overwritten.
#  (Specify "createNew" instead of "createTruncate" to
#  prevent overwriting existing files.)
handle = sftp.openFile("test_csv.csv","writeOnly","createTruncate")
if (sftp.get_LastMethodSuccess() != True):
    print(sftp.lastErrorText())
    sys.exit()

# #  Write some text to the file:
# success = sftp.WriteFileText(handle,"ansi","abcdefghijklmnopqrstuvwxyz")
# if (success != True):
#     print(sftp.lastErrorText())
#     sys.exit()
#
# success = sftp.WriteFileText(handle,"ansi","1234567890")
# if (success != True):
#     print(sftp.lastErrorText())
#     sys.exit()
#
# success = sftp.WriteFileText(handle,"ansi","ABCDEFGHIJKLMNOPQRSTUVWXYZ")
# if (success != True):
#     print(sftp.lastErrorText())
#     sys.exit()


#  Upload from the local file to the SSH server.
success = sftp.UploadFile(handle,"C:\\test_csv.csv")
if (success != True):
    print(sftp.lastErrorText())
    sys.exit()

#  Close the file.
success = sftp.CloseHandle(handle)
if (success != True):
    print(sftp.lastErrorText())
    sys.exit()

print("Success.")

def ping_sftp():
    if(init_sftp()):
        print('\nSuccessfull SFTP connection!\n')
        print(sys_options)
        choose_path()
    else:
        print('ERROR: Ping unsuccessfull. Please check server address, username, and password.')
        print(sys_options)
        choose_path()

def init_sftp():
    #  Important: It is helpful to send the contents of the
    #  sftp.LastErrorText property when requesting support.

    hostname = "sftp://sftp.gdom.net"
    port = 22

    sftp = chilkat.CkSFtp()

    if(not sftp.UnlockComponent("Anything for 30-day trial")):
         print(sftp.lastErrorText())
        else if(sftp.AuthenticatePw("smellysocks","dai0xaeJ")):
             print(sftp.lastErrorText())
            else if(sftp.AuthenticatePw("smellysocks","dai0xaeJ")):
                 print(sftp.lastErrorText())
    if sftp.UnlockComponent("Anything for 30-day trial") == False:
        print(sftp.lastErrorText())
    else:
         if action == 2:
             print_csv_library()
         else:
            if action ==3:
                ping_sftp()
            else:
                if action == 4:
                    print('4')
                else:
                    if action == 5:
                        print('4')
                    else:
                        if action == 6:
                            print('4')
    #
