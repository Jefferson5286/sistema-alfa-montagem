import os

# Extensões de arquivos relevantes
EXTENSOES_RELEVANTES = (
    ".py", ".html", ".js", ".ts", ".json", ".txt", ".md", ".yml", ".yaml", ".toml"
)

# Pastas a ignorar
PASTAS_IGNORADAS = {
    ".git", "__pycache__", "node_modules", ".venv", "env", "venv", ".mypy_cache", ".pytest_cache", ".idea", ".vscode", "exclude"
}

# Caminho do projeto
caminho_base = '/home/jeffers/Projects/PycharmProjects/sistema-alfa-montagem'
saida_txt = "projeto_exportado.txt"

with open(saida_txt, "w", encoding="utf-8") as arquivo_saida:
    for raiz, pastas, arquivos in os.walk(caminho_base):
        # Ignora pastas desnecessárias
        pastas[:] = [p for p in pastas if p not in PASTAS_IGNORADAS]

        for nome_arquivo in arquivos:
            if nome_arquivo.endswith(EXTENSOES_RELEVANTES):
                caminho_arquivo = os.path.join(raiz, nome_arquivo)
                try:
                    with open(caminho_arquivo, "r", encoding="utf-8") as f:
                        conteudo = f.read()

                    # Escreve no txt com delimitadores
                    arquivo_saida.write(f"{'-'*80}\n")
                    arquivo_saida.write(f"ARQUIVO: {os.path.relpath(caminho_arquivo, caminho_base)}\n")
                    arquivo_saida.write(f"{'-'*80}\n")
                    arquivo_saida.write(conteudo + "\n\n")

                except Exception as e:
                    print(f"[ERRO] Não foi possível ler {caminho_arquivo}: {e}")

print(f"\n✅ Exportação finalizada! Conteúdo salvo em: {saida_txt}")
