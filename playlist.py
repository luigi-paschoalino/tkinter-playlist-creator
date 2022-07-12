import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from tkinter.constants import FIRST, LAST
import artista as art
import pickle
import os.path

class Playlist:
    def __init__(self, nome):
        self.__nome = nome
        
        self.__musicas = []
        
    def getNome(self):
        return self.__nome
    
    def getMusicas(self):
        return self.__musicas
    
    def addMusica(self, musica):
        self.__musicas.append(musica)
    
    def printMusicas(self):
        lista = self.getNome() + ':\n----------------\n'
        for musica in self.__musicas:
            lista += musica.getTitulo() + ' - ' + musica.getArtista().getNome() + '\n'
        return lista
    
class LimiteCriaPlaylist(tk.Toplevel):
    def __init__(self, controle, listaArtistas):
        tk.Toplevel.__init__(self)
        self.geometry('300x250')
        self.title('Playlist')
        self.controle = controle
        
        self.frameNome = tk.Frame(self)
        self.frameArtista = tk.Frame(self)
        self.frameMusicas = tk.Frame(self)
        self.frameButton = tk.Frame(self)
        self.frameNome.pack()
        self.frameArtista.pack()
        self.frameMusicas.pack()
        self.frameButton.pack()
        
        self.labelNome = tk.Label(self.frameNome, text='Nome da playlist: ')
        self.labelNome.pack(side='left')
        self.inputNome = tk.Entry(self.frameNome, width=20)
        self.inputNome.pack(side='left')
        
        self.labelArtista = tk.Label(self.frameArtista, text='Artista: ')
        self.labelArtista.pack(side='left')
        self.escolhaCombo = tk.StringVar()
        self.combobox = ttk.Combobox(self.frameArtista, width=15, textvariable=self.escolhaCombo)
        self.combobox.pack(side='left')
        self.combobox['values'] = listaArtistas
        
        self.labelMusicas = tk.Label(self.frameMusicas, text='Escolha as músicas: ')
        self.labelMusicas.pack(side='left')
        self.listbox = tk.Listbox(self.frameMusicas)
        self.listbox.pack(side='left')
            
        self.buttonInsere = tk.Button(self.frameButton, text='Inserir música')
        self.buttonInsere.pack(side='left')
        self.buttonInsere.bind('<Button>', controle.insereMusica)
        
        self.buttonBuscar = tk.Button(self.frameButton, text='Buscar músicas')
        self.buttonBuscar.pack(side='left')
        self.buttonBuscar.bind('<Button>', controle.buscarMusicas)
        
        self.buttonCria = tk.Button(self.frameButton, text='Criar playlist')
        self.buttonCria.pack(side='left')
        self.buttonCria.bind('<Button>', controle.enterHandler)
        
    def mostraJanela(self, titulo, msg):
        messagebox.showinfo(titulo, msg)
        
class CtrlPlaylist():
    def __init__(self, controlePrincipal):
        if not os.path.isfile('playlist.pickle'):
            self.listaPlaylists = []
        else:
            with open('playlist.pickle', 'rb') as f:
                self.listaPlaylists = pickle.load(f)
        
        self.musicasPlaylist = []
        self.ctrlPrincipal = controlePrincipal
        
    def getListaPlaylist(self):
        return self.listaPlaylists
    
    def getPlaylist(self, plistNome):
        plistRet = None
        for plist in self.listaPlaylists:
            if plistNome == plist.getNome():
                plistRet = plist
        return plistRet
    
    def getListaMusicas(self, nomeArtista):
        listaMusicas = []
        for musica in self.ctrlPrincipal.ctrlArtista.getArtista(nomeArtista).getMusicas():
            listaMusicas.append(musica)
    
    def criaPlaylist(self):
        listaArtistas = []
        for artista in self.ctrlPrincipal.ctrlArtista.getListaArtistas():
            listaArtistas.append(artista.getNome())
        del listaArtistas[0]
        self.limiteIns = LimiteCriaPlaylist(self, listaArtistas)
        
    def buscarMusicas(self, event):
        artista = self.limiteIns.escolhaCombo.get()
        if self.limiteIns.listbox.size() != 0:
            self.limiteIns.listbox.delete(0, tk.END)
        for musica in self.ctrlPrincipal.ctrlArtista.getArtista(artista).getMusicas():
            self.limiteIns.listbox.insert(tk.END, musica.getTitulo())
        
    def consultaPlaylist(self):
        busca = simpledialog.askstring('Consulta', 'Insira o nome da playlist: ')
        if busca is not None:
            for plist in self.listaPlaylists:
                if busca == plist.getNome():
                    messagebox.showinfo('Conteúdo da playlist', plist.printMusicas())
                    return
            messagebox.showerror('Erro na busca', 'A playlist pesquisada não foi encontrada')
        else:
            pass
        
    def salvaPlaylist(self):
        if len(self.listaPlaylists) != 0:
            with open('playlist.pickle', 'wb') as f:
                pickle.dump(self.listaPlaylists, f)
                
    def insereMusica(self, event):
        musicaSel = self.limiteIns.listbox.get(tk.ACTIVE)
        for musica in self.ctrlPrincipal.ctrlArtista.getArtista(self.limiteIns.escolhaCombo.get()).getMusicas():
            if musica.getTitulo() == musicaSel:
                self.musicasPlaylist.append(musica)
                break
        self.limiteIns.mostraJanela('Sucesso', 'Música adicionada com sucesso')
        self.limiteIns.listbox.delete(tk.ACTIVE)
                
    def enterHandler(self, event):
        nome = self.limiteIns.inputNome.get()
        playlist = Playlist(nome)
        for musica in self.musicasPlaylist:
            playlist.addMusica(musica)
        self.listaPlaylists.append(playlist)
        self.musicasPlaylist.clear()
        self.limiteIns.mostraJanela('Sucesso', 'Playlist criada com sucesso')
        self.limiteIns.destroy()
        