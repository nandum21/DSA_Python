import tkinter as tk

# ---------- Trie ----------
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for ch in word.lower():
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end = True

    def search_prefix(self, prefix):
        node = self.root

        for ch in prefix.lower():
            if ch not in node.children:
                return []

            node = node.children[ch]

        result = []
        self._dfs(node, prefix.lower(), result)
        return result

    def _dfs(self, node, current, result):
        if node.is_end:
            result.append(current)

        for ch, child in node.children.items():
            self._dfs(child, current + ch, result)


# ---------- Sample Names ----------
names = [
    "Sadanandam",
    "Sai",
    "Sairam",
    "Saketh",
    "Samuel",
    "Sandeep",
    "Sanjay",
    "Sarath",
    "Satish",
    "Sowmya"
]

trie = Trie()

for name in names:
    trie.insert(name)


# ---------- Tkinter ----------
root = tk.Tk()
root.title("Trie Autocomplete")
root.geometry("300x300")

entry = tk.Entry(root, font=("Arial", 14))
entry.pack(fill="x", padx=10, pady=10)

listbox = tk.Listbox(root, font=("Arial", 12))
listbox.pack(fill="both", expand=True, padx=10, pady=10)


def update_list(event=None):
    prefix = entry.get()

    listbox.delete(0, tk.END)

    if prefix == "":
        return

    matches = trie.search_prefix(prefix)

    for name in matches:
        listbox.insert(tk.END, name.title())


entry.bind("<KeyRelease>", update_list)

root.mainloop()
