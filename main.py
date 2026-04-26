import networkx as nx

G = nx.Graph()

edges = [
("Core","R1",2),
("Core","R2",3),
("Core","R3",2),
("Core","R4",4),

("R1","DB_Server",1),
("R1","Web_Server",2),
("R1","Mail_Server",2),
("R1","DNS_Server",1),

("R2","SW1",2),
("R2","SW2",3),
("R3","SW3",2),
("R4","SW4",3),

("SW1","PC1",1),
("SW1","PC2",1),
("SW1","PC3",2),
("SW1","PC4",2),

("SW2","PC5",1),
("SW2","PC6",2),
("SW2","PC7",1),
("SW2","PC8",2),

("SW3","PC9",1),
("SW3","PC10",2),
("SW3","PC11",1),
("SW3","PC12",2),

("SW4","PC13",1),
("SW4","PC14",2),
("SW4","PC15",1),

("R2","R3",4),
("R3","R4",3),
("R2","R4",5),

("Firewall1","Core",2),
("Firewall2","Core",2),
]

G.add_weighted_edges_from(edges)

print("Вузлів у графі:",len(G.nodes()))

start=input("Початковий вузол: ")
end=input("Кінцевий вузол: ")

path=nx.dijkstra_path(G,start,end)
length=nx.dijkstra_path_length(G,start,end)

print("Маршрут:",path)
print("Вага:",length)