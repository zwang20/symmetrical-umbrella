"""
main.py

The main file of the program.
"""

import os
import asyncio
import logging
import tkinter
import tkinter.ttk
import rsa
import aiohttp

class Stream:
    """
    asyncio stream class
    """

    async def __init__(self, connection_handler, server=True) -> None:
        
        if server:
            self.reader, self.writer = await asyncio.start_server(
                connection_handler,
                "localhost",
                0,
                )


class App(object):
    """
    tkinter app class
    """

    async def __init__(self) -> None:
        super().__init__()

        # get current path
        self.current_path = os.path.dirname(os.path.realpath(__file__))

        # create ./env/ directory
        logging.info("Creating ./env/ directory")
        env_path = os.path.join(self.current_path, 'env')
        if not os.path.exists(env_path):
            os.makedirs(env_path)

        # check if ./env/key.pub exists
        logging.info("Checking if ./env/key.pub exists")
        if not os.path.exists(os.path.join(env_path, 'key.pub')):

            # generate key
            logging.info("Generating key")
            (self.pubkey, self.privkey) = rsa.newkeys(2048)

            # save public key
            with open(os.path.join(env_path, 'key.pub'), 'wb') as key_file:
                key_file.write(self.pubkey.save_pkcs1())

            # save private key
            with open(os.path.join(env_path, 'key'), 'wb') as key_file:
                key_file.write(self.privkey.save_pkcs1())

        # load public key
        logging.info("Loading public key")
        public_key_path = os.path.join(env_path, 'key.pub')
        with open(public_key_path, "rb") as file:
            self.public_key = rsa.PublicKey.load_pkcs1(file.read())

        # load private key
        logging.info("Loading private key")
        private_key_path = os.path.join(env_path, 'key')
        with open(private_key_path, "rb") as file:
            self.private_key = rsa.PrivateKey.load_pkcs1(file.read())

        # create socket lists
        self.connections = []
        self.pending_connections = []

        # create socket server
        logging.info("Creating socket server")
        self.main_socket = self.create_socket()
        self.connections.remove(self.main_socket)

        # start tkinter
        self.root = tkinter.Tk()
        self.root.title("Symmetrical Unbrella")

        self.mainframe = tkinter.Frame(self.root)
        self.mainframe.grid(
            column=0,
            row=0,
            sticky=(tkinter.N, tkinter.W, tkinter.E, tkinter.S),
            padx=5,
            pady=5,
        )

        # get ip address
        self.ip_address = f"{self.get_current_ip()}:{self.main_socket.getsockname()[1]}"

        # display current ip addresses and port
        tkinter.Label(
            self.mainframe,
            text="Current IP Address: "
        ).grid(column=0, row=0, sticky=tkinter.W)
        address_label = tkinter.Label(self.mainframe, text=f"{self.ip_address}")
        address_label.grid(column=1, row=0, sticky=(tkinter.W, tkinter.E))

        # create button to copy ip address to clipboard
        tkinter.Button(
            self.mainframe,
            text="Copy IP Address",
            command=lambda: self.copy_to_clipboard(f"{self.ip_address}")
        ).grid(column=2, row=0, sticky=(tkinter.W, tkinter.E))

        # create input field
        tkinter.Label(self.mainframe, text="Connect to: ").grid(column=0, row=1, sticky=tkinter.W)
        connect_to = tkinter.StringVar()
        address_entry = tkinter.ttk.Entry(self.mainframe, width=7, textvariable=connect_to)
        address_entry.grid(column=1, row=1, sticky=(tkinter.W, tkinter.E))

        # create connect button
        tkinter.Button(
            self.mainframe,
            text="Connect",
            command=lambda: self.connect(connect_to.get())
        ).grid(column=2, row=1, sticky=(tkinter.W, tkinter.E))


    async def

    @staticmethod
    async def get_current_ip() -> str:
        """
        return the current ip address
        """
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api6.ipify.org') as response:
                return await response.text()



    @staticmethod
    def copy_to_clipboard(text: str) -> None:
        """
        copy text to clipboard
        """
        tkint = tkinter.Tk()
        tkint.withdraw()
        tkint.clipboard_clear()
        tkint.clipboard_append(text)
        tkint.update()
        tkint.destroy()


    async def update(self):
        """
        update the app
        """
        # update tkinter
        self.root.update()
        self.root.update_idletasks()



if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app = App()
    while True:
        app.update()
