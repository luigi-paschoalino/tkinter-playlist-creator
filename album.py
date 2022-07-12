import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import artista as art
import pickle
import os.path

class Album:
    def __init__(self, titulo, artista, ano):
        self.__titulo = titulo
        self.__artista = artista
        self.__ano = ano

        self.__faixas = []

    def getTitulo(self):
        return self.__titulo

    def getArtista(self):
        return self.__artista

    def getAno(self):
        return self.__ano

    def getFaixas(self):
        return self.__faixas

    def addFaixa(self, musica):
        self.__faixas.append(musica)
    
    def printFaixas(self):
        lista = self.getTitulo() + ' - ' + self.getArtista().getNome() + '\n'
        if self.getArtista().getNome() != 'Vários artistas':
            for musica in self.__faixas:
                lista += str(musica.getNroFaixa()) + ' - ' + musica.getTitulo() + '\n'
        else:
            for musica in self.__faixas:
                lista += str(musica.getNroFaixa()) + ' - ' + musica.getTitulo() + ' - ' + musica.getArtista().getNome() + '\n'
        return lista
        
class Musica:
    def __init__(self, titulo, artista, nroFaixa):
        self.__titulo = titulo
        self.__artista = artista
        self.__nroFaixa = nroFaixa
        
    def getTitulo(self):
        return self.__titulo
    
    def getArtista(self):
        return self.__artista
    
    def getNroFaixa(self):
        return self.__nroFaixa
    
class LimiteCadastraAlbum(tk.Toplevel):
    def __init__(self, controle, listaArtistas):
        
        tk.Toplevel.__init__(self)
        self.geometry('250x120')
        self.title('Álbum')
        self.controle = controle
        
        self.frameTitulo = tk.Frame(self)
        self.frameArtista = tk.Frame(self)
        self.frameAno = tk.Frame(self)
        self.frameMusica = tk.Frame(self)
        self.frameButton = tk.Frame(self)
        self.frameTitulo.pack()
        self.frameArtista.pack()
        self.frameAno.pack()
        self.frameMusica.pack()
        self.frameButton.pack()
        
        self.labelTitulo = tk.Label(self.frameTitulo, text='Título: ')
        self.labelAno = tk.Label(self.frameAno, text='Ano: ')
        self.labelMusica = tk.Label(self.frameMusica, text='Música: ')
        self.labelTitulo.pack(side='left')
        self.labelAno.pack(side='left')
        self.labelMusica.pack(side='left')
        
        self.labelArtista = tk.Label(self.frameArtista, text='Artista: ')
        self.labelArtista.pack(side='left')
        self.escolhaCombo = tk.StringVar()
        self.combobox = ttk.Combobox(self.frameArtista, width=20, textvariable=self.escolhaCombo)
        self.combobox.pack(side='left')
        self.combobox['values'] = listaArtistas
        
        self.inputTitulo = tk.Entry(self.frameTitulo, width=20)
        self.inputTitulo.pack(side='left')
        self.inputAno = tk.Entry(self.frameAno, width=20)
        self.inputAno.pack(side='left')
        self.inputMusica = tk.Entry(self.frameMusica, width=20)
        self.inputMusica.pack(side='left')
        
        self.buttonInsere = tk.Button(self.frameButton, text='Adicionar música')
        self.buttonInsere.pack(side='left')
        self.buttonInsere.bind('<Button>', controle.insereMusica)
        
        self.buttonCria = tk.Button(self.frameButton, text='Criar álbum')
        self.buttonCria.pack(side='left')
        self.buttonCria.bind('<Button>', controle.criaAlbum)
        
    def mostraJanela(self, titulo, msg):
        messagebox.showinfo(titulo, msg)
        
class CtrlAlbum():
    def __init__(self, controlePrincipal):
        if not os.path.isfile('album.pickle'):
            self.listaAlbuns = []
        else:
            with open('album.pickle', 'rb') as f:
                self.listaAlbuns = pickle.load(f)
                
        self.listaMusicas = []
        self.ctrlPrincipal = controlePrincipal
        
    def getAlbum(self, albumNome):
        albumRet = None
        for album in self.listaAlbuns:
            if album.getTitulo() == albumNome:
                albumRet = album
        return albumRet
        
    def cadastraAlbum(self):
        listaArtistas = self.ctrlPrincipal.ctrlArtista.getNomeArtistas()
        self.limiteIns = LimiteCadastraAlbum(self, listaArtistas)
    
    def insereMusica(self, event):
        musicaTitulo = self.limiteIns.inputMusica.get()
        musicaArtista = self.ctrlPrincipal.ctrlArtista.getArtista(self.limiteIns.escolhaCombo.get())
        musicaNro = len(self.listaMusicas)
        musica = Musica(musicaTitulo, musicaArtista, musicaNro)
        self.listaMusicas.append(musica)
        self.limiteIns.mostraJanela('Sucesso', 'Música adicionada com sucesso')
        self.limiteIns.inputMusica.delete(0, len(self.limiteIns.inputMusica.get()))
    
    def criaAlbum(self, event):
        musicaTeste = self.listaMusicas[0]
        unicoArtista = True
        for musica in self.listaMusicas:
            if musicaTeste.getArtista() != musica.getArtista():
                unicoArtista = False
                artista = self.ctrlPrincipal.ctrlArtista.getListaArtistas()[0]
                break
        if unicoArtista:    
            artista = self.ctrlPrincipal.ctrlArtista.getArtista(self.limiteIns.escolhaCombo.get())
        albumTitulo = self.limiteIns.inputTitulo.get()
        albumAno = self.limiteIns.inputAno.get()
        album = Album(albumTitulo, artista, albumAno)
        for musica in self.listaMusicas:
            artista = musica.getArtista()
            artista.addMusica(musica)
            album.addFaixa(musica)
        artista.addAlbum(album)
        self.listaAlbuns.append(album)
        self.listaMusicas.clear()
        self.limiteIns.mostraJanela('Sucesso', 'Álbum criado com sucesso!')
        self.limiteIns.destroy()
        
    def consultaAlbum(self):
        busca = simpledialog.askstring('Consulta', 'Digite o nome do álbum: ')
        if busca is not None:
            for album in self.listaAlbuns:
                if busca == album.getTitulo():
                    messagebox.showinfo('Sucesso', '{}'.format(album.printFaixas()))
                    return
            messagebox.showerror('Erro na consulta', 'O álbum pesquisado não existe')
        else:
            pass
        
    def salvaAlbum(self):
        if len(self.listaAlbuns) != 0:
            with open('album.pickle', 'wb') as f:
                pickle.dump(self.listaAlbuns, f)
