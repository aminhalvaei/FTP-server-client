import socket

server_ip='127.0.0.1'
server_portnumber=2121
BUFFER_SIZE = 1024
client_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect((server_ip,server_portnumber))
print('connection established successfully')

def print_help() :
    
    instructions = {
        'HELP' : 'To show commnds list.',
        'LIST' : 'Lists files in current path.',
        'PWD' : 'Prints current path.',
        'CD <dir_name>' : 'Changes directory.',
        'DWLD <file_path>' : 'Downloads file.',
        'QUIT' : 'Exit'
    }
    
    print('\n')
    
    for command in instructions:
       print("{:<20} {:<30}".format(command,instructions[command]))
       
def list_files():
    client_socket.send('LIST'.encode())
    dir_list = client_socket.recv(BUFFER_SIZE).decode()
    dir_list = eval(dir_list)
    
    for item in dir_list :
        print(item)
        
    
    
    
def download_file() :
    
    client_socket.send(raw_command.encode())
    data_port_number=int(client_socket.recv(BUFFER_SIZE).decode())
    data_client_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    data_client_socket.connect((server_ip,data_port_number))
    everyThingIsOk = bool(client_socket.recv(BUFFER_SIZE).decode())
    
    if everyThingIsOk:
        
        file = open(raw_command[raw_command.find(' '):len(raw_command)],'wb')
        data_buffer_size = int(client_socket.recv(BUFFER_SIZE).decode())
        recived_data = data_client_socket.recv(data_buffer_size)
        file.write(recived_data)
        print('file downloaded')          
    else :
        
        print('bad request or file can not be downloaded')
            
    data_client_socket.close()
        
    
    
def current_working_dir() :
    client_socket.send(raw_command.encode())
    text_result=client_socket.recv(BUFFER_SIZE).decode()
    print(text_result)
    
def quit_program() :
    client_socket.send(raw_command.encode())
    text_result=client_socket.recv(BUFFER_SIZE).decode()
    print(text_result)
    if text_result == 'goodbye from server!' :
        client_socket.close()
        exit()

def change_dir() :
    client_socket.send(raw_command.encode())
    changed_dir = client_socket.recv(BUFFER_SIZE).decode()
    print(changed_dir)
    
print_help()

while True :
    raw_command = input('\nplease enter the command: ')
    
    if raw_command.__contains__(' ') :
        head_command = raw_command[0:raw_command.find(' ')]
        head_command = head_command.upper()
    else :
        head_command = raw_command.upper()

        
        
    head_command = head_command.upper()
    
    if head_command == 'HELP' :
        print_help()
    elif head_command == 'LIST' :
        list_files()
    elif head_command == 'DWLD' :
        download_file()
    elif head_command == 'PWD' :
        current_working_dir()
    elif head_command == 'CD' :
        change_dir()
    elif head_command == 'QUIT' :
        quit_program()
    else :
        print('command doesnt exist')
        
    