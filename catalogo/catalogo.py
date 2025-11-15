# Importa a biblioteca para mexer com o banco de dados SQLite
import sqlite3

# Define o nome do arquivo do banco de dados
DB_NAME = "catalogo_jogos.db"

def criar_tabela():
    """
    Cria a tabela 'jogos' no banco de dados se ela ainda não existir.
    """
    # conn = sqlite3.connect(DB_NAME)  # Conecta ao banco
    # O try...finally garante que a conexão será fechada mesmo se der erro
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()  # Cria um cursor para executar comandos

        # Executa o comando SQL para criar a tabela
        # "IF NOT EXISTS" garante que não vai dar erro se a tabela já existir
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS jogos (
            id_jogo INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            plataforma TEXT,
            genero TEXT,
            status TEXT 
            -- Status pode ser: 'Jogando', 'Zerado', 'Quero Jogar'
        );
        """)

        conn.commit()  # Salva (comita) as mudanças
        print("Tabela 'jogos' verificada/criada com sucesso.")
    
    except sqlite3.Error as e:
        print(f"Ocorreu um erro ao criar a tabela: {e}")
    
    finally:
        if conn:
            conn.close()  # Fecha a conexão


def adicionar_jogo():
    """
    Pede ao usuário os dados de um novo jogo e insere no banco.
    (CREATE do CRUD)
    """
    print("\n--- Adicionar Novo Jogo ---")
    titulo = input("Título: ")
    plataforma = input("Plataforma (PC, PS5, etc.): ")
    genero = input("Gênero (RPG, FPS, etc.): ")
    status = input("Status (Jogando, Zerado, Quero Jogar): ")

    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        # IMPORTANTE: Usamos '?' para evitar SQL Injection.
        # Os valores são passados em uma tupla (segundo argumento do execute)
        cursor.execute("""
        INSERT INTO jogos (titulo, plataforma, genero, status) 
        VALUES (?, ?, ?, ?);
        """, (titulo, plataforma, genero, status))

        conn.commit()
        print(f"Jogo '{titulo}' adicionado com sucesso!")

    except sqlite3.Error as e:
        print(f"Ocorreu um erro ao adicionar o jogo: {e}")
    
    finally:
        if conn:
            conn.close()


def listar_jogos():
    """
    Busca e exibe todos os jogos cadastrados no banco.
    (READ do CRUD)
    """
    print("\n--- Meu Catálogo de Jogos ---")
    
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM jogos ORDER BY titulo;") # Ordena por título
        
        jogos = cursor.fetchall()  # Busca todos os resultados

        if not jogos:
            print("Nenhum jogo encontrado no catálogo.")
        else:
            # Formata e exibe cada jogo
            print(f"{'ID':<4} | {'Título':<30} | {'Plataforma':<15} | {'Gênero':<15} | {'Status':<15}")
            print("-" * 84) # Linha divisória
            for jogo in jogos:
                # jogo[0] é o id, jogo[1] é o titulo, etc.
                # :<N formata a string para ter N caracteres, alinhada à esquerda
                print(f"{jogo[0]:<4} | {jogo[1]:<30} | {jogo[2]:<15} | {jogo[3]:<15} | {jogo[4]:<15}")
                
    except sqlite3.Error as e:
        print(f"Ocorreu um erro ao listar os jogos: {e}")

    finally:
        if conn:
            conn.close()


def atualizar_status():
    """
    Atualiza o status de um jogo existente.
    (UPDATE do CRUD)
    """
    print("\n--- Atualizar Status do Jogo ---")
    # Primeiro, mostramos a lista para o usuário saber qual ID usar
    listar_jogos() 
    
    try:
        id_para_atualizar = int(input("\nDigite o ID do jogo que deseja atualizar: "))
        novo_status = input("Digite o novo status (Jogando, Zerado, etc.): ")

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("UPDATE jogos SET status = ? WHERE id_jogo = ?;", (novo_status, id_para_atualizar))
        
        conn.commit()
        
        # cursor.rowcount nos diz quantas linhas foram afetadas
        if cursor.rowcount == 0:
            print(f"Erro: Jogo com ID {id_para_atualizar} não encontrado.")
        else:
            print(f"Status do jogo ID {id_para_atualizar} atualizado para '{novo_status}'!")
            
    except ValueError:
        print("Entrada inválida. O ID deve ser um número.")
    except sqlite3.Error as e:
        print(f"Ocorreu um erro ao atualizar o jogo: {e}")
    finally:
        if conn:
            conn.close()


def deletar_jogo():
    """
    Remove um jogo do banco de dados pelo ID.
    (DELETE do CRUD)
    """
    print("\n--- Deletar Jogo ---")
    # Mostramos a lista para o usuário saber qual ID usar
    listar_jogos()

    try:
        id_para_deletar = int(input("\nDigite o ID do jogo que deseja DELETAR: "))
        
        # Confirmação de segurança
        confirmar = input(f"Tem certeza que deseja deletar o jogo ID {id_para_deletar}? (s/n): ").strip().lower()

        if confirmar == 's':
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()

            cursor.execute("DELETE FROM jogos WHERE id_jogo = ?;", (id_para_deletar,))
            
            conn.commit()
            
            if cursor.rowcount == 0:
                print(f"Erro: Jogo com ID {id_para_deletar} não encontrado.")
            else:
                print(f"Jogo ID {id_para_deletar} DELETADO com sucesso.")
            
        else:
            print("Operação cancelada.")
            
    except ValueError:
        print("Entrada inválida. O ID deve ser um número.")
    except sqlite3.Error as e:
        print(f"Ocorreu um erro ao deletar o jogo: {e}")
    finally:
        if conn:
            conn.close()


def menu_principal():
    """
    Exibe o menu principal e controla o fluxo do programa.
    """
    # Garante que a tabela exista antes de mostrar o menu
    criar_tabela()

    while True:
        print("\n===== CATÁLOGO DE JOGOS (Python + SQL) =====")
        print("1. Adicionar novo jogo")
        print("2. Listar todos os jogos")
        print("3. Atualizar status de um jogo")
        print("4. Deletar um jogo")
        print("0. Sair")
        
        opcao = input("Escolha uma opção: ").strip() # .strip() remove espaços em branco

        if opcao == '1':
            adicionar_jogo()
        elif opcao == '2':
            listar_jogos()
        elif opcao == '3':
            atualizar_status()
        elif opcao == '4':
            deletar_jogo()
        elif opcao == '0':
            print("Saindo... Até mais!")
            break
        else:
            print("Opção inválida. Tente novamente.")

# --- Ponto de entrada do script ---
# Se este arquivo (catalogo.py) for executado diretamente...
if __name__ == "__main__":
    menu_principal()