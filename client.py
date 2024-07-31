import socket
import threading
import tkinter as tk
import ssl

# HOST = '10.20.200.232'
HOST = '192.168.56.1'
PORT = 8080

class ChatClient:
    def __init__(self):
        
        certfile = "server.crt"
        ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        ssl_context.load_verify_locations(certfile)

        # Connect to the server
        server_address = (HOST, 8080)
        self.client_socket = ssl_context.wrap_socket(socket.socket(socket.AF_INET), server_hostname='localhost')
        self.client_socket.connect(server_address)

        # Create the GUI
        self.root = tk.Tk()
        self.root.title("Chat Room")

        # Create a frame for username entry
        self.username_frame = tk.Frame(self.root)
        self.username_frame.pack(padx=10, pady=10)

        # Create a label and entry widget for username
        self.username_label = tk.Label(self.username_frame, text="Username: ")
        self.username_label.pack(side=tk.LEFT)

        self.username_entry = tk.Entry(self.username_frame, width=50)
        self.username_entry.pack(side=tk.LEFT)

        # Create a frame for chat window
        self.chat_frame = tk.Frame(self.root,bg="#FF00FF")
        self.chat_frame.pack(padx=10, pady=10)

        # Create a scrollbar and text widget for chat window
        self.chat_scrollbar = tk.Scrollbar(self.chat_frame)
        self.chat_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.chat_text = tk.Text(self.chat_frame, height=20, width=50, yscrollcommand=self.chat_scrollbar.set)
        self.chat_text.pack(side=tk.LEFT, fill=tk.BOTH)

        self.chat_scrollbar.config(command=self.chat_text.yview)

        # Create a frame for message entry
        self.message_frame = tk.Frame(self.root)
        self.message_frame.pack(padx=10, pady=10)

        # Create a label and entry widget for message
        self.message_label = tk.Label(self.message_frame, text="Message: ")
        self.message_label.pack(side=tk.LEFT)

        self.message_entry = tk.Entry(self.message_frame, width=50)
        self.message_entry.pack(side=tk.LEFT)

        # Create a button to send message
        self.send_button = tk.Button(self.message_frame, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.LEFT)

        # Start a thread to receive messages from the server
        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.start()

        # Start the GUI main loop
        self.root.mainloop()

    def send_message(self):
    
        username = self.username_entry.get()
        message = self.message_entry.get()

        if username and message:
            # Clear the message entry
            self.message_entry.delete(0, tk.END)

            # Send message to the server in the format "username: message"
            full_message = f"{username}: {message}"
            self.client_socket.send(full_message.encode())

    def receive_messages(self):
        """
        Thread function to receive messages from the server.
        """
        while True:
            try:
                # Receive message from server
                message = self.client_socket.recv(1024).decode()

                # Append message to the chat window
                self.chat_text.insert(tk.END, message+"\n")
                self.chat_text.see(tk.END)
            except:
                # If there's an error, close the socket and exit the thread
                self.client_socket.close()
                break

if __name__ == "__main__":
    ChatClient()

