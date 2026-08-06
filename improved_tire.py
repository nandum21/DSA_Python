
movies = []

def update_list(event=None):

    global movies

    prefix = entry.get()

    listbox.delete(0, tk.END)

    if prefix == "":
        return

    movies = trie.search_prefix(prefix)

    for movie in movies:
        listbox.insert(tk.END, movie["Movie"])
def show_details(event):

    if not listbox.curselection():
        return

    index = listbox.curselection()[0]

    movie = movies[index]

    details.delete("1.0", tk.END)

    details.insert(tk.END, f"Movie : {movie['Movie']}\n")
    details.insert(tk.END, f"Year : {movie['Year']}\n")
    details.insert(tk.END, f"Certificate : {movie['Certificate']}\n")
    details.insert(tk.END, f"Genre : {movie['Genre']}\n")
    details.insert(tk.END, f"Runtime : {movie['Runtime']} mins\n")
    details.insert(tk.END, f"Rating : {movie['Rating']}\n")
    details.insert(tk.END, f"Ratings : {movie['No.of.Ratings']}\n\n")

    details.insert(tk.END, "Overview\n")
    details.insert(tk.END, "-"*50 + "\n")
    details.insert(tk.END, movie["Overview"])


class TrieNode:
    def __init__(self):
        self.children = {}
        self.movies = []      # Store movie records
        self.is_end = False


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, movie):
        """
        movie is a dictionary:
        {
            "Movie": "...",
            "Year": "...",
            "Genre": "...",
            ...
        }
        """
        title = movie["Movie"].lower()

        node = self.root

        for ch in title:
            if ch not in node.children:
                node.children[ch] = TrieNode()

            node = node.children[ch]

        node.is_end = True
        node.movies.append(movie)

    def search_prefix(self, prefix):

        node = self.root

        for ch in prefix.lower():
            if ch not in node.children:
                return []

            node = node.children[ch]

        result = []
        self._dfs(node, result)

        return result

    def _dfs(self, node, result):

        if node.is_end:
            result.extend(node.movies)

        for child in node.children.values():
            self._dfs(child, result)
import pandas as pd

df = pd.read_csv("TeluguMovies_Clean.csv")

trie = Trie()

for _, row in df.iterrows():
    trie.insert(row.to_dict())

import tkinter as tk

root = tk.Tk()
root.geometry("800x500")

entry = tk.Entry(root, font=("Arial", 14))
entry.pack(fill="x", padx=10, pady=5)

listbox = tk.Listbox(root, height=8)
listbox.pack(fill="x", padx=10)

details = tk.Text(root, height=15)
details.pack(fill="both", expand=True, padx=10, pady=10)


entry.bind("<KeyRelease>", update_list)
listbox.bind("<<ListboxSelect>>", show_details)

root.mainloop()


