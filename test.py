import weather

g = weather.Gegevens()
g.temperatuur = 33
g.neerslagkans = 0

g.windkracht = 6
print g.generate_cijfer()

g.windkracht = 7
print g.generate_cijfer()
