# local
MyListsTest
    .create_pre_authenticated_session --> .management.commands.create_session
                                          .create_pre_authenticated_session
# staging
MyListsTest
	.create_pre_authenticated_session

  |
 \|/

server_tools
	.create_session_on_server

  |
 \|/

subprocess.check_output

  |
 \|/

fab

  |
 \|/

fabfile.create_session_on_server

  |
 \|/

run manage.py create_session

  |
 \|/

.management.commands.create_session
.create_pre_authenticated_session