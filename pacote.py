def criar(num_sequencia, data = b''):
    seq_bytes = num_sequencia.to_bytes(4, byteorder = 'little', signed = True)
    return seq_bytes + data

def extrair(pacote):
    num_sequencia = int.from_bytes(pacote[0:4], byteorder = 'little', signed = True)
    return num_sequencia, pacote[4:]
