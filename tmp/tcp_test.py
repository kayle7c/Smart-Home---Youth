import socket

socket_server = socket.socket()
socket_server.bind(('', 8888))
# 监听端口
socket_server.listen(128)
print("服务端已开始监听，正在等待客户端连接...")

while True:
    # 等待客户端连接，accept方法返回二元元组(连接对象, 客户端地址信息)
    conn, address = socket_server.accept()
    print(f"接收到了客户端的连接，客户端的信息：{address}")

    while True:
        try:
            # 接收消息
            data: str = conn.recv(1024).decode("UTF-8")
            if not data:  # 如果客户端发送空数据，表示客户端已断开连接
                print("客户端已断开连接")
                break
            print(f"客户端发来的消息是：{data}")
            # 回复消息
            msg = data
            if msg == 'exit':
                break
            conn.send(msg.encode("UTF-8"))  # encode将字符串编码为字节数组对象
        except ConnectionResetError:
            print("客户端强制断开连接")
            break
        except Exception as e:
            print(f"发生错误：{e}")
            break

    # 关闭当前客户端连接
    conn.close()
    print("等待下一个客户端连接...")