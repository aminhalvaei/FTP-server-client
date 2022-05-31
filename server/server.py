import socket
import os
import sys
import random

port_number=2121
isconnected=False
BUFFER_SIZE = 1024
welcoming_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
welcoming_socket.bind(('',port_number))
welcoming_socket.listen(1)
print('This server is ready to perform!')

def list_files() :
    dir_list = os.listdir()
    dir_list_result = list()
    total_size = 0
    for item in dir_list :
        path = os.getcwd()+'\\'+item
        total_size_of_dir = 0
        if os.path.isdir(path) :
            
            for path,dirs,files in os.walk(path):
                for f in files:
                    fp = os.path.join(path, f)
                    total_size_of_dir += os.path.getsize(fp)
                
            dir_list_result.append('>'+item+'   '+str(total_size_of_dir))
            total_size += total_size_of_dir
        else :
            file_size = os.path.getsize(path)
            dir_list_result.append(item+'   '+str(file_size))
            total_size += file_size
            
        dir_list_result[-1]=dir_list_result[-1]+'bytes'
            
    dir_list_result.append('total size of this directory: '+str(total_size)+'bytes')
    dir_list = str(dir_list_result)
    connection_server.send(dir_list.encode())
    print('list sent to client')

def change_dir() :
    path = os.getcwd()+'\\'+raw_command[raw_command.find(' ')+1:len(raw_command)]
    if os.path.isdir(path) :
        os.chdir(path)
        print('directory changed to '+os.getcwd())
        current_working_dir()
    else :
        connection_server.send('invalid dir name'.encode())

def download_file() :
    data_port_number=random.randint(3000,50000)
    connection_server.send(str(data_port_number).encode())
    welcoming_data_server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    welcoming_data_server_socket.bind(('',data_port_number))
    welcoming_data_server_socket.listen(1)
    data_server_socket , addr=welcoming_data_server_socket.accept()
    print('data transfering tunnel established on {}'.format(addr))
        
    path =  path = os.getcwd()+'\\'+raw_command[raw_command.find(' ')+1:len(raw_command)]
    if os.path.isfile(path) :
        connection_server.send(str(True).encode())
        f = open(path,'rb')
        data_buffer_size = os.path.getsize(path)
        connection_server.send(str(data_buffer_size).encode())
        data = f.read(data_buffer_size)
        data_server_socket.send(data)
    else :
        connection_server.send(False)
        print('bad request from client')
        
    data_server_socket.close()
    welcoming_data_server_socket.close()
            
def current_working_dir() :
    full_cwd = os.getcwd() 
    result = full_cwd[full_cwd.find('server')-1:len(full_cwd)]
    result = result.replace('\\server','\\')
    result = result.replace('\\\\','\\')
    connection_server.send(result.encode())
    print('cwd sent to client')
    
def quit_program(isconnected,connection_server) :
    isconnected = False
    print('client disconnected')
    connection_server.send('goodbye from server!'.encode())
    connection_server.close()

while True :
    
    if isconnected == False :
        connection_server , addr=welcoming_socket.accept()
        isconnected = True
        print('client connected')
        
    raw_command=connection_server.recv(BUFFER_SIZE).decode()
    
    if raw_command.__contains__(' ') :
        head_command = raw_command[0:raw_command.find(' ')]
        head_command = head_command.upper()
    else :
        head_command = raw_command.upper()
        
    
    if head_command == 'QUIT' :
        isconnected = False
        print('client disconnected')
        connection_server.send('goodbye from server!'.encode())
    elif head_command == 'PWD' :
        current_working_dir()
    elif head_command == 'LIST' :
        list_files()
    elif head_command == 'CD' :
        change_dir()
    elif head_command == 'DWLD' :
        download_file()
    
        