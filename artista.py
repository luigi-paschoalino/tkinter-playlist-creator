import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
import album as alb
import playlist as plist
import os.path
import pickle

class Artista:
    def __init__(self, nome):
        self.__nome = nome
        
        self.__albuns = []
        self.__musicas = []
        
    def getNome(self):
        return self.__nome
    
    def getAlbuns(self):
        return self.__albuns
    
    def getMusicas(self):
        return self.__musicas
    
    def addAlbum(self, album):
        self.__albuns.append(album)
        
    def addMusica(self, musica):
        self.__musicas.append(musica)
        
    def printAlbuns(self):
        lista = self.getNome() + '\n---------------\n'
        for album in self.__albuns:
            lista += album.getTitulo() + ' - ' + str(album.getAno()) + '\n'
            for musica in album.getFaixas():
                lista += ' ' + str(musica.getNroFaixa()) + ' - ' + musica.getTitulo() + '\n'
            lista += '---------------\n'
        return lista
        
class LimiteCadastraArtistas(tk.Toplevel):
    def __init__(self, controle):
        
        tk.Toplevel.__init__(self)
        self.geometry('250x100')
        self.title('Artista')
        self.controle = controle
        
        self.frameNome = tk.Frame(self)
        self.frameButton = tk.Frame(self)
        self.frameNome.pack()
        self.frameButton.pack()
        
        self.labelNome = tk.Label(self.frameNome,text='Nome: ')
        self.labelNome.pack(side='left')
        
        self.inputNome = tk.Entry(self.frameNome, width=20)
        self.inputNome.pack(side='left')
        
        self.buttonSubmit = tk.Button(self.frameButton,text='Enter')
        self.buttonSubmit.pack(side='left')
        self.buttonSubmit.bind('<Button>', controle.enterHandler)
        
        self.buttonFecha = tk.Button(self.frameButton,text='Concluído')
        self.buttonFecha.pack(side='left')
        self.buttonFecha.bind('<Button>', controle.fechaHandler)
        
    def mostraJanela(self, titulo, msg):
        messagebox.showinfo(titulo, msg)
        
class CtrlArtista():
    def __init__(self, controlePrincipal):
        if not os.path.isfile('artista.pickle'):
            artColetanea = Artista('Vários artistas')
            self.listaArtistas = [artColetanea]
        else:
            with open('artista.pickle', 'rb') as f:
                self.listaArtistas = pickle.load(f)
                
        self.ctrlPrincipal = controlePrincipal
        
    def getArtista(self, nome):
        artRet = None
        for art in self.listaArtistas:
            if art.getNome() == nome:
                artRet = art
        return artRet
    
    def getNomeArtistas(self):
        nomeArtistas = []
        for art in self.listaArtistas:
            nomeArtistas.append(art.getNome())
        return nomeArtistas
    
    def getListaArtistas(self):
        return self.listaArtistas
    
    def cadastraArtista(self):
        self.limiteIns = LimiteCadastraArtistas(self)
        
    def consultaArtista(self):
        busca = simpledialog.askstring('Consulta', 'Digite o nome do artista: ')
        if busca is not None:
            for art in self.listaArtistas:
                if busca == art.getNome():
                    messagebox.showinfo('Resultado da busca', '{}'.format(art.printAlbuns()))
                    return
            messagebox.showerror('Erro na busca', 'O artista pesquisado não existe.')
        else:
            pass
    
    def salvaArtistas(self):
        if len(self.listaArtistas) != 0:
            with open('artista.pickle', 'wb') as f:
                pickle.dump(self.listaArtistas, f)
                
    def enterHandler(self, event):
        nome = self.limiteIns.inputNome.get()
        artista = Artista(nome)
        self.listaArtistas.append(artista)
        self.limiteIns.mostraJanela('Sucesso', 'Artista adicionado com sucesso.')
        self.clearHandler(event)
        
    def clearHandler(self, event):
        self.limiteIns.inputNome.delete(0, len(self.limiteIns.inputNome.get()))
    
    def fechaHandler(self, event):
        self.limiteIns.destroy()