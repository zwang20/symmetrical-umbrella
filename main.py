"""
main.py

The main file of the program.
"""

import asyncio
import base64
import logging
import os
import socket
import tkinter
import tkinter.ttk

import aiohttp
import aiohttp.web

import src.datastore


class Server:
    """
    aiohttp server class
    """


    def __init__(self):
        self.port = 0
        self.routes = aiohttp.web.RouteTableDef()
        self.runner = None

        # load keys
        public_key = src.datastore.DataStore().get_keys()[0]

        # convert public key to text
        text = public_key.save_pkcs1().decode('utf-8')

        @self.routes.get('/')
        async def hello(request):
            str(request)
            return aiohttp.web.Response(text=text)

        @self.routes.post("/ping")
        async def ping(request):
            str(request)
            return aiohttp.web.Response(text="pong")

        @self.routes.get("/echo")
        async def echo(request):
            str(request)
            return aiohttp.web.Response(text=request.query['text'])

        @self.routes.get("/cert")
        async def cert(request):
            str(request)

            # get current path
            current_path = os.getcwd()

            # id path
            id_path = os.path.join(current_path, 'data', "id")

            # load id
            with open(id_path, 'r', encoding="utf-8") as id_file:
                self_id = id_file.readline()

            # get cert path
            cert_path = os.path.join(current_path, 'certs', f"{self_id}.json")

            # load cert
            with open(cert_path, 'r', encoding="utf-8") as cert_file:
                cert = cert_file.read()

            return aiohttp.web.Response(text=cert)

        @self.routes.get("/sig")
        async def sig(request):
            str(request)

            # get current path
            current_path = os.getcwd()

            # id path
            id_path = os.path.join(current_path, 'data', "id")

            # load id
            with open(id_path, 'r', encoding="utf-8") as id_file:
                self_id = id_file.readline()

            # get signature path
            sig_path = os.path.join(current_path, 'certs', f"{self_id}.pem")

            # load signature
            with open(sig_path, 'rb') as sig_file:
                signiture = str(base64.b64encode(sig_file.read()))

            return aiohttp.web.Response(text=signiture)

        @self.routes.get("/routes")
        async def routes(request):
            str(request)
            return aiohttp.web.Response(text='\n'.join(str(route) for route in self.routes))


    @classmethod
    async def create(cls):
        """
        create a new server
        """

        self = cls()

        # get free port
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

            # bind to free port
            sock.bind(('127.0.0.1', 0))

            # save port
            self.port = sock.getsockname()[1]

            # close socket
            sock.close()

        # start server
        logging.info("Starting server on port %d", self.port)
        app = aiohttp.web.Application()
        app.add_routes(self.routes)
        self.runner = aiohttp.web.AppRunner(app)

        # return server
        return self


class App(object):
    """
    tkinter app class
    """

    def __init__(self) -> None:
        super().__init__()

        # create stream lists
        self.connections = []
        self.pending_connections = []

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

        # initialise variables
        self.main_server = None
        self.ip_address = tkinter.StringVar()

        # display current ip addresses and port
        tkinter.Label(
            self.mainframe,
            text="Current IP Address: "
        ).grid(column=0, row=0, sticky=tkinter.W)
        address_label = tkinter.Label(self.mainframe, textvariable=self.ip_address)
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

        # # create connect button
        # tkinter.Button(
        #     self.mainframe,
        #     text="Connect",
        #     command=lambda: self.connect(connect_to.get())
        # ).grid(column=2, row=1, sticky=(tkinter.W, tkinter.E))


    @classmethod
    async def create(cls) -> None:
        """
        create a new app
        """
        self = App()

        # create stream server
        logging.info("Creating stream server")
        self.main_server = await Server.create()


        # get ip address
        self.ip_address.set(
            f"{await self.get_current_ip()}:{self.main_server.port}"
        )

        # return self
        return self


    @staticmethod
    async def get_current_ip() -> str:
        """
        return the current ip address
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get('https://api6.ipify.org') as response:
                    return await response.text()
        except aiohttp.client_exceptions.ClientConnectorError:
            pass
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get('https://api4.ipify.org') as response:
                    return await response.text()
        except aiohttp.client_exceptions.ClientConnectorError:
            return "error"


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


async def main():
    """
    main function
    """
    app = await App.create()

    await app.main_server.runner.setup()
    site = aiohttp.web.TCPSite(app.main_server.runner, '', app.main_server.port)
    await site.start()

    while True:
        await app.update()
        await asyncio.sleep(0.1)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main())
