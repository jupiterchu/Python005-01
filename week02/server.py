import socket


HOST = 'localhost'
PORT = 10000
def server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.bind((HOST, PORT))
    s.listen(1)

    while True:
        conn, addr = s.accept()
        print(f'connection by {addr}, {conn}')

        f = open('upload_file', 'wb')
        try:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                conn.send(b'file send successful!')
                f.write(data)
                print('file accept successful!')

        except Exception as e:
            print(f'File acceptance error -> {e}')
            s.send(b'File acceptance failed!')
        finally:
            f.close()

        conn.close()


if __name__ == "__main__":
    server()
