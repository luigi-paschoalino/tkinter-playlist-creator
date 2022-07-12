import tkinter as tk
from tkinter import messagebox
import artista as art
import playlist as plist
import album as alb

class LimitePrincipal():
    def __init__(self, root, controle):
        self.controle = controle
        self.root = root
        self.root.geometry('300x250')
        self.menubar = tk.Menu(self.root)
        self.artistaMenu = tk.Menu(self.menubar)
        self.albumMenu = tk.Menu(self.menubar)
        self.playlistMenu = tk.Menu(self.menubar)
        self.sairMenu = tk.Menu(self.menubar)
        
        self.artistaMenu.add_command(label='Cadastrar', \
                    command=self.controle.cadastraArtista)
        self.artistaMenu.add_command(label='Consultar', \
                    command=self.controle.consultaArtista)
        self.menubar.add_cascade(label='Artista', \
                    menu=self.artistaMenu)
        
        self.albumMenu.add_command(label='Cadastrar', \
                    command=self.controle.cadastraAlbum)
        self.albumMenu.add_command(label='Consultar', \
                    command=self.controle.consultaAlbum)
        self.menubar.add_cascade(label='Álbum', \
                    menu=self.albumMenu)
        
        self.playlistMenu.add_command(label='Criar', \
                    command=self.controle.criaPlaylist)
        self.playlistMenu.add_command(label='Consultar', \
                    command=self.controle.consultaPlaylist)
        self.menubar.add_cascade(label='Playlist', \
                    menu=self.playlistMenu)
        
        self.sairMenu.add_command(label='Salvar e sair', \
                    command=self.controle.salvaDados)
        self.menubar.add_cascade(label='Opções', \
                    menu=self.sairMenu)
        
        self.root.config(menu=self.menubar)
        
class ControlePrincipal():
    def __init__(self):
        self.root = tk.Tk()
        
        self.ctrlArtista = art.CtrlArtista(self)
        self.ctrlAlbum = alb.CtrlAlbum(self)
        self.ctrlPlaylist = plist.CtrlPlaylist(self)
        
        self.limite = LimitePrincipal(self.root, self)
        
        self.root.title('Playlist Maker')
        
        self.root.mainloop()
        
    def cadastraArtista(self):
        self.ctrlArtista.cadastraArtista()
        
    def consultaArtista(self):
        self.ctrlArtista.consultaArtista()
        
    def cadastraAlbum(self):
        self.ctrlAlbum.cadastraAlbum()
        
    def consultaAlbum(self):
        self.ctrlAlbum.consultaAlbum()
        
    def criaPlaylist(self):
        self.ctrlPlaylist.criaPlaylist()
        
    def consultaPlaylist(self):
        self.ctrlPlaylist.consultaPlaylist()
        
    def salvaDados(self):
        self.ctrlArtista.salvaArtistas()
        self.ctrlAlbum.salvaAlbum()
        self.ctrlPlaylist.salvaPlaylist()
        self.root.destroy()
        
if __name__ == '__main__':
    c = ControlePrincipal()