

class Root_object:
    def from_AL(self, AL, content, list_prop):
        self.conf_dict = {}
        for i in AL[content]:
            if i in list_prop:
                self.conf_dict[i] = AL[content][i]
        #self.conf_dict = {prop:value for (prop, value) in AL[content].items() if prop in list_prop}
