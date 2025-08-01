import textwrap
from datetime import datetime

# Cores para melhorar a interface
CORES = {
    'erro': '\033[31m',
    'sucesso': '\033[32m',
    'alerta': '\033[33m',
    'info': '\033[34m',
    'reset': '\033[m'
}

def menu():
    print(f"\n{CORES['info']}======== MENU ========{CORES['reset']}")
    print("1. Depositar")
    print("2. Sacar")
    print("3. Extrato")
    print("4. Novo usuário")
    print("5. Nova conta")
    print("6. Listar contas")
    print("0. Sair")
    return input("=> ")

def depositar(saldo, extrato):
    try:
        valor = float(input("\nValor do depósito: "))
        if valor > 0:
            saldo += valor
            extrato.append(f"{datetime.now().strftime('%d/%m %H:%M')} - Depósito: R$ {valor:.2f}")
            print(f"{CORES['sucesso']}Depositado: R$ {valor:.2f}{CORES['reset']}")
            print(f"Saldo atual: R$ {saldo:.2f}")
        else:
            print(f"{CORES['erro']}Valor inválido{CORES['reset']}")
    except:
        print(f"{CORES['erro']}Digite um número válido{CORES['reset']}")
    return saldo, extrato

def sacar(saldo, extrato, limite, saques_hoje, limite_saques):
    print(f"\nSaques hoje: {saques_hoje}/{limite_saques}")
    print(f"Limite por saque: R$ {limite:.2f}")
    
    try:
        valor = float(input("\nValor do saque: "))
        
        if valor <= 0:
            print(f"{CORES['erro']}Valor deve ser positivo{CORES['reset']}")
        elif valor > saldo:
            print(f"{CORES['erro']}Saldo insuficiente{CORES['reset']}")
        elif valor > limite:
            print(f"{CORES['erro']}Excede limite por saque{CORES['reset']}")
        elif saques_hoje >= limite_saques:
            print(f"{CORES['erro']}Limite diário atingido{CORES['reset']}")
        else:
            saldo -= valor
            extrato.append(f"{datetime.now().strftime('%d/%m %H:%M')} - Saque: R$ {valor:.2f}")
            saques_hoje += 1
            print(f"{CORES['sucesso']}Saque realizado!{CORES['reset']}")
            print(f"Saldo: R$ {saldo:.2f}")
            
    except:
        print(f"{CORES['erro']}Valor inválido{CORES['reset']}")
    
    return saldo, extrato, saques_hoje

def exibir_extrato(saldo, extrato):
    print(f"\n{CORES['info']}=== EXTRATO ===")
    if not extrato:
        print("Sem movimentações")
    else:
        for mov in extrato:
            print(mov)
    print(f"\nSaldo: R$ {saldo:.2f}{CORES['reset']}")

def criar_usuario(usuarios):
    nome = input("\nNome completo: ")
    cpf = input("CPF (apenas números): ")
    
    # Verifica se CPF já existe
    if any(user['cpf'] == cpf for user in usuarios):
        print(f"{CORES['erro']}CPF já cadastrado{CORES['reset']}")
        return
    
    usuarios.append({
        'nome': nome,
        'cpf': cpf,
        'endereco': input("Endereço: ")
    })
    print(f"{CORES['sucesso']}Usuário criado!{CORES['reset']}")

def criar_conta(agencia, contas, usuarios):
    cpf = input("\nCPF do titular: ")
    usuario = next((u for u in usuarios if u['cpf'] == cpf), None)
    
    if usuario:
        contas.append({
            'agencia': agencia,
            'numero': len(contas) + 1,
            'usuario': usuario
        })
        print(f"{CORES['sucesso']}Conta criada! (Nº {len(contas)}){CORES['reset']}")
    else:
        print(f"{CORES['erro']}Usuário não encontrado{CORES['reset']}")

def listar_contas(contas):
    print(f"\n{CORES['info']}=== CONTAS ===")
    for conta in contas:
        print(f"\nAg: {conta['agencia']} C/C: {conta['numero']}")
        print(f"Titular: {conta['usuario']['nome']}")
        print(f"CPF: {conta['usuario']['cpf']}")
    print(CORES['reset'])

def main():
    AGENCIA = "0001"
    LIMITE_SAQUE = 500
    MAX_SAQUES = 3
    
    saldo = 0
    extrato = []
    saques_hoje = 0
    usuarios = []
    contas = []

    while True:
        op = menu()
        
        if op == "1":  # Depositar
            saldo, extrato = depositar(saldo, extrato)
            
        elif op == "2":  # Sacar
            saldo, extrato, saques_hoje = sacar(
                saldo, extrato, LIMITE_SAQUE, saques_hoje, MAX_SAQUES)
            
        elif op == "3":  # Extrato
            exibir_extrato(saldo, extrato)
            
        elif op == "4":  # Novo usuário
            criar_usuario(usuarios)
            
        elif op == "5":  # Nova conta
            criar_conta(AGENCIA, contas, usuarios)
            
        elif op == "6":  # Listar contas
            listar_contas(contas)
            
        elif op == "0":  # Sair
            print(f"\n{CORES['sucesso']}Até logo!{CORES['reset']}")
            break
            
        else:
            print(f"{CORES['erro']}Opção inválida{CORES['reset']}")

if __name__ == "__main__":
    main()
