import json

class Items:
    def __init__(self) -> None:
        try:
            with open('items.json', 'r') as f:
                self.items = json.load(f)
        except FileNotFoundError:
            self.items = []
    def all(self):
        return self.items

    def get(self, id):
        items = [item for item in self.all() if item['id'] == id]
        if items:
            return items[0]
        return {}    
    def add(self, data):
        self.items.append(data)
        self.save()
    def save(self):
        with open('items.json', 'w') as f:
            json.dump(self.items, f)    
    
    def delete(self, id):
        item =self.get(id)
        if item:
            self.items.remove(item)
            self.save()
            return True
        return False
        
    def update(self, id, data):
        item = self.get(id)
        if item:
            index = self.items.index(item)
            self.items[index] = data
            self.save()
            return True
        return False       

items = Items()    